"""Behave hooks: browser lifecycle, shared pre-login and per-scenario reset.

The run logs in once in `before_all` and every scenario then starts from a
known-good home page. `before_scenario` is responsible for making that true
again after whatever the previous scenario left behind - an open modal, a
stray tab, a logged-out session or even a crashed browser tab.
"""

import os

from playwright.sync_api import sync_playwright

from locators.student_locators.login_locators import LoginLocators
from pages.base_page import BasePage
from pages.login_page import LoginPage
from utils.config import Config
from utils.helpers import attach_screenshot
from utils.logger import log

ACCOUNTS_MENU = "//button[@aria-label='Accounts menu']"

# The "Help us personalize your journey" modal re-appears on every dashboard
# load and overlays the header, intercepting the next scenario's first click.
PERSONALIZE_POPUP = (
    "//*[contains(normalize-space(),'personalize your journey') "
    "or contains(normalize-space(),'personalise your journey')]"
)
PERSONALIZE_POPUP_CLOSE = [
    "//div[contains(@class,'ant-modal')]//button[contains(@class,'ant-modal-close')]",
    "//button[normalize-space()='Skip' or normalize-space()='Maybe Later' "
    "or normalize-space()='Close' or normalize-space()='No, Thanks']",
]
LOGGED_OUT_URL_MARKERS = ("login", "/guest", "sign-in", "signin")

BROWSER_ARGS = [
    "--start-maximized",
    "--use-fake-ui-for-media-stream",      # auto-deny the camera/mic prompt
    "--use-fake-device-for-media-stream",  # use a fake device instead of prompting
]


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _page(context):
    """A BasePage bound to the current tab, for the shared UI helpers."""
    return BasePage(context.page)


def _is_newuser_only_run(context):
    """True when every requested feature path is a new-user feature.

    Those features register a brand-new account through a manual email/OTP
    flow, so they must not go through the shared persona pre-login (which
    assumes an existing, already-verified account).
    """
    paths = getattr(context.config, "paths", None) or []
    return bool(paths) and all("newuser" in os.path.basename(p).lower() for p in paths)


def _new_browser_context(context):
    """A browser context with every permission denied and no fixed viewport."""
    return context.browser.new_context(no_viewport=True, permissions=[])


def _start_tracing(context):
    """Start a Playwright trace for this scenario when TRACE_ON is set."""
    context.trace_enabled = False
    if not Config.TRACE_ON:
        return
    try:
        context.context.tracing.start(screenshots=True, snapshots=True, sources=True)
        context.trace_enabled = True
    except Exception as error:
        log.warning("Could not start tracing: %s", error)


def _login(context, persona):
    """Run the login flow for `persona` and confirm it left the login page."""
    username, password = Config.get_credentials(persona)

    if persona == "student":
        login_page = LoginPage(context.page)
    else:
        from pages.common_pages.common_login_page import CommonLoginPage
        from locators.common_locators.common_login_locators import CommonLoginLocators

        login_page = CommonLoginPage(context.page, login_locators=CommonLoginLocators)

    login_page.open(Config.BASE_URL)
    login_page.dismiss_popup_if_present()
    login_page.click_get_started()
    login_page.click_continue_with_email()
    login_page.login(username, password)

    if persona == "student":
        login_page.wait_for_home_page()
    else:
        context.page.wait_for_load_state("networkidle", timeout=15000)
        context.page.wait_for_function(
            "() => !window.location.href.includes('login')", timeout=20000)


def _ensure_live_page(context):
    """Guarantee `context.page` points at a usable tab.

    A scenario can crash the Chromium tab (or the whole browser context). Every
    later scenario would then fail with "Target page, context or browser has
    been closed", so the tab - and if needed the context - is rebuilt here so a
    single crash does not cascade through the rest of the run.
    """
    try:
        if getattr(context, "page", None) is not None and not context.page.is_closed():
            return True
    except Exception as error:
        log.debug("Could not inspect the current page, assuming it is dead: %s", error)

    try:
        context.page = context.context.new_page()
        return True
    except Exception as error:
        log.debug("Could not open a new page in the existing context: %s", error)

    try:
        context.context = _new_browser_context(context)
        context.page = context.context.new_page()
        return True
    except Exception as error:
        log.error("Could not recreate a live page after a crash: %s", error)
        return False


def _page_is_dead(context):
    try:
        return getattr(context, "page", None) is None or context.page.is_closed()
    except Exception:
        return True


def _re_login(context):
    """Log in again after a session loss (logout step) or a tab crash."""
    persona = getattr(context, "persona", Config.DEFAULT_PERSONA)
    if not _ensure_live_page(context):
        log.error("Re-login aborted: no live page/browser available")
        return

    page = _page(context)
    try:
        LoginPage(context.page).open(Config.BASE_URL)
        LoginPage(context.page).dismiss_popup_if_present()

        # When the session is still valid the guest URL redirects straight to
        # the dashboard and there is no "Get Started" button - so treat a
        # missing button as "already logged in" instead of waiting it out.
        if not page.is_visible(LoginLocators.GET_STARTED_BUTTON, timeout=5000):
            log.info("Session still authenticated (persona=%s) - skipping full re-login", persona)
            return

        _login(context, persona)
        log.info("Re-login successful (persona=%s)", persona)
    except Exception as error:
        log.error("Re-login failed: %s", error)


def _dismiss_personalize_popup(context):
    """Close the personalize-journey modal. True when it is gone afterwards."""
    page = _page(context)
    if not page.is_visible(PERSONALIZE_POPUP, timeout=1000):
        return True
    page.click_first_visible(PERSONALIZE_POPUP_CLOSE, "personalize-journey popup", timeout=1500)
    page.pause(500)
    return not page.is_visible(PERSONALIZE_POPUP, timeout=1000)


def _student_go_home(context):
    """Return the student to the home dashboard in the SAME tab - no re-login.

    The student scenarios keep a valid session between scenarios, so logging in
    again is both unnecessary and flaky. Navigating to the stored dashboard URL
    lands on home reliably; the header check afterwards makes sure no leftover
    modal or half-loaded SPA view is covering the Accounts menu, which would
    otherwise turn one broken scenario into a run of "menu not clickable"
    failures.
    """
    from pages.student_persona.student_persona_page import StudentPersonaPage

    page = _page(context)
    url = StudentPersonaPage.shared_dashboard_url
    if not url:
        base = Config.BASE_URL or ""
        # BASE_URL is the /guest landing; the authenticated dashboard is /home.
        url = base.replace("/guest", "/home") if "/guest" in base else base

    # A previous scenario can leave a stray tab open (courses/pitch/certificate
    # open in one), which would make the next scenario act on a background page.
    page.close_extra_tabs()

    for _ in range(2):
        try:
            page.open_url(url)
        except Exception as error:
            log.warning("Could not navigate to the student home page: %s", error)
            break
        page.pause(1000)
        page.press_escape()
        popup_cleared = _dismiss_personalize_popup(context)
        if popup_cleared and page.is_visible(ACCOUNTS_MENU, timeout=8000):
            return
        # Retry: a fresh navigation also clears a stuck popup.

    log.warning("Student home header not reachable after reload - re-logging in")
    _re_login(context)


def _other_persona_go_home(context):
    """Home reset + re-login recovery for the faculty/RM-style personas."""
    page = _page(context)
    if any(marker in page.current_url() for marker in LOGGED_OUT_URL_MARKERS):
        _re_login(context)
        return

    page.click_first_visible([LoginLocators.HOME_BUTTON], "Home menu", timeout=8000)
    page.wait_for_load("domcontentloaded", timeout=10000)

    # A scenario that died deep in a sub-view can leave the Home button
    # unreachable, so confirm the Accounts menu entry point is really there.
    if not page.is_visible(ACCOUNTS_MENU, timeout=8000):
        _re_login(context)


# ----------------------------------------------------------------------------
# Behave hooks
# ----------------------------------------------------------------------------
def before_all(context):
    """Launch the browser and log in once for the whole run."""
    context.persona = Config.get_persona()
    context.skip_shared_login = _is_newuser_only_run(context)

    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(
        headless=Config.HEADLESS, slow_mo=Config.SLOW_MO, args=BROWSER_ARGS)
    context.context = _new_browser_context(context)
    context.page = context.context.new_page()

    if context.skip_shared_login:
        log.info("New-user-only run detected - skipping the shared persona pre-login "
                 "(this feature registers its own account via a manual email/OTP flow)")
        return

    _login(context, context.persona)
    log.info("Login completed for persona '%s' - ready to run scenarios", context.persona)


def before_feature(context, feature):
    """Start every feature with clean new-user page-object state.

    The new-user page objects keep state on the class (course URL, activity
    frames, active-flow flags) because Behave discards `context` attributes
    between scenarios - that is what lets one registration journey span several
    scenarios. Resetting per feature stops one feature leaking into the next.
    """
    for module_name, class_name in (
        ("pages.Newuser.new_user_page", "NewUserPage"),
        ("pages.Newuser.business_planner_page", "BusinessPlannerPage"),
        ("pages.Newuser.think_activity_page", "ThinkActivityPage"),
    ):
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name).reset_shared_state()
        except Exception as error:
            log.debug("Could not reset %s state: %s", class_name, error)


def before_scenario(context, scenario):
    """Put the browser back on a usable home page, then start tracing."""
    # New-user runs drive navigation from scratch in their own Given step.
    # Their page-object state must survive scenario boundaries, so it is reset
    # per feature (see before_feature) rather than here.
    if getattr(context, "skip_shared_login", False):
        _start_tracing(context)
        return

    # A previous scenario may have crashed the tab; rebuild and re-login so the
    # rest of the run is not lost. A fresh login already lands on home.
    if _page_is_dead(context):
        if _ensure_live_page(context):
            _re_login(context)
        _start_tracing(context)
        return

    _page(context).press_escape()
    if getattr(context, "persona", Config.DEFAULT_PERSONA) == "student":
        _student_go_home(context)
    else:
        _other_persona_go_home(context)

    _start_tracing(context)


def after_step(context, step):
    """On failure, attach a screenshot and the URL so the report is diagnosable."""
    if step.status != "failed":
        return
    try:
        page = getattr(context, "page", None)
        if page is not None and not page.is_closed():
            attach_screenshot(page, f"FAILURE: {step.name}", dedupe=False)
            log.error("Step '%s' failed at URL: %s", step.name, page.url)
    except Exception as error:
        log.error("Could not capture failure screenshot: %s", error)


def after_scenario(context, scenario):
    """Save this scenario's Playwright trace, when tracing is on."""
    if not getattr(context, "trace_enabled", False):
        return
    try:
        traces_dir = os.path.join(os.getcwd(), "reports", "traces")
        os.makedirs(traces_dir, exist_ok=True)
        safe_name = "".join(
            char if char.isalnum() or char in (" ", "-", "_") else "_"
            for char in scenario.name
        ).strip().replace(" ", "_")
        context.context.tracing.stop(path=os.path.join(traces_dir, f"{safe_name}.zip"))
    except Exception as error:
        log.warning("Could not save the scenario trace: %s", error)


def after_all(context):
    """Close the browser once every scenario has run."""
    for closer in ("context", "browser", "playwright"):
        target = getattr(context, closer, None)
        if target is None:
            continue
        try:
            target.stop() if closer == "playwright" else target.close()
        except Exception as error:
            log.debug("Could not close %s: %s", closer, error)
