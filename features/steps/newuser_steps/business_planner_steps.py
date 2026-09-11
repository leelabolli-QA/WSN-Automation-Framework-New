"""Steps for features/newuser.feature > "User validates Business Planner LTI
course and completes all required activities".

The ordinal button step ('the user clicks on the first "Enroll Now" button',
'the ... "Start" button') is NOT defined here: newuser.feature's other scenario
already uses that exact wording and behave's step registry is global, so a
second definition would be an AmbiguousStep error. The single definition lives
in newuser_steps.py and routes to this page object while the BusinessPlanner
flow is active (BusinessPlannerPage.is_active()).
"""

from behave import given, when, then

from pages.Newuser.business_planner_page import BusinessPlannerPage
from utils.config import Config
from utils.helpers import attach_screenshot

_ORDINAL_TO_INT = {"first": 1, "second": 2, "third": 3, "fourth": 4}


def _page(context):
    """Reuse one BusinessPlannerPage for the whole scenario.

    The object tracks state across steps (course content URL, the activity
    iframe, whether the certificate modal appeared) and behave discards context
    attributes at the end of a scenario, so the instance is held on the class
    and reset per feature by environment.py's before_feature.
    """
    context.business_planner_page = BusinessPlannerPage.for_page(context.page)
    return context.business_planner_page


def _flow_page(context):
    """The page object for whichever course flow is currently running.

    newuser.feature's BusinessPlanner-LTI, Dev-Think LTI and Do-LTI scenarios
    share several step wordings (clicking a button/tab/course, 'should be able
    to see the ...', 'should be navigated to the ... page') and behave's step
    registry is global, so one definition has to serve all three. Every page
    object exposes the same method names for these steps, so routing on the
    active flow is all the shared definitions need.
    See ThinkActivityPage.activate().
    """
    # Tolerated while the Do-LTI page object/locators are still being written:
    # an unimportable DoLtiPage just means that flow cannot be the active one,
    # and the BusinessPlanner / Dev-Think scenarios must still route normally.
    try:
        from pages.Newuser.do_lti_page import DoLtiPage
    except ImportError:
        DoLtiPage = None
    if DoLtiPage is not None and DoLtiPage.is_active():
        context.do_lti_page = DoLtiPage.for_page(context.page)
        return context.do_lti_page
    from pages.Newuser.think_activity_page import ThinkActivityPage
    if ThinkActivityPage.is_active():
        context.think_activity_page = ThinkActivityPage.for_page(context.page)
        return context.think_activity_page
    return _page(context)


# ---------- login / navigation ----------

@given('the user is logged into the WSN application')
def user_is_logged_in(context):
    _page(context).verify_logged_in(Config.BASE_URL)


@when('the user clicks on the "{label}" button')
def click_labelled_button(context, label):
    _flow_page(context).click_button(label)
    attach_screenshot(context.page, f"Clicked the '{label}' button")


@when('the user clicks on the "{label}" option')
def click_labelled_option(context, label):
    _page(context).click_option(label)
    attach_screenshot(context.page, f"Clicked the '{label}' option")


@when('the user clicks on the "{label}" tab')
def click_labelled_tab(context, label):
    _flow_page(context).click_tab(label)
    attach_screenshot(context.page, f"Clicked the '{label}' tab")


@when('the user clicks on the "{course_name}" course')
def click_course(context, course_name):
    _flow_page(context).click_course(course_name)
    attach_screenshot(context.page, f"Opened the '{course_name}' course")


@then('the user should be navigated to the {destination} page')
def verify_navigated_to_page(context, destination):
    _flow_page(context).verify_navigated_to(destination)


@then('the user should be navigated back to the course content page')
def verify_back_on_course_content(context):
    _page(context).verify_back_on_course_content()


@then('the user should be navigated to the {activity} activity')
def verify_navigated_to_activity(context, activity):
    _page(context).verify_navigated_to_activity(activity)


# ---------- generic visibility validations ----------
#
# Every "the user should be able to see the ..." line in the scenario resolves
# through one definition; the description is looked up in
# BusinessPlannerPage._VIEW_TARGETS, which fails loudly on an unmapped one
# instead of silently passing.

@then('the user should be able to see the {description}')
def verify_visible(context, description):
    _flow_page(context).verify_visible(description)


# ---------- editing an answer on an already-reviewed plan ----------
#
# BusinessPlanner2 opens on the plan BusinessPlanner1 submitted, where the
# Business Idea is read-only behind an "Edit" button. These steps cover the
# Edit -> confirmation -> "Yes, Edit" -> editable field journey.
#
# "the edit confirmation popup should be displayed" is deliberately NOT of the
# form "the user should be able to see the ..." - that phrasing has a generic
# catch-all definition above and behave's step registry is global, so it would
# be matched by whichever definition happened to be registered first.
#
# Accepting the confirmation reuses the generic 'the user clicks on the
# "{label}" button' step; BusinessPlannerPage.click_button routes "Yes, Edit"
# to the edit-confirmation handler.

@when('the user clicks on the edit button for the Business Idea question')
def click_edit_button(context):
    _page(context).click_edit_button()


@then('the edit confirmation popup should be displayed')
def verify_edit_popup_message(context):
    _page(context).verify_edit_popup_message()


@then('the user should able to see the popup message for the edit button')
def verify_edit_button_popup_message(context):
    _page(context).verify_edit_popup_message()


@then('the user should be able to click on the "Yes, Edit" button')
def click_yes_edit_button(context):
    _page(context).click_button("Yes, Edit")


# ---------- enrollment ----------

@then('the enrollment confirmation popup should be displayed')
def verify_enrollment_popup(context):
    _page(context).verify_enrollment_popup()


@then('the user should be successfully enrolled in the BusinessPlanner-LTI course')
def verify_enrolled(context):
    _page(context).verify_enrolled()


@then('the enrollment success message should be displayed')
def verify_enrollment_success_message(context):
    _page(context).verify_enrolled()


# ---------- certificate name popup ----------
#
# Raised only by the FIRST activity start; the BusinessPlanner2 activity opens
# straight into its content, so these report a skip rather than failing when
# the modal was not shown (see BusinessPlannerPage's module docstring).

@then('the certificate name confirmation popup should be displayed')
def verify_certificate_popup(context):
    _page(context).verify_certificate_popup()


# ---------- answering the activity questions ----------

@when('the user enters the required answer for the Business Idea question')
def enter_business_idea_answer(context):
    _page(context).enter_business_idea_answer()


# Drives the question loop in both activity scenarios: answer whatever
# question is on screen, then let the Then step below confirm it advanced.
@when('the user enters the required answer for each remaining question')
def enter_answer_for_remaining_questions(context):
    _page(context).answer_current_question()
    attach_screenshot(context.page, "Answered the current question")


@then('the answer should be entered successfully')
def verify_answer_entered(context):
    _page(context).verify_answer_entered()


@then('the "Continue" button should be enabled')
def verify_continue_enabled(context):
    _page(context).verify_continue_enabled()


@then('the user should be able to proceed to the next required question')
def verify_proceeded_to_next_required_question(context):
    _page(context).verify_next_question_displayed()


@then('the user should be able to enter the required answer')
def verify_required_answer_field(context):
    _page(context).verify_visible('required answer field')


@then('the next question should be displayed')
def verify_next_question_displayed(context):
    _page(context).verify_next_question_displayed()


@then('the user should be able to continue to the next question')
def verify_can_continue_to_next_question(context):
    _page(context).verify_next_question_displayed()


# ---------- completing an activity ----------

@when('the user completes all the required questions in the {activity} activity')
def complete_all_required_questions(context, activity):
    _page(context).complete_all_required_questions(activity)


@then('all the required questions should be completed')
def verify_all_questions_completed(context):
    _page(context).verify_back_on_course_content()


@then('all the required answers should be submitted successfully')
def verify_answers_submitted(context):
    _page(context).verify_back_on_course_content()


@then('the activity progress should be updated')
def verify_activity_progress_updated(context):
    _page(context).verify_progress_updated()


@then('the overall course progress should be updated')
def verify_overall_progress_updated(context):
    _page(context).verify_progress_updated()


@then('the {activity} activity should be marked as completed')
def verify_activity_marked_completed(context, activity):
    _page(context).verify_activity_completed(activity)
