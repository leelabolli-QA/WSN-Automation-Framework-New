from behave import given, then

from pages.Newuser.student_CA_page import StudentCAPage
from pages.login_page import LoginPage
from pages.student_persona.my_career_advisor_page import MyCareerAdvisorPage
from locators.student_persona_locators.my_career_advisor_locators import MyCareerAdvisorLocators


def _student_ca_page(context) -> StudentCAPage:
    if not hasattr(context, "student_ca_page"):
        context.student_ca_page = StudentCAPage(context.page)
    return context.student_ca_page


@given("user is on homepage")
def step_user_is_on_homepage(context):
    LoginPage(context.page).wait_for_home_page()
    _student_ca_page(context).click_completion_popup_close_button()


@given("user is on Career Advisor page")
def step_user_is_on_career_advisor_page(context):
    if "/career-advisor/" in context.page.url:
        context.student_ca_flow_started = True
        context.student_ca_url = context.page.url
        _student_ca_page(context).click_completion_popup_close_button()
        return
    LoginPage(context.page).wait_for_home_page()
    _student_ca_page(context).click_completion_popup_close_button()
    career_advisor = MyCareerAdvisorPage(context.page)
    career_advisor.capture_dashboard_url()
    context.career_advisor_onboarded = career_advisor.navigate_to_my_career_advisor()
    context.student_ca_flow_started = True
    context.student_ca_url = context.page.url


@then("user validates the CA card in homepage and click on it")
def step_open_career_advisor_from_homepage(context):
    context.career_advisor_onboarded = MyCareerAdvisorPage(
        context.page
    ).navigate_to_my_career_advisor()
    context.student_ca_flow_started = True
    context.student_ca_url = context.page.url


@then("user validates the CA card details in the subsequent page")
def step_validate_career_advisor_page(context):
    career_advisor = MyCareerAdvisorPage(context.page)
    if getattr(context, "career_advisor_onboarded", False):
        career_advisor.validate_header_count()
    else:
        career_advisor.validate_visible(
            MyCareerAdvisorLocators.PASSIONS_HEADER,
            "Career Advisor Passions header",
            timeout=15000,
        )


@then("user clicks on matches roles section")
def step_click_matches_roles_section(context):
    _student_ca_page(context).click_matches_roles_section()


@then("user clicks passions preferences")
def step_click_passions_preferences(context):
    _student_ca_page(context).click_passions_preferences()


@then("user selects the Arts & Design option")
def step_select_arts_and_design_option(context):
    _student_ca_page(context).select_arts_and_design_option()


@then("user clicks review passions preferences")
def step_click_review_passions_preferences(context):
    _student_ca_page(context).click_review_passions_preferences()


@then("user validates the selected items in passions review section")
def step_validate_selected_items_in_passions_review(context):
    _student_ca_page(context).validate_selected_items_in_passions_review()


@then("user click on submit button in passions section")
def step_click_submit_button(context):
    _student_ca_page(context).click_submit_button()


@then("user clicks on questionnaires section")
def step_click_questionnaires_section(context):
    _student_ca_page(context).click_questionnaires_section()


@then("user clicks on interests card in questionnaires section and clicks on reattempt button")
def step_click_interests_card_questionnaire_reattempt(context):
    _student_ca_page(context).open_interests_questionnaire_reattempt()


@then("user clicks on questionnaries choose button and clicks on question cards and click on next button")
def step_choose_questionnaire_and_answer_first(context):
    _student_ca_page(context).choose_questionnaire_and_answer_first_question()


@then("user attempts all the questions in interests section and clicks on next button")
def step_answer_all_interests_questions(context):
    _student_ca_page(context).answer_all_interests_questions()


@then("user clicks start aptitudes and answer all the questions in aptitudes section and clicks on next button")
def step_start_aptitudes_and_answer_all(context):
    _student_ca_page(context).start_aptitudes_and_answer_all()


@then("user clicks on start values and answer all the questions in values section and clicks on next button")
def step_start_values_and_answer_all(context):
    _student_ca_page(context).start_values_and_answer_all()


@then("user clicks on interests card and clicks on reattempt button")
def step_click_interests_card_and_reattempt(context):
    _student_ca_page(context).click_interests_card_and_reattempt()


@then("user clicks on aptitudes card and clicks on reattempt button")
def step_click_aptitudes_card_and_reattempt(context):
    _student_ca_page(context).click_aptitudes_card_and_reattempt()


@then("user clicks on values card and clicks on reattempt button")
def step_click_values_card_and_reattempt(context):
    _student_ca_page(context).click_values_card_and_reattempt()


@then("user slides the slider to 7 or 8 or 8 or 7 and clicks on next button")
def step_slide_slider_and_click_next(context):
    _student_ca_page(context).slide_slider_and_click_next_through_questions()


@then("user clicks on submit button in interests section")
def step_click_submit_interests_section(context):
    _student_ca_page(context).click_submit_questionnaire()


@then("user clicks on submit button in aptitudes section")
def step_click_submit_aptitudes_section(context):
    _student_ca_page(context).click_submit_questionnaire()


@then("user clicks on submit button in values section")
def step_click_submit_values_section(context):
    _student_ca_page(context).click_submit_questionnaire()


@then("user clicks on backarrow button")
def step_click_back_arrow(context):
    _student_ca_page(context).click_back_arrow()


@then("user clicks on review button in aptitudes section")
def step_click_first_aptitudes_review_button(context):
    _student_ca_page(context).complete_aptitudes_first_flow()


@then("user clicks on reattempt")
def step_click_reattempt(context):
    _student_ca_page(context).click_reattempt()


@then("user chooses slider option in aptitudes section")
def step_choose_slider_option_aptitudes(context):
    _student_ca_page(context).choose_slider_option()


@then("user clicks on 1st question and changes the slider value to 9 or 10 and clicks on update")
def step_update_first_slider_value(context):
    _student_ca_page(context).update_first_question_slider_value()


@then("user clicks on Go to matched roles")
def step_click_go_to_matched_roles(context):
    _student_ca_page(context).click_go_to_matched_roles()


@then("user clicks on without college degree and validate the recommended roles")
def step_click_without_college_degree_and_validate_roles(context):
    _student_ca_page(context).click_without_college_degree()
    _student_ca_page(context).validate_recommended_roles()


@then("user clicks on search roles")
def step_click_search_roles(context):
    _student_ca_page(context).click_search_roles()


@then("user enters jobrole and add the first job as add saved")
def step_enter_jobrole_and_add_first_job_as_saved(context):
    job_role = "Automation"
    _student_ca_page(context).enter_jobrole_and_add_first_job_as_saved(job_role)


@then("user clicks on save menu header and validates the saved job")
def step_click_save_menu_header_and_validate_saved_job(context):
    _student_ca_page(context).click_save_menu_header_and_validate_saved_job()


@then("user clicks on compare roles")
def step_click_compare_roles(context):
    _student_ca_page(context).click_compare_roles()


@then("user clicks on first and second checkbox in search results and clicks on compare button")
def step_click_first_second_checkbox_and_compare(context):
    _student_ca_page(context).click_first_second_checkbox_and_compare()


@then("user clicks on share report and click and validates the share report options")
def step_click_share_report_and_validate_options(context):
    _student_ca_page(context).click_share_report_and_validate_options()


@then("user validates self review, matched roles, and favourite roles tabs in share report section")
def step_validate_share_report_tabs(context):
    _student_ca_page(context).validate_share_report_tabs()


@then("user clicks on Saved menu and removes the saved job from favourites")
def step_click_saved_menu_and_remove_saved_job(context):
    _student_ca_page(context).click_saved_menu_and_remove_saved_job()


@then("user clicks on help icon")
def step_click_help_icon(context):
    _student_ca_page(context).click_help_icon()


@then("user clicks on about icon")
def step_click_about_icon(context):
    _student_ca_page(context).click_about_icon()


@then("user logout")
def step_user_logout(context):
    LoginPage(context.page).logout()


# ----------------------------------------------------------------------
# Recommended-role filters, search edge cases, saved roles and About.
# ----------------------------------------------------------------------
@then("user clicks on with college degree and validate the recommended roles")
def step_click_with_college_degree_and_validate_roles(context):
    _student_ca_page(context).click_with_college_degree()
    _student_ca_page(context).validate_recommended_roles()


@then("user compares the recommended roles with and without a college degree")
def step_compare_college_degree_filters(context):
    """The two degree filters must return genuinely different role sets.

    Asserting only that each filter renders *a* count would pass even if the
    toggle did nothing at all, so the counts are captured under both filters
    and compared. The Without filter is re-applied at the end because the
    selection is persisted server-side for the account and would otherwise
    leak into later scenarios and re-runs.
    """
    page = _student_ca_page(context)

    previous = page.get_recommended_role_counts()
    page.click_without_college_degree()
    # click_without_college_degree() returns immediately (no settle wait of
    # its own), so give the re-query the same chance to land.
    without_counts = page.wait_for_role_counts_change(previous)
    assert any(without_counts), "No matched-role counts rendered for 'Without College Degree'"

    page.click_with_college_degree()
    # Read through the settle helper: the previous filter's numbers stay on
    # screen until the re-query lands, and comparing against those made the
    # two filters look identical.
    with_counts = page.wait_for_role_counts_change(without_counts)
    assert any(with_counts), "No matched-role counts rendered for 'With College Degree'"

    assert without_counts != with_counts, (
        "The college-degree filter did not change the recommended roles: "
        f"both returned {without_counts}"
    )

    page.click_without_college_degree()


@then("user validates the why this recommendation option on recommended roles")
def step_validate_why_this_recommendation(context):
    _student_ca_page(context).validate_why_this_recommendation()


@then('user searches for the job role "{job_role}"')
def step_search_for_job_role(context, job_role):
    _student_ca_page(context).search_for_role(job_role)


@then("user validates the search results are returned")
def step_validate_search_results_returned(context):
    _student_ca_page(context).validate_search_results_returned()


@then("user validates no related jobs are found")
def step_validate_no_related_jobs(context):
    _student_ca_page(context).validate_no_related_jobs()


@then("user clears the search input")
def step_clear_search_input(context):
    _student_ca_page(context).clear_search_input()


@then("user validates the saved roles page")
def step_validate_saved_roles_page(context):
    _student_ca_page(context).validate_saved_roles_page()


@then("user validates the about page details")
def step_validate_about_page_details(context):
    _student_ca_page(context).validate_about_page_content()
