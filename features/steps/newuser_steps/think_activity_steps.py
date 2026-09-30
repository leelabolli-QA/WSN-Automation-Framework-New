"""Steps for features/newuser.feature > "User validates Dev-Think LTI course,
completes Think activities and assessment".

Run the WHOLE feature - `behave features/newuser.feature` - not this scenario
on its own. The feature's first scenario registers a brand-new account (the
email and the OTP are typed into the browser by hand) and this scenario
continues as that user, which is the only way the course is untouched: enrolled
fresh, both Think activities unstarted and the quiz with no attempts. There is
no fallback to a saved login, so running it alone fails on the Given.

Only wordings unique to this scenario are defined here. The ones it shares with
the BusinessPlanner-LTI scenario in the same feature - clicking a button, tab or
course, 'the user should be able to see the ...' and 'the user should be
navigated to the ... page' - already have a definition in
business_planner_steps.py, and behave's step registry is global, so a second
definition would be an AmbiguousStep error. Those single definitions route to
whichever page object owns the flow that is running (ThinkActivityPage.is_active()).
"""

from behave import given, then, when

from pages.Newuser.think_activity_page import ThinkActivityPage
from utils.config import Config
from utils.helpers import attach_screenshot


def _think_page(context):
    """Reuse one ThinkActivityPage for the whole scenario.

    The object tracks state across steps (course URL, the two activity iframes,
    the assessment's own tallies) and behave discards context attributes at the
    end of a scenario, so the instance is held on the class and reset per
    feature by environment.py's before_feature.
    """
    context.think_activity_page = ThinkActivityPage.for_page(context.page)
    return context.think_activity_page


def _page(context):
    """The page object for whichever LTI course flow is currently running.

    newuser.feature's Dev-Think and Do-LTI scenarios share every wording in
    this file that is not about a Think activity by name - the Explore cards,
    the "validate ..." checks, the Orientation PDF and the whole Moodle
    assessment - and behave's step registry is global, so one definition has to
    serve both. DoLtiPage subclasses ThinkActivityPage, so the shared steps
    below need nothing more than routing on the active flow.
    See ThinkActivityPage.activate().
    """
    # Tolerated while the Do-LTI page object/locators are still being written:
    # an unimportable DoLtiPage just means that flow cannot be the active one,
    # and the Dev-Think scenarios must still route to their own page object.
    try:
        from pages.Newuser.do_lti_page import DoLtiPage
    except ImportError:
        DoLtiPage = None
    if DoLtiPage is not None and DoLtiPage.is_active():
        context.do_lti_page = DoLtiPage.for_page(context.page)
        return context.do_lti_page
    return _think_page(context)


# ---------- login / navigation ----------

@given('the user is successfully logged into the WSN application')
def user_is_successfully_logged_in(context):
    # Pinned to the Dev-Think page object: this Given is what ACTIVATES that
    # flow, so it must not route through whichever flow ran before it.
    _think_page(context).verify_logged_in(Config.BASE_URL)


@then('the user should be able to see all {count:d} cards under "{section}"')
def verify_explore_cards(context, count, section):
    _page(context).verify_explore_cards(count, section)


@when('the user clicks on the "{label}" card')
def click_card(context, label):
    _page(context).click_card(label)
    attach_screenshot(context.page, "Clicked the '%s' card" % label)


# ---------- validations ----------
#
# The variant carrying an expected value is registered FIRST: behave returns
# the first registered definition that matches, and the greedy '{description}'
# of the one below would otherwise also swallow '... as "2 hours"'.

@then('the user should be able to validate the {description} as "{expected}"')
def validate_value(context, description, expected):
    _page(context).validate_value(description, expected)


@then('the user should be able to validate the {description}')
def validate(context, description):
    _page(context).validate(description)


# ---------- enrollment ----------

@when('the user clicks on the "{label}" button in the popup')
def click_popup_button(context, label):
    _page(context).click_popup_button(label)
    attach_screenshot(context.page, "Clicked the '%s' button in the popup" % label)


@then('the user should be successfully enrolled in the course')
def verify_enrolled(context):
    _page(context).verify_enrolled()


# ---------- Orientation ----------

@when('the user completes the Orientation PDF')
def complete_orientation(context):
    _page(context).complete_orientation()


# ---------- Think activities ----------

@when('the user clicks on the "{label}" button for the {section} activity')
def click_activity_start(context, label, section):
    # The feature names the section ("Dev think LTI"); its first activity card
    # is "think 1", which is what actually carries the Start button.
    _think_page(context).open_think_activity("think 1", section=section)


@when('the user selects the correct answer for Think {number:d}')
def select_correct_think_answer(context, number):
    _think_page(context).answer_think_activity(number)


@when('the user answers the Think {number:d} question')
def answer_think_question(context, number):
    page = _think_page(context)
    page.open_think_activity("think %d" % number)
    page.answer_think_activity(number)


@then('the user should be able to access "{activity_name}"')
def verify_can_access_activity(context, activity_name):
    _page(context).verify_can_access(activity_name)


# ---------- assessment ----------

@then('the user should be able to proceed to the Assessment section')
def proceed_to_assessment(context):
    _page(context).open_assessment_section()


@then('the user should be able to start the assessment')
def verify_assessment_started(context):
    _page(context).verify_assessment_started()


@then('the user should be able to see {count:d} questions')
def verify_question_count(context, count):
    _page(context).verify_question_count(count)


@when('the user answers all {count:d} questions')
def answer_all_questions(context, count):
    _page(context).answer_all_questions(count)


# Answering and paging are one loop (Moodle's Next saves the page before it
# advances), so these corroborate what answer_all_questions already did rather
# than driving the attempt themselves.
@when('the user clicks on the "Next" button for each question')
def verify_next_clicked_for_each_question(context):
    _page(context).verify_clicked_next_for_each_question()


@then('the user should be navigated to the next question')
def verify_navigated_to_next_question(context):
    _page(context).verify_navigated_to_next_question()


@then("the user's answer should be saved")
def verify_answers_saved(context):
    _page(context).verify_answers_saved()


@when('the user completes all {count:d} questions')
def complete_all_questions(context, count):
    _page(context).complete_all_questions(count)


@then('the user should be navigated back to the Assessment page')
def verify_back_on_assessment(context):
    _page(context).verify_back_on_assessment()


@when('the user clicks on the Assessment back arrow button')
def click_assessment_back_arrow(context):
    _page(context).click_assessment_back_arrow()


@then('the user should be able to download the "Microcertificate" and click on the "share certificate" button and paste it in new tab')
def download_and_share_microcertificate(context):
    _page(context).download_microcertificate_and_share()
