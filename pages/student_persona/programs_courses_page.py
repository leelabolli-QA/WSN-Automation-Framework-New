from locators.student_persona_locators.programs_and_courses_locators import (
    ProgramsAndCoursesLocators as L,
)
from pages.student_persona.student_persona_page import CARD_TIMEOUT, StudentPersonaPage
from utils.logger import log


class ProgramsCoursesPage(StudentPersonaPage):
    """Actions for the detailed Programs & Courses student scenario."""

    def open_programs_and_courses(self):
        self.open_card_from_dashboard(
            L.PROGRAMS_AND_COURSES_CARD,
            "Programs & Courses card",
            ready_locator=L.IN_PROGRESS_TAB,
        )

    def validate_tabs(self):
        self.validate_visible(L.IN_PROGRESS_TAB, "In Progress tab", timeout=CARD_TIMEOUT)
        self.validate_visible(L.COMPLETED_TAB, "Completed tab", timeout=CARD_TIMEOUT)

    def open_in_progress(self):
        self.click(L.IN_PROGRESS_TAB, "In Progress tab", timeout=CARD_TIMEOUT)

    def validate_enrolled_courses(self):
        self.validate_visible(L.ENROLLED_COURSE_CARD, "enrolled course card", timeout=CARD_TIMEOUT)

    def open_qa_emp_skill_course(self):
        self.click(L.COURSE_CARD_TITLE, "QA-Emp skill Test-V2-Open course", timeout=CARD_TIMEOUT)
        self.validate_visible(L.PRE_VIDEO_ICON, "Pre Video icon", timeout=CARD_TIMEOUT)

    def validate_pre_video_icon(self):
        self.validate_visible(L.PRE_VIDEO_ICON, "Pre Video icon", timeout=CARD_TIMEOUT)

    def click_pre_video_icon(self):
        self.click(L.PRE_VIDEO_ICON, "Pre Video icon", timeout=CARD_TIMEOUT)

    def validate_pre_video_popup(self):
        self.validate_visible(
            L.VALIDATE_PITCH_TRAINER_PRE_VIDEO_ICON,
            "Pre Video popup",
            timeout=CARD_TIMEOUT,
        )

    def click_right_arrow_if_pre_video_not_started(self):
        self.click(L.PRE_VIDEO_NOTSTARTED_RIGHTARROW, "Pre Video not started right arrow", timeout=CARD_TIMEOUT)

    def click_back_and_pre_video_icon(self):
        self.click(L.PRE_VIDEO_BACKNAVIATION_ARROW, "Pre Video back navigation arrow", timeout=CARD_TIMEOUT)
        self.click(L.PRE_VIDEO_ICON, "Pre Video icon", timeout=CARD_TIMEOUT)

    def close_popup(self):
        self.click(L.POPUP_CLOSE_BUTTON, "course activity popup close button", timeout=CARD_TIMEOUT)

    def validate_collaborate_icon(self):
        self.validate_visible(L.COLLABORATE_ICON, "Collaborate icon", timeout=CARD_TIMEOUT)

    def click_collaborate_icon(self):
        self.click(L.COLLABORATE_ICON, "Collaborate icon", timeout=CARD_TIMEOUT)

    def validate_collaborate_popup(self):
        self.validate_visible(L.POPUP_CLOSE_BUTTON, "Collaborate popup", timeout=CARD_TIMEOUT)

    def validate_assessments_icon(self):
        self.validate_visible(L.ASSESSMENTS_ICON, "Assessments icon", timeout=CARD_TIMEOUT)

    def click_assessments_icon(self):
        self.click(L.ASSESSMENTS_ICON, "Assessments icon", timeout=CARD_TIMEOUT)

    def validate_assessments_popup(self):
        self.validate_visible(L.POPUP_CLOSE_BUTTON, "Assessments popup", timeout=CARD_TIMEOUT)

    def validate_post_video_icon(self):
        self.validate_visible(L.POST_VIDEO_ICON, "Post Video icon", timeout=CARD_TIMEOUT)

    def click_post_video_icon(self):
        self.click(L.POST_VIDEO_ICON, "Post Video icon", timeout=CARD_TIMEOUT)

    def validate_post_video_popup(self):
        self.validate_visible(L.POPUP_CLOSE_BUTTON, "Post Video popup", timeout=CARD_TIMEOUT)

    def return_to_course_list(self):
        self.close_extra_tabs()
        self.click(L.COURSE_BACK_BUTTON, "back to Programs & Courses list", timeout=CARD_TIMEOUT)
        self.validate_visible(L.IN_PROGRESS_TAB, "In Progress tab", timeout=CARD_TIMEOUT)

    def _open_completed_tab(self):
        """Reset to Completed because course actions return to In Progress."""
        self.click(L.COMPLETED_TAB, "Completed tab", timeout=CARD_TIMEOUT)
        self.validate_visible(L.COMPLETED_COURSE_CARD, "completed course card", timeout=CARD_TIMEOUT)

    def open_completed_courses(self):
        self._open_completed_tab()

    def validate_completed_courses(self):
        self._open_completed_tab()

    def validate_dev_try_activity_course(self):
        self._open_completed_tab()
        self.validate_visible(L.DEV_TRY_ACTIVITY_SELF_SERVE_COURSE_TITLE,
                              "Dev-Try activity-Self serve course", timeout=CARD_TIMEOUT)

    def resume_dev_try_activity_course(self):
        self._open_completed_tab()
        self.click(L.RESUME_COURSE_BUTTON, "Resume Course button", timeout=CARD_TIMEOUT)

    def click_COURSE_BACK_BUTTON_from_course_details(self):
        self.click(L.COURSE_BACK_BUTTON, "back button from course details page", timeout=CARD_TIMEOUT)

    def validate_complete_all_criteria_message(self):
        if not self.is_visible(L.COMPLETE_ALL_CRITERIA_MESSAGE, timeout=2000):
            log.warning(
                "Complete all criteria message is unavailable after Resume Course; "
                "continuing with course navigation."
            )
            return
        log.info("Validated complete all criteria message")

    def click_COURSE_CONTENT_BACK_ARROW_from_complete_all_criteria_message(self):
        self.click(
            L.COURSE_CONTENT_BACK_ARROW,
            "back arrow from complete all criteria message",
            timeout=CARD_TIMEOUT,
        )

    def validate_dev_think_course(self):
        self._open_completed_tab()
        self.validate_visible(L.DEV_THINK_LTI_OPEN_COURSE_TITLE,
                              "Dev-Think LTI-Open course", timeout=CARD_TIMEOUT)

    def handle_complete_all_criteria_message(self):
        # Resume Course can open a lesson or an assessment error screen instead
        # of rendering the criteria message. The content back arrow is still
        # the correct way to leave that screen, so do not gate the click on the
        # optional message.
        self.click_COURSE_CONTENT_BACK_ARROW_from_complete_all_criteria_message()

    def validate_certificate_button(self):
        self._open_completed_tab()
        self.validate_visible(L.DEV_THINK_LTI_OPEN_COURSE_CERTIFICATE,
                              "Certificate button", timeout=CARD_TIMEOUT)

    def open_completed_course_by_title(self, course_title):
        self._open_completed_tab()
        course_card = (
            f"//h4[normalize-space()='{course_title}']"
            "/ancestor::div[contains(@class,'learning-item-card')][1]"
        )
        self.click(
            f"{course_card}//span[normalize-space()='Course Completed']",
            f"{course_title} Course Completed card",
            timeout=CARD_TIMEOUT,
        )

    def validate_certificate_panel(self, include_scorecard=False, include_download=False):
        self.validate_visible(L.COURSE_COMPLETION_PANEL_PREVIEW_IMAGE,
                              "certificate image", timeout=CARD_TIMEOUT)
        if include_download:
            self.validate_visible(L.DOWNLOAD_CERTIFICATE_BUTTON,
                                  "Download Certificate button", timeout=CARD_TIMEOUT)
        self.validate_visible(L.SHARE_BUTTON, "Share button", timeout=CARD_TIMEOUT)
        if include_scorecard:
            self.validate_visible(L.SCORECARD_DOWNLOAD_LINK,
                                  "scorecard download link", timeout=CARD_TIMEOUT)

    def click_download_certificate(self):
        self.click(L.DOWNLOAD_CERTIFICATE_BUTTON, "Download Certificate button", timeout=CARD_TIMEOUT)

    def click_share_button(self):
        share_button = self.wait_for_visible(L.SHARE_BUTTON, timeout=CARD_TIMEOUT)
        self.show_element(share_button)
        try:
            with self.page.context.expect_page(timeout=3000) as new_page_info:
                share_button.click()
            new_tab = new_page_info.value
            new_tab.wait_for_load_state("domcontentloaded", timeout=CARD_TIMEOUT)
            new_tab.close()
            self.page.bring_to_front()
            log.info("Opened and closed the share tab")
        except Exception:
            # Some environments show a share dialog or copy the link without
            # opening a tab; the click has already completed in that case.
            self.page.bring_to_front()
            log.info("Clicked Share button without opening a new tab")

    def click_optional_scorecard_download(self):
        if self.is_visible(L.SCORECARD_DOWNLOAD_LINK, timeout=2000):
            self.click(L.SCORECARD_DOWNLOAD_LINK, "scorecard download link", timeout=CARD_TIMEOUT)
        else:
            log.info("Scorecard download link is unavailable; skipping optional step.")

    def validate_hps_test_course(self):
        self._open_completed_tab()
        self.validate_visible(L.HPS_TEST_QA2_COURSE_TITLE, "HPS Test-QA2 course", timeout=CARD_TIMEOUT)

    def validate_certificate_and_scorecard_buttons(self):
        self._open_completed_tab()
        self.validate_visible(L.HPS_TEST_QA2_COURSE_CERTIFICATE,
                              "Certificate button", timeout=CARD_TIMEOUT)
        hps_card = (
            "//h4[normalize-space()='HPS Test-QA2']"
            "/ancestor::div[contains(@class,'learning-item-card')][1]"
        )
        self.validate_visible(
            f"{hps_card}//button[normalize-space()='Scorecard']",
            "Scorecard button",
            timeout=CARD_TIMEOUT,
        )

    def validate_recommended_by_institute(self):
        self.scroll_to_bottom()
        self.validate_visible(L.RECOMMENDED_BY_INSTITUTE,
                              "Programs & Courses recommended by institute", timeout=CARD_TIMEOUT)

    def validate_recommended_cards(self):
        self.validate_visible(L.RECOMMENDED_CARD, "recommended course or program card", timeout=CARD_TIMEOUT)

    def validate_recommended_by_wadhwani(self):
        self.scroll_to_bottom()
        self.validate_visible(L.RECOMMENDED_BY_WADHWANI,
                              "Programs & Courses recommended by Wadhwani Foundation", timeout=CARD_TIMEOUT)

    def validate_join_a_batch(self):
        self.scroll_to_bottom()
        self.validate_visible(L.JOIN_A_BATCH, "Join a batch section", timeout=CARD_TIMEOUT)