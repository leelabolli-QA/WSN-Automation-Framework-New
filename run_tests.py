import subprocess
import sys
import os
from pathlib import Path
import shutil
import pdfkit
import json
import matplotlib.pyplot as plt
import webbrowser
from datetime import datetime
import re

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


# Wadhwani brand theme for Allure reports. Mirrors the behave HTML report:
# red brand chrome + orange accent, with passed-status green recolored to
# orange so the report uses only red/orange (no green).
WADHWANI_THEME_CSS = """<style id="wadhwani-theme-overrides">
.side-nav{background:#C8102E !important}
.side-nav__head{border-bottom:1px solid #9e0c24 !important}
.side-nav__link_active{border-right:4px solid #F47920 !important;color:#fff !important}
.side-nav__link:hover{color:#F47920 !important}
.bar__fill_status_passed,.label_status_passed,.chart__legend-icon_status_passed,.y-label_status_passed{background:#F47920 !important}
.alert_status_passed{background:#fbd2b3 !important}
.text_status_passed,.n-label_status_passed{color:#F47920 !important}
.chart__fill_status_passed{fill:#F47920 !important}
.message_status_passed,.status-details_status_passed,.n-label_status_passed{border-color:#F47920 !important}
.status-details_status_passed{background:#ffe8d6 !important}
</style>"""


def apply_wadhwani_theme(report_index_path):
    """Inject Wadhwani brand color overrides into a generated Allure single-file report."""
    try:
        index_path = Path(report_index_path)
        if not index_path.exists():
            return
        html = index_path.read_text(encoding="utf-8")
        if "wadhwani-theme-overrides" in html:
            return  # already themed
        if "</head>" in html:
            html = html.replace("</head>", WADHWANI_THEME_CSS + "</head>", 1)
        elif "</body>" in html:
            html = html.replace("</body>", WADHWANI_THEME_CSS + "</body>", 1)
        else:
            html += WADHWANI_THEME_CSS
        index_path.write_text(html, encoding="utf-8")
        print(f"🎨 Applied Wadhwani theme to {index_path}")
    except Exception as e:
        print(f"❌ Failed to apply Wadhwani theme to {report_index_path}: {e}")


def find_wkhtmltopdf_executable():
    possible_paths = [
        Path("C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"),
        Path("C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe"),
    ]

    for path in possible_paths:
        if path.exists():
            return str(path)

    try:
        result = subprocess.run(["where.exe", "wkhtmltopdf"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().splitlines()[0].strip()
    except Exception:
        pass

    return None

def find_allure_executable():
    possible_paths = [
        Path.home() / "scoop" / "shims" / "allure.bat",
        Path.home() / "scoop" / "shims" / "allure.cmd",
        Path.home() / "allure-2.36.0" / "bin" / "allure.bat",
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    return "allure"

def parse_results(results_dir):
    passed = failed = broken = 0
    for file in Path(results_dir).glob("*.json"):
        try:
            with open(file) as f:
                data = json.load(f)
                status = data.get("status")
                if status == "passed":
                    passed += 1
                elif status == "failed":
                    failed += 1
                elif status == "broken":
                    broken += 1
        except Exception:
            continue
    total = passed + failed + broken
    return total, passed, failed, broken


def collect_scenario_results(results_dir):
    scenarios = []
    for file in Path(results_dir).glob("*-result.json"):
        try:
            with open(file, encoding="utf-8") as f:
                data = json.load(f)

            name = data.get("name", file.name)
            status = (data.get("status") or "unknown").lower()
            start = data.get("start") or 0
            stop = data.get("stop") or start
            duration_sec = round(max(0, stop - start) / 1000, 2)
            details = (data.get("statusDetails") or {}).get("message", "")

            scenarios.append({
                "name": name,
                "status": status,
                "duration": duration_sec,
                "details": details[:240] if isinstance(details, str) else "",
                "start": start,
            })
        except Exception:
            continue

    scenarios.sort(key=lambda item: item.get("start", 0))
    return scenarios


def generate_detailed_pdf_from_results(results_dir, output_pdf):
    if not REPORTLAB_AVAILABLE:
        print("❌ reportlab not installed. Install with: pip install reportlab")
        return False

    total, passed, failed, broken = parse_results(results_dir)
    scenarios = collect_scenario_results(results_dir)
    chart_path = create_chart(passed, failed, broken)

    doc = SimpleDocTemplate(output_pdf, pagesize=A4, leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Automation Execution Report", styles["Title"]))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    summary_data = [
        ["Total", "Passed", "Failed", "Broken"],
        [str(total), str(passed), str(failed), str(broken)]
    ]
    summary_table = Table(summary_data, colWidths=[120, 120, 120, 120])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#F4F7FB")),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))

    if Path(chart_path).exists():
        elements.append(Image(chart_path, width=240, height=240))
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("Scenario Details", styles["Heading2"]))

    scenario_rows = [["#", "Scenario", "Status", "Duration (s)"]]
    for index, row in enumerate(scenarios, start=1):
        scenario_rows.append([str(index), row["name"], row["status"].upper(), str(row["duration"])])

    if len(scenario_rows) == 1:
        scenario_rows.append(["-", "No scenario-level allure results found", "-", "-"])

    scenario_table = Table(scenario_rows, colWidths=[30, 330, 70, 70], repeatRows=1)
    scenario_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]

    for row_num in range(1, len(scenario_rows)):
        status_text = scenario_rows[row_num][2]
        if status_text == "PASSED":
            scenario_style.append(("TEXTCOLOR", (2, row_num), (2, row_num), colors.HexColor("#15803D")))
        elif status_text == "FAILED":
            scenario_style.append(("TEXTCOLOR", (2, row_num), (2, row_num), colors.HexColor("#B91C1C")))
        elif status_text == "BROKEN":
            scenario_style.append(("TEXTCOLOR", (2, row_num), (2, row_num), colors.HexColor("#B45309")))

    scenario_table.setStyle(TableStyle(scenario_style))
    elements.append(scenario_table)

    doc.build(elements)
    return True


def generate_allure_dashboard_pdf(report_dir, output_pdf):
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not available for dashboard-style PDF export")
        return False

    index_file = Path(report_dir) / "index.html"
    if not index_file.exists():
        print("❌ Allure index.html not found for dashboard PDF export")
        return False

    index_uri = index_file.resolve().as_uri()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1600, "height": 2200})
            page.goto(index_uri, wait_until="domcontentloaded", timeout=30000)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            page.wait_for_timeout(500)
            page.pdf(
                path=output_pdf,
                format="A3",
                landscape=True,
                print_background=True,
                margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
            )
            browser.close()
        return True
    except Exception as e:
        print(f"❌ Playwright dashboard PDF export failed: {e}")
        return False


def sanitize_filename(value):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")


def get_pdf_max_screenshots(default_value=30):
    try:
        value = int(os.getenv("PDF_MAX_SCREENSHOTS", str(default_value)))
        return max(1, value)
    except Exception:
        return default_value


def capture_viewport_segments(page, screenshots_dir, base_name, title_prefix, captures):
    viewport = page.viewport_size or {"width": 1600, "height": 1200}
    viewport_height = max(800, int(viewport.get("height", 1200)))
    step = max(600, viewport_height - 120)
    total_height = page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")

    segment_index = 1
    for y in range(0, max(total_height, viewport_height), step):
        page.evaluate(f"window.scrollTo(0, {y});")
        page.wait_for_timeout(700)
        segment_path = screenshots_dir / f"{base_name}_seg_{segment_index:02d}.png"
        page.screenshot(path=str(segment_path), full_page=False)
        captures.append((f"{title_prefix} (Part {segment_index})", segment_path))
        segment_index += 1


def is_empty_allure_section(page):
    try:
        body_text = page.locator("body").inner_text(timeout=3000).lower()
        return "there is nothing to show" in body_text
    except Exception:
        return False


def infer_results_dir_from_report_dir(report_dir):
    report_path = Path(report_dir)
    report_name = report_path.name
    if report_name.startswith("allure-report-"):
        persona_suffix = report_name.replace("allure-report-", "", 1)
        return report_path.parent / f"allure-results-{persona_suffix}"
    return report_path.parent / "allure-results"


def generate_allure_detailed_menu_pdf(report_dir, output_pdf):
    if not PLAYWRIGHT_AVAILABLE or not REPORTLAB_AVAILABLE:
        print("❌ Missing Playwright/ReportLab for menu-wise detailed PDF export")
        return False

    index_file = Path(report_dir) / "index.html"
    if not index_file.exists():
        print("❌ Allure index.html not found for menu-wise detailed PDF export")
        return False

    screenshots_dir = Path(report_dir) / "_menu_screens"
    if screenshots_dir.exists():
        shutil.rmtree(screenshots_dir)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    index_uri = index_file.resolve().as_uri()
    menu_names = ["Overview", "Categories", "Suites", "Graphs", "Timeline", "Behaviors", "Packages"]
    results_dir = infer_results_dir_from_report_dir(report_dir)
    scenario_names = [item.get("name") for item in collect_scenario_results(results_dir) if item.get("name")]
    captures = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1800, "height": 1400})
            page.goto(index_uri, wait_until="domcontentloaded", timeout=30000)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            page.wait_for_timeout(500)
            page.evaluate("document.body.style.zoom='125%'")

            for index, menu in enumerate(menu_names, start=1):
                clicked = False

                link = page.get_by_role("link", name=menu)
                if link.count() > 0:
                    link.first.click(timeout=3000)
                    clicked = True
                else:
                    fallback = page.locator(f"a:has-text('{menu}')")
                    if fallback.count() > 0:
                        fallback.first.click(timeout=3000)
                        clicked = True

                if not clicked:
                    continue

                page.wait_for_timeout(1000)

                if is_empty_allure_section(page):
                    continue

                base_name = f"{index:02d}_{sanitize_filename(menu)}"
                capture_viewport_segments(page, screenshots_dir, base_name, menu, captures)

            suites_link = page.get_by_role("link", name="Suites")
            if suites_link.count() > 0:
                suites_link.first.click(timeout=3000)
                page.wait_for_timeout(500)

                seen_names = set()
                for scenario_index, scenario_name in enumerate(scenario_names, start=1):
                    if scenario_name in seen_names:
                        continue
                    seen_names.add(scenario_name)

                    clicked = False
                    scenario_candidates = [
                        page.get_by_text(scenario_name, exact=True),
                        page.locator(f"text={scenario_name}"),
                    ]

                    for candidate in scenario_candidates:
                        try:
                            if candidate.count() > 0:
                                candidate.first.click(timeout=3000)
                                clicked = True
                                break
                        except Exception:
                            continue

                    if not clicked:
                        continue

                    page.wait_for_timeout(1000)
                    if is_empty_allure_section(page):
                        continue

                    detail_base = f"{len(captures)+1:02d}_suite_detail_{scenario_index:02d}_{sanitize_filename(scenario_name)}"
                    capture_viewport_segments(page, screenshots_dir, detail_base, f"Suite Detail - {scenario_name}", captures)

            browser.close()
    except Exception as e:
        print(f"❌ Failed capturing Allure menu screenshots: {e}")
        return False

    if not captures:
        print("❌ No menu screenshots captured for detailed PDF")
        return False

    try:
        doc = SimpleDocTemplate(
            output_pdf,
            pagesize=landscape(A4),
            leftMargin=16,
            rightMargin=16,
            topMargin=16,
            bottomMargin=16,
        )
        styles = getSampleStyleSheet()
        styles["Title"].fontSize = 24
        styles["Heading2"].fontSize = 16
        styles["Normal"].fontSize = 11
        elements = [
            Paragraph("Allure Detailed Report (Menu-wise)", styles["Title"]),
            Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]),
            Spacer(1, 10),
        ]

        page_width = landscape(A4)[0] - 32
        max_height = landscape(A4)[1] - 80

        for menu, image_path in captures:
            image_reader = ImageReader(str(image_path))
            image_width, image_height = image_reader.getSize()
            scale = min(page_width / image_width, max_height / image_height)
            draw_width = image_width * scale
            draw_height = image_height * scale

            elements.append(Paragraph(menu, styles["Heading2"]))
            image = Image(str(image_path), width=draw_width, height=draw_height)
            elements.append(image)
            elements.append(Spacer(1, 16))

        attachment_images = sorted(results_dir.glob("*-attachment.png"), key=lambda path: path.stat().st_mtime)
        max_screenshots = get_pdf_max_screenshots()

        if attachment_images:
            elements.append(Paragraph("Clicked Screenshots", styles["Heading2"]))
            if len(attachment_images) > max_screenshots:
                elements.append(
                    Paragraph(
                        f"Showing latest {max_screenshots} of {len(attachment_images)} screenshots (auto-limited for PDF size).",
                        styles["Normal"],
                    )
                )
            elements.append(Spacer(1, 8))

            selected_attachments = attachment_images[-max_screenshots:]

            for index, attachment_path in enumerate(selected_attachments, start=1):
                image_reader = ImageReader(str(attachment_path))
                image_width, image_height = image_reader.getSize()
                scale = min(page_width / image_width, max_height / image_height)
                draw_width = image_width * scale
                draw_height = image_height * scale

                elements.append(Paragraph(f"Screenshot {index}", styles["Normal"]))
                elements.append(Image(str(attachment_path), width=draw_width, height=draw_height))
                elements.append(Spacer(1, 14))

        doc.build(elements)
        return True
    except Exception as e:
        print(f"❌ Failed building menu-wise detailed PDF: {e}")
        return False

def create_chart(passed, failed, broken, chart_path="reports/results_chart.png"):
    labels = ['Passed', 'Failed', 'Broken']
    values = [passed, failed, broken]
    colors = ['green', 'red', 'orange']
    plt.figure(figsize=(5,5))
    if sum(values) == 0:
        plt.pie([1], labels=['No Results'], colors=['lightgrey'])
    else:
        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title("Test Results Distribution")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def build_summary_html(total, passed, failed, broken, chart_path):
    chart_abs = Path(chart_path).resolve().as_uri()
    html = f"""
    <h1>Automation Test Summary</h1>
    <p><b>Total Tests:</b> {total}</p>
    <p><b>Passed:</b> {passed}</p>
    <p><b>Failed:</b> {failed}</p>
    <p><b>Broken:</b> {broken}</p>
    <img src="{chart_abs}" alt="Results Chart">
    """
    return html

def generate_summary_pdf(html_content, output_pdf="reports/summary-report.pdf"):
    try:
        wkhtmltopdf_path = find_wkhtmltopdf_executable()
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path) if wkhtmltopdf_path else None
        options = {
            "enable-local-file-access": "",
        }
        pdfkit.from_string(html_content, output_pdf, configuration=config, options=options)
        print(f"✅ Management summary PDF generated at {output_pdf}")
        webbrowser.open(output_pdf)
    except Exception as e:
        print(f"❌ Failed to generate summary PDF: {e}")

def run_tests(feature_path=None, tags=None, trace_on=False, headless=False, persona=None):
    if trace_on:
        os.environ["TRACE_ON"] = "true"
    if headless:
        os.environ["HEADLESS"] = "true"
    if persona:
        os.environ["PERSONA"] = persona

    project_root = Path(__file__).resolve().parent
    python_exe = sys.executable
    persona_key = (persona or os.getenv("PERSONA", "student")).strip().lower()
    results_dir = project_root / "reports" / f"allure-results-{persona_key}"
    report_dir = project_root / "reports" / f"allure-report-{persona_key}"
    report_dir.parent.mkdir(parents=True, exist_ok=True)

    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    cmd = [python_exe, "-m", "behave"]
    cmd.append(feature_path if feature_path else "features/")
    if tags:
        cmd.extend(["--tags", tags])
    cmd.extend([
        "-f", "pretty",
        "-o", "-",
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", str(results_dir),
    ])

    print(f"▶ Running persona: {persona_key} | feature: {feature_path if feature_path else 'features/'}")
    run_env = os.environ.copy()
    run_env["PERSONA"] = persona_key
    if trace_on:
        run_env["TRACE_ON"] = "true"
    if headless:
        run_env["HEADLESS"] = "true"

    result = subprocess.run(cmd, env=run_env)
    print(f"✅ Behave test run complete for persona: {persona_key}")

    if result.returncode != 0:
        print(f"⚠ Behave execution failed for persona '{persona_key}'. Attempting report/PDF generation from available results.")

    allure_exe = find_allure_executable()
    try:
        subprocess.run([
            allure_exe, "generate",
            str(results_dir),
            "-o", str(report_dir),
            "--clean",
            "--single-file"
        ], check=True, shell=True, env=run_env)
        print(f"✅ Allure report generated at {report_dir}/index.html")
        apply_wadhwani_theme(report_dir / "index.html")

        output_pdf = str(report_dir / f"allure-report-{persona_key}.pdf")
        output_pdf_path = Path(output_pdf)
        pdf_candidates = [output_pdf_path]
        timestamped_name = f"allure-report-{persona_key}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
        pdf_candidates.append(report_dir / timestamped_name)

        try:
            dashboard_pdf_ok = False
            generated_pdf_path = None

            for candidate_path in pdf_candidates:
                try:
                    dashboard_pdf_ok = generate_allure_detailed_menu_pdf(report_dir, str(candidate_path))
                    if not dashboard_pdf_ok:
                        dashboard_pdf_ok = generate_allure_dashboard_pdf(report_dir, str(candidate_path))
                    if not dashboard_pdf_ok:
                        dashboard_pdf_ok = generate_detailed_pdf_from_results(results_dir, str(candidate_path))

                    if dashboard_pdf_ok:
                        generated_pdf_path = candidate_path
                        break
                except PermissionError:
                    continue

            if dashboard_pdf_ok and generated_pdf_path:
                print(f"✅ Detailed Allure PDF generated at {generated_pdf_path}")
                webbrowser.open(str(generated_pdf_path))
            else:
                print("❌ Detailed Allure PDF generation skipped")
        except Exception as e:
            print(f"❌ Failed to generate Allure PDF: {e}")

        total, passed, failed, broken = parse_results(results_dir)
        chart_path = create_chart(passed, failed, broken, chart_path=str(report_dir / f"results_chart_{persona_key}.png"))
        summary_html = build_summary_html(total, passed, failed, broken, chart_path)
        generate_summary_pdf(summary_html, output_pdf=str(report_dir / f"summary-report-{persona_key}.pdf"))

        # Executive stakeholder dashboard (self-contained HTML).
        try:
            from utils.executive_report import generate_executive_dashboard
            dashboard_path = generate_executive_dashboard(
                results_dir,
                report_dir / f"executive-dashboard-{persona_key}.html",
                persona=persona_key,
            )
            print(f"✅ Executive dashboard generated at {dashboard_path}")
            webbrowser.open(Path(dashboard_path).resolve().as_uri())
        except Exception as e:
            print(f"❌ Failed to generate executive dashboard: {e}")

    except FileNotFoundError:
        print("❌ Allure CLI not found. Please install Allure Commandline and add it to PATH.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate Allure report: {e}")

    return result.returncode


def run_persona_sequence(personas=None, trace_on=False, headless=False):
    personas_to_run = personas or ["student", "faculty"]
    default_feature_by_persona = {
        "student": "features/Student_All.feature",
        "faculty": "features/faculty_all.feature",
    }

    exit_codes = {}
    project_root = Path(__file__).resolve().parent
    combined_results_dir = project_root / "reports" / "allure-results"

    if combined_results_dir.exists():
        shutil.rmtree(combined_results_dir)
    combined_results_dir.mkdir(parents=True, exist_ok=True)

    for persona in personas_to_run:
        feature_path = default_feature_by_persona.get(persona, "features/")
        code = run_tests(
            feature_path=feature_path,
            tags=None,
            trace_on=trace_on,
            headless=headless,
            persona=persona,
        )
        exit_codes[persona] = code

        persona_results_dir = project_root / "reports" / f"allure-results-{persona}"
        if persona_results_dir.exists():
            for item in persona_results_dir.iterdir():
                if item.is_file():
                    destination = combined_results_dir / f"{persona}_{item.name}"
                    shutil.copy2(item, destination)

    combined_report_dir = project_root / "reports" / "allure-report"
    try:
        allure_exe = find_allure_executable()
        subprocess.run([
            allure_exe, "generate",
            str(combined_results_dir),
            "-o", str(combined_report_dir),
            "--clean",
            "--single-file"
        ], check=True, shell=True)
        print(f"✅ Combined Allure report generated at {combined_report_dir}/index.html")
        apply_wadhwani_theme(combined_report_dir / "index.html")

        combined_pdf_primary = combined_report_dir / "allure-report-combined.pdf"
        combined_pdf_fallback = combined_report_dir / f"allure-report-combined-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
        combined_pdf_candidates = [combined_pdf_primary, combined_pdf_fallback]

        combined_pdf_ok = False
        generated_combined_pdf = None
        for combined_pdf in combined_pdf_candidates:
            try:
                combined_pdf_ok = generate_allure_detailed_menu_pdf(combined_report_dir, str(combined_pdf))
                if not combined_pdf_ok:
                    combined_pdf_ok = generate_allure_dashboard_pdf(combined_report_dir, str(combined_pdf))
                if not combined_pdf_ok:
                    combined_pdf_ok = generate_detailed_pdf_from_results(combined_results_dir, str(combined_pdf))
                if combined_pdf_ok:
                    generated_combined_pdf = combined_pdf
                    break
            except PermissionError:
                continue

        if combined_pdf_ok and generated_combined_pdf:
            print(f"✅ Combined detailed PDF generated at {generated_combined_pdf}")
            webbrowser.open(str(generated_combined_pdf))

        total, passed, failed, broken = parse_results(combined_results_dir)
        combined_chart = create_chart(
            passed,
            failed,
            broken,
            chart_path=str(combined_report_dir / "results_chart_combined.png")
        )
        combined_summary = build_summary_html(total, passed, failed, broken, combined_chart)
        generate_summary_pdf(combined_summary, output_pdf=str(combined_report_dir / "summary-report-combined.pdf"))

        # Combined executive stakeholder dashboard.
        try:
            from utils.executive_report import generate_executive_dashboard
            combined_dashboard = generate_executive_dashboard(
                combined_results_dir,
                combined_report_dir / "executive-dashboard-combined.html",
                persona="combined",
            )
            print(f"✅ Combined executive dashboard generated at {combined_dashboard}")
            webbrowser.open(Path(combined_dashboard).resolve().as_uri())
        except Exception as e:
            print(f"❌ Failed to generate combined executive dashboard: {e}")
    except FileNotFoundError:
        print("❌ Allure CLI not found. Please install Allure Commandline and add it to PATH.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate combined Allure report: {e}")

    for persona, code in exit_codes.items():
        status = "PASSED" if code == 0 else "FAILED"
        print(f"[{persona}] -> {status}")

    return 0 if all(code == 0 for code in exit_codes.values()) else 1

# ---------------------------------------------------------------------------
# Combined dev + prod, all-personas matrix run (single "executive" report)
# ---------------------------------------------------------------------------
PERSONA_PRETTY = {
    "student": "Student",
    "faculty": "Faculty",
    "rm": "Relationship Manager",
    "mentor": "Mentor",
    "career_buddy": "Career Buddy",
    "institute_admin": "Institute Admin",
    "newuser": "New User",
}

DEFAULT_FEATURE_BY_PERSONA = {
    # Student runs the card-based student.feature (matches the prod/new student
    # dashboard), not the older left-nav Student_All.feature.
    "student": "features/student.feature",
    "faculty": "features/faculty_all.feature",
    "rm": "features/rm_all.feature",
    "mentor": "features/mentor.feature",
    "career_buddy": "features/career_buddy.feature",
    # Registers a brand-new account each run (manual email/OTP entry - see
    # features/steps/student_persona/newuser_steps.py), so it needs no
    # persona credentials and skips the shared pre-login entirely.
    "newuser": "features/newuser.feature",
}

# (environment, persona) pairs whose feature differs from the default above.
# The new-user journey is course-specific, and dev/prod host different courses.
FEATURE_BY_ENV_AND_PERSONA = {
    ("prod", "newuser"): "features/newuser_prod.feature",
}


def feature_for(env_name, persona):
    return FEATURE_BY_ENV_AND_PERSONA.get(
        (env_name.lower(), persona), DEFAULT_FEATURE_BY_PERSONA.get(persona, "features/")
    )

# Env var key fragment per persona, used to detect whether credentials exist for
# a given (environment, persona) pair before attempting a run.
_PERSONA_CRED_KEY = {
    "faculty": "FACULTY",
    "rm": "RM",
    "career_buddy": "CAREER_BUDDY",
    "institute_admin": "INSTITUTE_ADMIN",
}


def _ensure_dotenv_loaded():
    """Load .env into os.environ so credential detection sees env-specific keys."""
    try:
        from dotenv import load_dotenv
        for candidate in (Path(".env"), Path("utils/.env/.env")):
            if candidate.exists():
                load_dotenv(dotenv_path=str(candidate), override=False)
                break
    except Exception:
        pass


def has_credentials(env_name, persona):
    """True when a username is configured for this (environment, persona) pair.

    Mirrors the resolution order in config/env_config.py: env-specific key
    (e.g. PROD_FACULTY_USERNAME) first, then the flat fallback.
    """
    e = env_name.upper()
    if persona == "newuser":
        # Registers its own brand-new account each run (manual email/OTP) -
        # no persona credentials to check for.
        return True
    if persona == "student":
        return bool(os.getenv(f"{e}_STUDENT_USERNAME") or os.getenv("STUDENT_USERNAME"))
    if persona == "mentor":
        # Dedicated mentor account first, then Career Buddy (back-compat), then a
        # hardcoded dev-only fallback account.
        return bool(
            os.getenv(f"{e}_MENTOR_USERNAME")
            or os.getenv("MENTOR_USERNAME")
            or os.getenv(f"{e}_CAREER_BUDDY_USERNAME")
            or os.getenv("CAREER_BUDDY_USERNAME")
            or env_name.lower() == "dev"
        )
    key = _PERSONA_CRED_KEY.get(persona)
    if not key:
        return False
    return bool(os.getenv(f"{e}_{key}_USERNAME") or os.getenv(f"{key}_USERNAME"))


def _run_behave_once(feature_path, persona, env_name, results_dir, trace_on=False, headless=False):
    """Run behave for a single (environment, persona) and emit allure results.

    Each run is its own subprocess, so ENV/PERSONA are read fresh by
    config/env_config.py — that is how we switch between dev and prod within one
    orchestrated execution.
    """
    python_exe = sys.executable
    cmd = [python_exe, "-m", "behave", feature_path,
           "-f", "pretty", "-o", "-",
           "-f", "allure_behave.formatter:AllureFormatter", "-o", str(results_dir)]

    run_env = os.environ.copy()
    run_env["ENV"] = env_name
    run_env["PERSONA"] = persona
    run_env["PYTHONUTF8"] = "1"
    run_env["PYTHONIOENCODING"] = "utf-8"
    if trace_on:
        run_env["TRACE_ON"] = "true"
    if headless:
        run_env["HEADLESS"] = "true"

    print(f"▶ Running [{env_name}] / [{persona}] | feature: {feature_path}")
    result = subprocess.run(cmd, env=run_env)
    print(f"✅ Completed [{env_name}] / [{persona}] (exit={result.returncode})")
    return result.returncode


def _merge_run_into_combined(run_results_dir, combined_results_dir, env_name, persona):
    """Copy one run's allure files into the combined dir, tagging each scenario
    result with its environment + persona role.

    Attachment / container files keep their original (uuid) names so the
    `source` references inside the result JSON still resolve — only the
    *-result.json files are rewritten to carry the extra labels.
    """
    pretty_role = PERSONA_PRETTY.get(persona, persona.replace("_", " ").title())
    for item in Path(run_results_dir).iterdir():
        if not item.is_file():
            continue
        destination = combined_results_dir / item.name
        if item.name.endswith("-result.json"):
            try:
                data = json.loads(item.read_text(encoding="utf-8"))
                labels = [l for l in data.get("labels", [])
                          if l.get("name") not in ("environment", "persona_role")]
                labels.append({"name": "environment", "value": env_name})
                labels.append({"name": "persona_role", "value": pretty_role})
                data["labels"] = labels
                destination.write_text(json.dumps(data), encoding="utf-8")
                continue
            except Exception:
                pass  # fall through to a verbatim copy
        shutil.copy2(item, destination)


def run_full_matrix(personas=None, envs=None, trace_on=False, headless=False):
    """Execute every (environment × persona) pair in one go and produce a single
    combined Allure report + combined executive dashboard (the NEN-style report).

    Pairs without configured credentials are skipped (not failed) so a missing
    prod account for, say, Career Buddy does not poison the combined health.
    """
    _ensure_dotenv_loaded()
    envs = [e.strip().lower() for e in (envs or ["dev", "prod"])]
    personas = [p.strip().lower() for p in (personas or ["student", "faculty", "rm", "mentor", "career_buddy", "newuser"])]

    project_root = Path(__file__).resolve().parent
    combined_results_dir = project_root / "reports" / "allure-results-combined"
    combined_report_dir = project_root / "reports" / "allure-report-combined"
    if combined_results_dir.exists():
        shutil.rmtree(combined_results_dir)
    combined_results_dir.mkdir(parents=True, exist_ok=True)

    matrix = []  # (env, persona, status)
    for env_name in envs:
        for persona in personas:
            if not has_credentials(env_name, persona):
                print(f"⏭  Skipping [{env_name}] / [{persona}] — no credentials configured")
                matrix.append((env_name, persona, "skipped"))
                continue

            feature_path = feature_for(env_name, persona)
            run_results_dir = project_root / "reports" / f"allure-results-{env_name}-{persona}"
            if run_results_dir.exists():
                shutil.rmtree(run_results_dir)
            run_results_dir.mkdir(parents=True, exist_ok=True)

            code = _run_behave_once(feature_path, persona, env_name, run_results_dir, trace_on, headless)
            _merge_run_into_combined(run_results_dir, combined_results_dir, env_name, persona)
            matrix.append((env_name, persona, "passed" if code == 0 else "failed"))

    # ---- One combined report for the whole matrix ----
    try:
        allure_exe = find_allure_executable()
        subprocess.run([
            allure_exe, "generate",
            str(combined_results_dir),
            "-o", str(combined_report_dir),
            "--clean",
            "--single-file",
        ], check=True, shell=True)
        print(f"✅ Combined Allure report generated at {combined_report_dir}/index.html")
        apply_wadhwani_theme(combined_report_dir / "index.html")
    except FileNotFoundError:
        print("❌ Allure CLI not found. Please install Allure Commandline and add it to PATH.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate combined Allure report: {e}")

    total, passed, failed, broken = parse_results(combined_results_dir)
    create_chart(passed, failed, broken, chart_path=str(combined_report_dir / "results_chart_combined.png"))

    # Combined executive dashboard (the stakeholder NEN-style report).
    try:
        from utils.executive_report import generate_executive_dashboard
        combined_dashboard = generate_executive_dashboard(
            combined_results_dir,
            combined_report_dir / "executive-dashboard-combined.html",
            persona="combined",
            extra_meta={"env": " + ".join(envs)},
        )
        print(f"✅ Combined executive dashboard generated at {combined_dashboard}")
        webbrowser.open(Path(combined_dashboard).resolve().as_uri())
    except Exception as e:
        print(f"❌ Failed to generate combined executive dashboard: {e}")

    print("\n================ MATRIX SUMMARY ================")
    for env_name, persona, status in matrix:
        print(f"  [{env_name:<5}] {persona:<16} -> {status.upper()}")
    print("===============================================")

    ran = [m for m in matrix if m[2] != "skipped"]
    return 0 if all(m[2] == "passed" for m in ran) else 1


def _force_utf8_stdout():
    """Make stdout/stderr tolerate the emoji status glyphs even when output is
    redirected to a cp1252-encoded file (e.g. a background task), instead of
    crashing with UnicodeEncodeError."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    _force_utf8_stdout()
    run_mode = os.getenv("RUN_MODE", "dual").strip().lower()
    if run_mode == "matrix":
        personas_env = os.getenv("PERSONAS", "").strip()
        envs_env = os.getenv("ENVS", "dev,prod").strip()
        personas = [p for p in re.split(r"[\s,]+", personas_env) if p] or None
        envs = [e for e in re.split(r"[\s,]+", envs_env) if e] or None
        headless = os.getenv("HEADLESS", "false").lower() in ("1", "true", "yes")
        trace_on = os.getenv("TRACE_ON", "false").lower() in ("1", "true", "yes")
        sys.exit(run_full_matrix(personas=personas, envs=envs, trace_on=trace_on, headless=headless))
    _main_legacy()


def _main_legacy():
    run_mode = os.getenv("RUN_MODE", "dual").strip().lower()
    if run_mode == "single":
        persona = os.getenv("PERSONA", "student").strip().lower()
        default_feature_by_persona = {
            "student": "features/student.feature",
            "faculty": "features/faculty_all.feature",
        }
        feature_path = default_feature_by_persona.get(persona, "features/")
        exit_code = run_tests(feature_path=feature_path, persona=persona)
    else:
        exit_code = run_persona_sequence()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
