from behave import given, when, then
from pages.Newuser.new_user_page import NewUserPage
from utils.config import Config
from utils.helpers import attach_screenshot

_ORDINAL_TO_INT = {"first": 1, "second": 2, "third": 3, "fourth": 4}


def _get_page(context):
    """Reuse one NewUserPage instance for the whole feature.

    The page object tracks state across steps (e.g. self._self_serve_frame,
    self._course_content_url) - a fresh instance per step would silently lose
    all of that between steps. behave also discards context attributes when a
    scenario ends, so the instance is held on NewUserPage itself and reset per
    feature by environment.py's before_feature; that lets a new-user journey
    split across scenarios (newuser_prod.feature) keep its state.
    """
    context.new_user_page = NewUserPage.for_page(context.page)
    return context.new_user_page


@given('the user opens the WSN application')
def open_wsn_application(context):
    new_user_page = _get_page(context)
    new_user_page.open_application(Config.BASE_URL)
    attach_screenshot(context.page, "WSN Application Opened")


@when('the user clicks on "{label}"')
def click_labelled_button(context, label):
    new_user_page = _get_page(context)
    new_user_page.click_button_by_label(label)
    attach_screenshot(context.page, f"Clicked '{label}'")


# Same handler registered for Then as well: newuser_prod.feature writes
# 'And the user clicks on "Enroll"' after a Then, and behave matches on the
# step's inherited keyword - the When definition above would not be found there.
@then('the user clicks on "{label}"')
def click_labelled_button_then(context, label):
    click_labelled_button(context, label)


@when('the user clicks on accounts menu')
def click_accounts_menu(context):
    _get_page(context).click_accounts_menu()


# "Join a batch" and "Enroll" are clicked through the generic
# 'the user clicks on "{label}"' step above; only the code entry and the
# outcome need their own wording.

# Registered for both keywords: newuser.feature writes it as a When (the action
# it is), newuser_prod.feature as a Then, and behave matches on the step's
# keyword - one decorator would leave the other feature with an undefined step.
@when('user enters the job code in the input field')
@then('user enters the job code in the input field')
def enter_job_code(context):
    _get_page(context).enter_job_code()


@then('the "Join a batch" card should be displayed')
def verify_join_a_batch_card_displayed(context):
    _get_page(context).verify_join_a_batch_element("card")


@then('the job code input field should be displayed')
def verify_job_code_field_displayed(context):
    _get_page(context).verify_join_a_batch_element("code field")


@then('the "Enroll" button should be displayed')
def verify_enroll_button_displayed(context):
    _get_page(context).verify_join_a_batch_element("Enroll button")


@then('the user should be enrolled successfully')
def verify_batch_enrollment(context):
    _get_page(context).verify_batch_enrollment()


@when('the user clicks on the {ordinal} "{label}" button')
def click_ordinal_labelled_button(context, ordinal, label):
    # newuser.feature's BusinessPlanner-LTI scenario uses this exact wording too
    # ("the first 'Enroll Now' button", "the second 'Start' button") and behave's
    # step registry is global, so a second definition would be an AmbiguousStep
    # error - this one definition routes to whichever page object owns the flow
    # that is currently running.
    from pages.Newuser.business_planner_page import BusinessPlannerPage
    if BusinessPlannerPage.is_active():
        BusinessPlannerPage.for_page(context.page).click_ordinal_button(label, _ORDINAL_TO_INT[ordinal])
    else:
        _get_page(context).click_ordinal_button(label, _ORDINAL_TO_INT[ordinal])
    attach_screenshot(context.page, f"Clicked the {ordinal} '{label}' button")


@when('the user enters a valid email address manually')
def enter_email_manually(context):
    new_user_page = _get_page(context)
    new_user_page.enter_email_manually()


@when('the user enters the OTP manually')
def enter_otp_manually(context):
    new_user_page = _get_page(context)
    new_user_page.enter_otp_manually()


@when('the user completes the registration form')
def complete_registration_form(context):
    new_user_page = _get_page(context)
    new_user_page.complete_registration_form()


@then('the user should be registered successfully')
def verify_registration_successful(context):
    new_user_page = _get_page(context)
    new_user_page.verify_registration_successful()


@then('the user should reach the application')
def verify_application_reached(context):
    new_user_page = _get_page(context)
    new_user_page.verify_application_reached()


# newuser_prod.feature's own wording for the step above (it validates the same
# thing - the authenticated home page rendered after registration).
@then('the application home page should be displayed')
def verify_home_page_displayed(context):
    _get_page(context).verify_application_reached()


@then('the Courses page should be displayed')
def verify_courses_page_displayed(context):
    new_user_page = _get_page(context)
    new_user_page.verify_courses_page_displayed()


@then('the "{course_name}" course should be available')
def verify_course_available(context, course_name):
    new_user_page = _get_page(context)
    new_user_page.verify_course_available(course_name)


@then('the course content should be displayed')
def verify_course_content_displayed(context):
    new_user_page = _get_page(context)
    new_user_page.verify_course_content_displayed()


@then('the {ordinal} self-serve activity should be started successfully')
def verify_self_serve_activity_started(context, ordinal):
    new_user_page = _get_page(context)
    new_user_page.verify_self_serve_activity_started(_ORDINAL_TO_INT[ordinal])


@when('the user selects the "{course_name}" course')
def select_course(context, course_name):
    new_user_page = _get_page(context)
    new_user_page.select_course(course_name)
    attach_screenshot(context.page, f"Selected '{course_name}' course")


@then('the course should be enrolled successfully')
def verify_course_enrolled(context):
    new_user_page = _get_page(context)
    new_user_page.verify_course_enrolled()


@when('the user opens the "{label}"')
def open_labelled_section(context, label):
    new_user_page = _get_page(context)
    new_user_page.open_labelled_section(label)
    attach_screenshot(context.page, f"Opened '{label}'")


@when('the user completes all the required activities')
def complete_required_activities(context):
    new_user_page = _get_page(context)
    new_user_page.complete_required_activities()


@then('all Try Activity tasks should be completed successfully')
def verify_try_activity_completed(context):
    new_user_page = _get_page(context)
    new_user_page.verify_try_activity_completed()


@when('the user clicks on the factory and production work')
def click_factory_and_production_work(context):
    new_user_page = _get_page(context)
    new_user_page.click_factory_and_production_work()
    attach_screenshot(context.page, "Clicked 'Factory & Production Work'")


@when('the user selects any job category or selects a random job role')
def select_job_category_or_random_role(context):
    new_user_page = _get_page(context)
    new_user_page.select_job_category_or_random_role()
    attach_screenshot(context.page, "Job category / random job role selected")


@when('the user answers all the available questions')
def answer_available_questions(context):
    new_user_page = _get_page(context)
    new_user_page.answer_available_questions()
    attach_screenshot(context.page, "Answered all available questions")


@then('the {ordinal} self-serve activity should be completed successfully')
def verify_self_serve_activity_completed(context, ordinal):
    new_user_page = _get_page(context)
    new_user_page.verify_self_serve_activity_completed(_ORDINAL_TO_INT[ordinal])


# ---------------------------------------------------------------------------
# Negative paths (features/newuser.feature > the "@negative" block)
#
# Each definition below is the mirror image of a positive step already in this
# file: the same screen, driven with the invalid input instead of the valid one.
# The wordings are deliberately NOT of the form "the user should be able to see
# the ..." / "the user should be navigated to the ... page" - those are generic
# catch-all definitions in business_planner_steps.py and behave's step registry
# is global, so reusing that phrasing here would either be an AmbiguousStep
# error or silently route a new-user check into the BusinessPlanner page object.
# ---------------------------------------------------------------------------


@given('the user is signed in to the WSN application')
def user_is_signed_in(context):
    """Make a negative scenario runnable on its own.

    The shared pre-login in environment.py is skipped for newuser-only runs, so
    the scenarios that start from inside the app (invalid batch key) log in with
    the configured student credentials when no session is open. Unlike
    business_planner_steps.py's equivalent Given this does not activate any
    course flow, so it cannot change where the shared ordinal/visibility steps
    route.
    """
    page = context.page
    new_user_page = _get_page(context)
    if page.url in ("about:blank", ""):
        page.goto(Config.BASE_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)

    for locator in ("//button[@aria-label='Accounts menu']", "//h6[text()='Courses']"):
        if new_user_page._is_visible(locator, timeout=8000):
            print("User is already signed in to the WSN application")
            attach_screenshot(page, "Signed in to the WSN application")
            return

    from pages.login_page import LoginPage
    username, password = Config.get_credentials(Config.get_persona())
    login_page = LoginPage(page)
    login_page.open(Config.BASE_URL)
    login_page.dismiss_popup_if_present()
    login_page.click_get_started()
    login_page.click_continue_with_email()
    login_page.login(username, password)
    login_page.wait_for_home_page()
    attach_screenshot(page, "Signed in to the WSN application")


# ----- email step -----

@when('the user enters the email address "{email}"')
def enter_email_address(context, email):
    _get_page(context).enter_email(email)


@when('the user leaves the email address field empty')
def leave_email_empty(context):
    _get_page(context).enter_email("")


@when('the user submits the email address')
def submit_email_address(context):
    # Returns False when "Next" was disabled - that IS the rejection, and the
    # Then step below is what asserts the outcome either way.
    context.email_submitted = _get_page(context).submit_email()


@then('the email address should be rejected')
def verify_email_rejected(context):
    _get_page(context).verify_email_rejected()


@then('the user should not reach the OTP screen')
def verify_otp_screen_not_reached(context):
    _get_page(context).verify_otp_screen_not_reached()


# ----- OTP step -----

@when('the user enters the OTP "{otp}"')
def enter_otp_value(context, otp):
    _get_page(context).enter_otp(otp)


@when('the user submits the OTP')
def submit_otp(context):
    _get_page(context).submit_otp()


@then('the OTP should be rejected')
def verify_otp_rejected(context):
    _get_page(context).verify_otp_rejected()


# ----- password / profile steps -----

@when('the user enters the password "{password}" and the confirm password "{confirm_password}"')
def enter_passwords(context, password, confirm_password):
    # submit_password_step=False stops at the filled password screen so the
    # Then step below owns the submit-and-assert.
    _get_page(context).complete_registration_form(
        password=password, confirm_password=confirm_password, submit_password_step=False
    )


@then('the password should be rejected')
def verify_password_rejected(context):
    _get_page(context).verify_password_rejected()


@then('the user should remain on the password step')
def verify_still_on_password_step(context):
    _get_page(context).verify_still_on_password_screen()


@when('the user completes the registration form without accepting the terms and conditions')
def registration_form_without_terms(context):
    _get_page(context).complete_registration_form(accept_terms=False, accept_privacy=False)


@when('the user completes the registration form without entering the first name')
def registration_form_without_first_name(context):
    _get_page(context).complete_registration_form(first_name="")


@when('the user completes the registration form without selecting the city')
def registration_form_without_city(context):
    _get_page(context).complete_registration_form(select_city=False)


@then('the registration form should not be submitted')
def verify_registration_not_submitted(context):
    _get_page(context).verify_registration_not_submitted()


# ----- join a batch -----

@when('the user enters the job code "{code}"')
def enter_job_code_value(context, code):
    context.job_code = code
    _get_page(context).enter_job_code(code)


@when('the user leaves the job code field empty')
def leave_job_code_empty(context):
    _get_page(context).clear_job_code()


@then('the batch enrollment should be rejected')
def verify_batch_enrollment_rejected(context):
    _get_page(context).verify_batch_enrollment_rejected(getattr(context, "job_code", None))


# ----- shared -----

@then('the "{label}" button should be disabled')
def verify_button_disabled(context, label):
    _get_page(context).verify_button_disabled(label)
