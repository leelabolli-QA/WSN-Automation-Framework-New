"""Step definitions for the detailed Programs & Courses scenario."""

from behave import then, when

from pages.student_persona.programs_courses_page import ProgramsCoursesPage


def _page(context):
    return ProgramsCoursesPage(context.page)


@then("user navigates to Programs & Courses page")
def navigate_to_programs_and_courses(context):
    _page(context).open_programs_and_courses()


@then("user validates the In Progress and Completed tabs")
def validate_tabs(context):
    _page(context).validate_tabs()


@when("user clicks on the In Progress tab")
def click_in_progress(context):
    _page(context).open_in_progress()


@then("user validates the enrolled course cards")
def validate_enrolled_courses(context):
    _page(context).validate_enrolled_courses()


@when('user opens the "QA-Emp skill Test-V2-Open" course')
def open_qa_emp_skill_course(context):
    _page(context).open_qa_emp_skill_course()


@then("user validates the course detail page")
def validate_course_detail_page(context):
    _page(context).validate_pre_video_icon()


@then("user validates the Pre Video icon")
def validate_pre_video_icon(context):
    _page(context).validate_pre_video_icon()


@then("user clicks on the Pre Video icon")
def click_pre_video_icon(context):
    _page(context).click_pre_video_icon()


@then("user validates the Pre Video popup")
def validate_pre_video_popup(context):
    _page(context).validate_pre_video_popup()


@then("user closes the Pre Video popup")
def close_pre_video_popup(context):
    _page(context).close_popup()


@then("user validates the Collaborate icon")
def validate_collaborate_icon(context):
    _page(context).validate_collaborate_icon()


@then("user clicks on the Collaborate icon")
def click_collaborate_icon(context):
    _page(context).click_collaborate_icon()


@then("user validates the Collaborate popup")
def validate_collaborate_popup(context):
    _page(context).validate_collaborate_popup()


@then("user closes the Collaborate popup")
def close_collaborate_popup(context):
    _page(context).close_popup()


@then("user validates the Assessments icon")
def validate_assessments_icon(context):
    _page(context).validate_assessments_icon()


@then("user clicks on the Assessments icon")
def click_assessments_icon(context):
    _page(context).click_assessments_icon()


@then("user validates the Assessments popup")
def validate_assessments_popup(context):
    _page(context).validate_assessments_popup()


@then("user closes the Assessments popup")
def close_assessments_popup(context):
    _page(context).close_assessments_popup()


@then("user validates the Post Video icon")
def validate_post_video_icon(context):
    _page(context).validate_post_video_icon()


@then("user clicks on the Post Video icon")
def click_post_video_icon(context):
    _page(context).click_post_video_icon()


@then("user validates the Post Video popup")
def validate_post_video_popup(context):
    _page(context).validate_post_video_popup()


@then("user closes the Post Video popup")
def close_post_video_popup(context):
    _page(context).close_popup()


@then("user navigates back to the Programs & Courses list")
def return_to_course_list(context):
    _page(context).return_to_course_list()


@when("user clicks on the Completed tab")
def click_completed(context):
    _page(context).open_completed_courses()


@then("user validates the completed course cards")
def validate_completed_courses(context):
    _page(context).validate_completed_courses()


@then("user validates the Dev-Try activity-Self serve course")
def validate_dev_try_activity_course(context):
    _page(context).validate_dev_try_activity_course()


@then("user validates the completed course and clicks on Resume Course option")
def resume_dev_try_activity_course(context):
    _page(context).resume_dev_try_activity_course()


@then("user validates the complete all citeria message")
def validate_complete_all_criteria_message(context):
    _page(context).validate_complete_all_criteria_message()


@then("user validates Dev-Think-Lti-open course")
def validate_dev_think_course(context):
    _page(context).validate_dev_think_course()


@then("user validates certificate button")
def validate_certificate_button(context):
    _page(context).validate_certificate_button()


@then("user clicks on course completed button")
def open_completed_course(context):
    _page(context).open_first_completed_course()


@then("user validates certificate image, download button and share button")
def validate_certificate_panel(context):
    _page(context).validate_certificate_panel()


@then("user validates HPS Test-QA2 course")
def validate_hps_test_course(context):
    _page(context).validate_hps_test_course()


@then("user validates certificate button and scorecard button")
def validate_certificate_and_scorecard_buttons(context):
    _page(context).validate_certificate_and_scorecard_buttons()


@then("user validates certificate image, download certificate button, share button and download score card button")
def validate_certificate_and_scorecard_panel(context):
    _page(context).validate_certificate_panel(include_scorecard=True)


@then("user validates Courses & Programs recommended by institute")
def validate_recommended_by_institute(context):
    _page(context).validate_recommended_by_institute()


@then("user validates the recommended course and program cards")
def validate_recommended_cards(context):
    _page(context).validate_recommended_cards()


@then("user validates Courses & Programs recommended by Wadhwani Foundation")
def validate_recommended_by_wadhwani(context):
    _page(context).validate_recommended_by_wadhwani()


@then("user validates the Join a batch section")
def validate_join_a_batch(context):
    _page(context).validate_join_a_batch()