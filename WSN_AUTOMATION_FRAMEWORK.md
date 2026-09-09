# WSN Automation Framework

## 1. Overview

The **WSN Automation Framework** is a comprehensive test automation solution designed to automate workflows and user interactions on the WSN (Wadhwani Skilling Network) application. It enables QA teams to:

- **Automate repetitive testing tasks** across multiple user personas (Student, Faculty, Mentor, RM, etc.)
- **Reduce manual testing effort** and improve testing efficiency
- **Support continuous testing** across different environments (dev, prod)
- **Generate detailed reports** with visual dashboards and PDF summaries for stakeholders

The framework uses **Behave** (Behavior-Driven Development) to write tests in plain English (.feature files), making it easy for non-technical team members to understand and contribute.

---

## 2. Framework Structure

| Folder/File | Purpose |
|---|---|
| `features/` | Contains Gherkin test scenarios (.feature files) organized by persona (student.feature, faculty_all.feature, mentor.feature, rm_all.feature, newuser.feature, etc.). Each file defines "Given-When-Then" test cases. |
| `features/steps/` | Python step definitions that implement the behavior described in .feature files. Common steps are in `common_steps/`, persona-specific steps in `student_persona/`, `faculty_steps/`, `rm_steps/`, etc. |
| `features/environment.py` | Behave hooks and setup/teardown logic; initializes browser sessions and cleans up after test runs. |
| `pages/` | Page Object Model (POM) classes. Each page represents a screen/section of the application. `base_page.py` contains common methods; persona-specific pages are in `student_persona/`, `faculty_pages/`, etc. |
| `locators/` | XPath and CSS selectors for UI elements. Organized by persona to match the page structure. Update these when UI elements change. |
| `config/` | Configuration files: `config.yaml` has environment URLs and timeouts; `env_config.py` reads `.env` file values. |
| `.env.example` | Template showing all environment variables needed (credentials, browser settings, log level, environment). Copy to `.env` and fill in real values. `.env` is git-ignored for security. |
| `scripts/` | Utility scripts for generating reports, PDFs, sending emails, and opening trace galleries. |
| `utils/` | Helper modules: `logger.py` for logging, `helpers.py` for common utilities, `report_stats.py` and `executive_report.py` for report generation. |
| `reports/` | Output folder for test reports: `allure-results/` (Allure data), `html-report/` (HTML reports), and generated PDFs. |
| `requirements.txt` | Python dependencies needed to run the framework. |
| `run_tests.py` | Main Python script that orchestrates test runs and report generation. |
| `run-report.ps1` | PowerShell script to run a specific persona's tests and generate reports. |
| `run-combined-report.ps1` | PowerShell script to run all personas across dev and prod, generating a combined dashboard. |
| `behave.ini` | Behave configuration file (currently minimal; can add more settings). |

---

## 3. Technologies Used

- **Python** – Programming language for the framework, page objects, and utilities
- **Playwright** – Browser automation library for cross-browser testing (Chrome, Firefox, Safari)
- **Behave** – BDD framework for writing tests in Gherkin (Given-When-Then) format
- **python-dotenv** – Loads environment variables from `.env` file for secure credential/config management
- **PyYAML** – Parses `config.yaml` for environment-specific settings
- **Allure** – Generates interactive HTML test reports with detailed metrics
- **behave-html-formatter** – Alternative HTML report formatter integrated with Behave
- **ReportLab & Matplotlib** – Generates PDF reports and visual dashboards
- **pdfkit** – Converts HTML to PDF
- **requests** – Makes HTTP calls to Microsoft Graph API for sending email summaries
- **Git/GitHub** – Version control and collaborative development

---

## 4. Environment Setup

Follow these steps to set up the framework on your machine:

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd WSN-Automation-Framework-New
```

### Step 2: Create and Activate Virtual Environment
```bash
# On Windows
python -m venv .venv
.\.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure the `.env` File
```bash
# Copy the example file
cp .env.example .env

# Open .env and fill in the values for your environment
# See section 5 (Configuration) below for details
```

### Step 5: Run a Basic Test
```bash
# Run student persona tests on dev environment
.\run-report.ps1 -Persona student -Env dev

# Or run combined tests (all personas, both dev and prod)
.\run-combined-report.ps1
```

After the run completes, reports are generated in the `reports/` folder. Open the HTML report in your browser to see results.

---

## 5. Configuration

### `.env` File Purpose
The `.env` file stores environment-specific settings and credentials:
- **Credentials** for each persona (username/password pairs)
- **Run configuration** (which environment, persona, browser settings)
- **Logging and tracing options** for debugging

### Environment Variables Explained

**Run Configuration:**
```
ENV=dev                    # Target environment: dev, prod, or qa
PERSONA=student            # Which user persona to test: student, faculty, mentor, rm, career_buddy, institute_admin
HEADLESS=false             # Run browser in headless mode (true/false)
SLOW_MO=0                  # Add delay (ms) between actions for visual debugging (0 = no delay)
TRACE_ON=false             # Record Playwright trace for debugging (true/false)
LOG_LEVEL=INFO             # Logging level: DEBUG, INFO, WARNING, ERROR
```

**Persona Credentials:**
```
STUDENT_USERNAME=<your_student_username>
STUDENT_PASSWORD=<your_student_password>

FACULTY_USERNAME=<your_faculty_username>
FACULTY_PASSWORD=<your_faculty_password>

RM_USERNAME=<your_rm_username>
RM_PASSWORD=<your_rm_password>

MENTOR_USERNAME=<your_mentor_username>
MENTOR_PASSWORD=<your_mentor_password>

CAREER_BUDDY_USERNAME=<your_career_buddy_username>
CAREER_BUDDY_PASSWORD=<your_career_buddy_password>

INSTITUTE_ADMIN_USERNAME=<your_admin_username>
INSTITUTE_ADMIN_PASSWORD=<your_admin_password>

ZOOM_USERNAME=<zoom_sandbox_username>      # For Zoom Connect testing
ZOOM_PASSWORD=<zoom_sandbox_password>
```

**Environment-Specific Overrides:**
You can prefix any variable with the environment name to override it for that environment only:
```
DEV_STUDENT_USERNAME=dev_student_account
PROD_STUDENT_USERNAME=prod_student_account

# When ENV=dev, the framework will use DEV_STUDENT_USERNAME first,
# then fall back to STUDENT_USERNAME if not found.
```

---

## 6. How to Run the Automation

### Run a Single Persona
```bash
# Run student persona tests on dev
.\run-report.ps1 -Persona student -Env dev

# Run faculty persona tests on prod
.\run-report.ps1 -Persona faculty -Env prod

# Run a specific feature file for a persona
.\run-report.ps1 -Persona student -Feature .\features\newuser.feature -Env dev
```

### Run All Personas (Combined Report)
```bash
# Run all personas on both dev and prod
.\run-combined-report.ps1

# Run specific personas only
.\run-combined-report.ps1 -Personas student,faculty,rm

# Run on prod environment only, in headless mode
.\run-combined-report.ps1 -Envs prod -Headless

# Run and send report via email
.\run-combined-report.ps1 -SendEmail

# Preview email without sending
.\run-combined-report.ps1 -DryRunEmail
```

### Commands Reference
| Task | Command |
|---|---|
| Run student tests (dev) | `.\run-report.ps1 -Persona student -Env dev` |
| Run faculty tests (prod) | `.\run-report.ps1 -Persona faculty -Env prod` |
| Run all personas (dev & prod) | `.\run-combined-report.ps1` |
| Run all personas (headless) | `.\run-combined-report.ps1 -Headless` |
| Send report via email | `.\run-combined-report.ps1 -SendEmail` |
| Preview email | `.\run-combined-report.ps1 -DryRunEmail` |

---

## 7. Personas

### What is a Persona?
A **persona** represents a user role or type in the WSN application. Each persona has:
- Different login credentials
- Different workflows and features
- Separate test scenarios (`.feature` files)
- Dedicated page objects and step definitions

### Available Personas
1. **Student** – End user/learner role; primary user persona
2. **Faculty** – Instructor/teacher; manages batches and assessments
3. **Mentor** – Provides guidance and mentoring to students
4. **RM** (Relationship Manager) – Manages batches and enrollment
5. **Career Buddy** – Career guidance role
6. **Institute Admin** – Administrative/system-level access

### How Personas are Configured
- **Credentials:** Stored in `.env` file with `{PERSONA}_USERNAME` and `{PERSONA}_PASSWORD` patterns
- **Test Scenarios:** Each persona has feature files (e.g., `features/student.feature`, `features/faculty_all.feature`)
- **Page Objects & Steps:** Organized in folders like `pages/student_persona/`, `steps/faculty_steps/`, etc.
- **Locators:** UI element locators are in `locators/student_persona/`, `locators/faculty_locators/`, etc.

### Running Tests for a Specific Persona
```bash
# Run student persona
.\run-report.ps1 -Persona student

# Run faculty persona
.\run-report.ps1 -Persona faculty

# Run mentor persona
.\run-report.ps1 -Persona mentor
```

---

## 8. Locators

### Where Locators are Maintained
All UI element locators (XPath, CSS selectors) are maintained in the `locators/` folder:
- `common_locators/` – Shared locators used across multiple pages/personas
- `faculty_locators/` – Faculty-specific UI elements
- `mentor_locators/` – Mentor-specific UI elements
- `rm_locators/` – RM-specific UI elements
- `student_locators/` – Student-specific UI elements
- `student_persona_locators/` – Career Buddy and other persona-specific elements

### What to Do When UI Changes
When the application UI changes:
1. **Identify which locator failed** – Check test logs and error messages
2. **Locate the locator file** – Find the relevant file in `locators/`
3. **Update the XPath/selector** – Use browser DevTools to inspect the new element and copy the updated selector
4. **Update the locator file** – Replace the old selector with the new one

**Example:** If a student login button's locator changes:
- Open `locators/student_locators/login_locators.py`
- Find the `LOGIN_BUTTON` selector
- Use browser DevTools to get the new XPath
- Replace the old XPath with the new one

### How to Validate Changes
1. Run the affected test scenario to verify the fix
2. Run related tests in the same page to ensure no side effects
3. Run the full persona suite if changes impact multiple scenarios

---

## 9. Common Issues & Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| **Locator not found / Element not visible** | UI element changed or locator is outdated | Update the locator in `locators/` folder. Use browser DevTools to find the correct XPath/selector. Re-run the test. |
| **Login fails / Session expires** | Invalid credentials or session timeout | Check `.env` file has correct credentials for the environment. Verify credentials are active in the application. Check network connectivity. |
| **Missing dependencies / Import errors** | `requirements.txt` not installed or virtual environment not activated | Run `pip install -r requirements.txt`. Verify `.venv` is activated. |
| **Script cannot find Python / PowerShell execution policy error** | Python not in PATH or PowerShell script execution disabled | Run PowerShell as Admin. For script policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`. Or run: `powershell -ExecutionPolicy Bypass -File .\run-report.ps1 ...` |
| **Tests pass locally but fail in CI/CD** | Environment configuration difference or missing credentials | Verify `.env` variables are set in CI/CD pipeline. Check base URLs in `config/config.yaml` match the target environment. |
| **Browser crashes / Timeout during test** | Test is too slow or browser resource issues | Increase `timeout` in `config/config.yaml`. Check for network issues. Close other applications consuming resources. |
| **Report not generated** | Test run failed before report generation or missing report dependencies | Check test logs for errors. Verify all dependencies installed (`pip install -r requirements.txt`). Check `reports/` folder has write permissions. |

---

## 10. Debugging Failures

### Step-by-Step Debugging Process

1. **Identify the Failed Test**
   - Note the persona, environment, and feature name from the failed run
   - Example: "Student persona, dev environment, student.feature"

2. **Check the Test Logs**
   - Open the HTML report in `reports/html-report/`
   - Look for the failed scenario and read the error message
   - Check the console output for stack traces or browser errors

3. **Classify the Issue**
   - **Locator issue:** "Element not found" or "Locator timed out"
   - **Data issue:** "Expected value X but found Y"
   - **Environment/Config issue:** Wrong URL, invalid credentials, missing setup
   - **Application issue:** Actual bug in the WSN application (not automation)

4. **Fix the Issue**
   - **Locator:** Update the selector in the relevant `locators/` file
   - **Data:** Check test data, configuration, or API state
   - **Environment:** Verify `.env` settings and `config/config.yaml` URLs
   - **Application:** Report to development team

5. **Re-run the Affected Scenario**
   ```bash
   # Run just the failing feature
   .\run-report.ps1 -Persona student -Feature .\features\student.feature -Env dev
   ```

6. **Run Related Tests**
   - Re-run other tests in the same feature file to ensure no side effects
   - Example: If login fails, run all newuser scenarios

7. **Run Full Suite (if needed)**
   ```bash
   # Run complete persona suite
   .\run-report.ps1 -Persona student -Env dev
   ```

### Useful Debugging Features
- **Trace Recording:** Set `TRACE_ON=true` in `.env` to record Playwright traces for detailed debugging
- **Slow Motion:** Set `SLOW_MO=500` in `.env` to add 500ms delay between actions (helps spot UI issues)
- **Log Level:** Set `LOG_LEVEL=DEBUG` in `.env` for verbose logging
- **Headless Mode:** Set `HEADLESS=false` in `.env` to see the browser during test execution

---

## 11. Best Practices

1. **Do Not Hardcode Credentials**
   - Always use `.env` file for usernames, passwords, and sensitive data
   - Never commit real credentials to Git
   - Use different credentials for dev vs. prod environments

2. **Keep Locators Maintainable**
   - Use stable XPaths (e.g., by ID or data-attributes) rather than brittle ones (e.g., nth-child)
   - Add comments in locator files explaining complex or non-obvious selectors
   - Centralize common locators in `common_locators/` to avoid duplication
   - Review and update locators regularly as UI evolves

3. **Follow the Existing Framework Structure**
   - Keep persona-specific code in appropriate folders (`faculty_pages/`, `student_persona/`, etc.)
   - Use Page Object Model (POM) – create page classes with reusable methods
   - Keep step definitions simple and focused on one action
   - Don't mix concerns (don't add DB queries in step definitions)

4. **Do Not Push Unnecessary Changes**
   - Don't commit debug prints, commented-out code, or temporary fixes
   - Clean up `.env` backups or local test data before committing
   - Review all changes before pushing to ensure quality

5. **Validate Changes Before Pushing**
   - Run affected tests locally to ensure they pass
   - Run the full persona suite for that persona
   - Test on both dev and prod if changes impact shared code

6. **Keep Scripts Reusable**
   - Write helper methods in `utils/helpers.py` for common operations
   - Avoid hardcoding values (URLs, timeouts, wait times)
   - Use the existing base classes and utilities instead of duplicating code

---

## 12. Git Workflow

### Basic Workflow for Updates

1. **Pull Latest Changes**
   ```bash
   git pull origin main
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/update-student-login-tests
   ```

3. **Make Your Changes**
   - Update locators, add new steps, create new page objects, etc.
   - Test your changes locally (see section 6 for run commands)

4. **Test Locally**
   ```bash
   # Activate virtual environment
   .\.venv\Scripts\activate

   # Run the affected persona
   .\run-report.ps1 -Persona student -Env dev

   # Verify the report passes
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Fix: Update student login locators for new UI"
   ```

6. **Push to Remote**
   ```bash
   git push origin feature/update-student-login-tests
   ```

7. **Create a Pull Request**
   - Go to GitHub and create a PR from your branch to `main`
   - Add a description of your changes
   - Link any related issues or tickets
   - Request review from team members

### Commit Message Best Practices
- Use clear, descriptive messages: `Fix: Update faculty locators`, `Add: New career guidance scenarios`
- Reference issue/ticket numbers if applicable: `Fix: Update login flow (Issue #123)`
- Keep commits focused: One feature or fix per commit, not multiple unrelated changes

---

## 13. Quick Reference

| Task | Command / Action | Notes |
|---|---|---|
| **Setup** | `python -m venv .venv` → `.\.venv\Scripts\activate` → `pip install -r requirements.txt` | Do this first on a new machine |
| **Configure** | Copy `.env.example` to `.env` and fill in credentials | Never commit `.env` to Git |
| **Run student tests** | `.\run-report.ps1 -Persona student -Env dev` | Outputs report to `reports/` |
| **Run all personas** | `.\run-combined-report.ps1` | Runs all personas on dev and prod |
| **Run in headless mode** | `.\run-combined-report.ps1 -Headless` | No browser window shown (faster) |
| **View report** | Open `reports/html-report/index.html` in browser | HTML dashboard with test results |
| **Update a locator** | Edit file in `locators/` → Test → Commit | Use browser DevTools to inspect elements |
| **Add a new test** | Create scenario in `.feature` file → Implement steps → Run & validate | Use Gherkin syntax (Given-When-Then) |
| **Debug a failure** | Set `TRACE_ON=true` and `SLOW_MO=500` in `.env` → Run test → Check trace | Helps identify why test failed |
| **Submit changes** | `git commit` → `git push` → Create PR | Always test locally first |
| **Install new package** | `pip install <package>` → Add to `requirements.txt` → Commit | Document any new dependencies |
| **Check test status** | View `reports/allure-results/` or `html-report/` | Allure provides detailed metrics |

---

## 14. Additional Resources

- **Behave Documentation:** https://behave.readthedocs.io/
- **Playwright Documentation:** https://playwright.dev/python/
- **Allure Report:** https://docs.qameta.io/allure/
- **XPath Tutorial:** https://www.w3schools.com/xml/xpath_intro.asp

---

**Last Updated:** 2026-09-07

**Framework Version:** WSN Automation Framework (Behave + Playwright)

**For Questions or Issues:** Reach out to the QA team or refer to the project's CONTRIBUTING.md guide.
