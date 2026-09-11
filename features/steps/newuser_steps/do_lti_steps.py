"""Steps for features/newuser.feature > the "Do-LTI" scenarios.

Run the WHOLE feature - `behave features/newuser.feature` - not these scenarios
on their own. Do-LTI_QA is a BATCH course: the feature registers a brand-new
account (email and OTP typed in by hand), joins the batch with the job key, and
only then is the course listed under In Progress with both activities unstarted
and the quiz with no attempts.

Only wordings unique to Do-LTI are defined here. Everything it shares with the
Dev-Think LTI scenarios in the same feature - clicking a button, tab, card or
course, "the user should be able to see/validate the ...", the Orientation PDF
and the whole assessment - already has a definition in business_planner_steps.py
or think_activity_steps.py, and behave's step registry is global, so a second
definition would be an AmbiguousStep error. Those single definitions route to
whichever page object owns the flow that is running (DoLtiPage.is_active()).
"""

from behave import given, then, when

from utils.config import Config
from utils.helpers import attach_screenshot

try:
    from pages.Newuser.do_lti_page import DoLtiPage
except ImportError:
    DoLtiPage = None


def _page(context):
    """Reuse one DoLtiPage for the whole feature.

    The object tracks state across steps (the course URL, the activity iframe,
    which activity is being driven) and behave discards context attributes at
    the end of a scenario, so the instance is held on the class and reset per
    feature by environment.py's before_feature.
    """
    if DoLtiPage is None:
        raise RuntimeError(
            "The Do-LTI flow is unavailable because its page object or locators could not be imported."
        )
    context.do_lti_page = DoLtiPage.for_page(context.page)
    return context.do_lti_page


# ---------- login / navigation ----------

@given('the user is enrolled in the Do-LTI batch course')
def user_is_enrolled_in_do_lti(context):
    # Also activates the Do-LTI flow, which is what points the shared step
    # wordings at DoLtiPage for the rest of these scenarios.
    _page(context).verify_logged_in(Config.BASE_URL)


@when('the user opens the Courses page')
def open_courses_page(context):
    _page(context).open_courses_page()
    attach_screenshot(context.page, "Programs & Courses page")


@when('the user opens the Do-LTI course')
def open_do_lti_course(context):
    _page(context).open_course()


# ---------- the Do-LTI activities ----------
#
# Written per activity rather than as one parameterised "both activities" step:
# Do-LTI-1 and Do-LTI-2 are separate LTI launches with their own session and
# their own questions, so the feature file describes each flow in full. The
# implementation behind them is shared - that is where the reuse belongs.

@when('the user opens the {activity} activity')
def open_activity(context, activity):
    _page(context).open_activity(activity)


@when('the user plays the {activity} session')
def play_session(context, activity):
    _page(context).play_session(activity)


@then('the {activity} session should be completed')
def verify_session_completed(context, activity):
    _page(context).verify_session_completed(activity)


@when('the user answers all {count:d} questions in the {activity} activity')
def answer_all_do_questions(context, count, activity):
    _page(context).answer_all_do_questions(count, activity)


@then('all {count:d} questions should be answered')
def verify_all_do_questions_answered(context, count):
    _page(context).verify_all_do_questions_answered(count)


@when('the user finishes the {activity} activity')
def finish_activity(context, activity):
    _page(context).finish_activity(activity)


@then('the {activity} activity should be completed')
def verify_activity_completed(context, activity):
    _page(context).verify_activity_completed(activity)
