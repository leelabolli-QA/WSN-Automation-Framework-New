from locators.student_persona_locators.career_buddy_locators import CareerBuddyLocators
from pages.base_page import LONG_TIMEOUT, SHORT_TIMEOUT
from pages.student_persona.student_persona_page import CARD_TIMEOUT, StudentPersonaPage
from utils.logger import log

# The mentor the Career Buddy scenario books with. "Anand" exists on prod;
# on dev this account is absent, so a dev run needs a mentor that exists there
# (e.g. "Leela") or the search returns no mentors at all.
MENTOR_NAME = "Anand"
SESSION_OUTCOME = "I need help in identifying right path"



class CareerBuddyPage(StudentPersonaPage):
    """Career Buddy: filter mentors, open a profile and book a session."""


    def click_career_buddy_card(self):
        self.click(CareerBuddyLocators.CAREER_BUDDY_CARD, "Career Buddy card", timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Mentor filters - all four share the same open/select/apply shape
    # ------------------------------------------------------------------
    def _apply_filter(self, filter_button, option, description):
        self.click(filter_button, f"{description} filter", timeout=CARD_TIMEOUT)
        self.click(option, f"{description} option")
        self.click(CareerBuddyLocators.APPLY_BUTTON, f"Apply on the {description} filter")

    def close_filter_popup(self, description):
        """Assert the filter popup is dismissed after applying it.

        Applying usually closes the modal on its own; when it does not, it is
        closed here. Either way the scenario ends up asserting that the popup
        is gone, which is what the old positional-SVG click was really for.
        """
        if self.is_visible(CareerBuddyLocators.FILTER_MODAL, timeout=SHORT_TIMEOUT):
            if not self.click_first_visible([CareerBuddyLocators.FILTER_MODAL_CLOSE],
                                            f"{description} filter close button",
                                            timeout=SHORT_TIMEOUT):
                self.press_escape()
            self.pause(500)
        assert not self.is_visible(CareerBuddyLocators.FILTER_MODAL, timeout=SHORT_TIMEOUT),             f"{description} filter popup did not close"
        log.info("%s filter popup is closed", description)

    def click_language_close_button(self):
        self.close_filter_popup("Language")

    def click_sector_close_button(self):
        self.close_filter_popup("Sector")

    def click_location_close_button(self):
        self.close_filter_popup("Location")

    def click_job_role_close_button(self):
        self.close_filter_popup("Job Role")

    def click_language_dropdown_and_apply(self):
        self._apply_filter(CareerBuddyLocators.LANGUAGE_BUTTON,
                           CareerBuddyLocators.LANGUAGE_OPTION_ENGLISH, "Language")


    def click_sector_dropdown_and_apply(self):
        self._apply_filter(CareerBuddyLocators.SECTOR_BUTTON,
                           CareerBuddyLocators.SECTOR_OPTION_HEALTHCARE, "Sector")


    def click_location_dropdown_and_apply(self):
        self._apply_filter(CareerBuddyLocators.LOCATION_BUTTON,
                           CareerBuddyLocators.LOCATION_OPTION_BENGALURU, "Location")


    def click_job_role_dropdown_and_apply(self):
        self._apply_filter(CareerBuddyLocators.JOBROLE_BUTTON,
                           CareerBuddyLocators.JOBROLE_OPTION_SALES_ASSOCIATE, "Job Role")


    # ------------------------------------------------------------------
    # Mentor profile
    # ------------------------------------------------------------------
    def search_mentor_and_fill_details(self):
        """Search the mentor listing for the scenario's mentor."""
        self.validate_visible(CareerBuddyLocators.MENTOR_CARD, "mentor listing", timeout=30000)
        self.enter_text(CareerBuddyLocators.SEARCH_MENTORS_INPUT, MENTOR_NAME,
                        "mentor search box")
        self.pause(3000)
        assert self.count(CareerBuddyLocators.MENTOR_CARD) > 0, (
            f"Searching for mentor '{MENTOR_NAME}' returned no results - check the mentor "
            f"exists on this environment and matches the filters the scenario applied")

    def click_recommended_mentor_card(self):
        """Open the searched mentor's profile from the filtered listing."""
        self.validate_visible(CareerBuddyLocators.MENTOR_CARD,
                              f"mentor card for '{MENTOR_NAME}'", timeout=25000)
        listed = self.get_text(CareerBuddyLocators.MENTOR_NAME)
        assert MENTOR_NAME.lower() in listed.lower(), (
            f"Search for '{MENTOR_NAME}' listed '{listed}' instead")
        self.click(CareerBuddyLocators.VIEW_PROFILE_BUTTON,
                   f"View Profile for '{MENTOR_NAME}'", timeout=CARD_TIMEOUT)
        log.info("Opened the mentor profile for '%s'", MENTOR_NAME)

    def validate_sector_jobrole_language_details(self):
        self.validate_visible(CareerBuddyLocators.VALIDATE_SECTORS_HEADER,
                              "Sectors header on the mentor profile", timeout=CARD_TIMEOUT)
        self.validate_visible(CareerBuddyLocators.VALIDATE_JOB_ROLES_HEADER,
                              "Job Roles header on the mentor profile", timeout=CARD_TIMEOUT)
        self.validate_visible(CareerBuddyLocators.VALIDATE_LANGUAGE_HEADER,
                              "Language header on the mentor profile", timeout=CARD_TIMEOUT)

    # ------------------------------------------------------------------
    # Booking a session
    # ------------------------------------------------------------------
    def click_book_session_button(self):
        self.click(CareerBuddyLocators.BOOK_SESSION_BUTTON, "Book Session button",
                   timeout=CARD_TIMEOUT)

    def select_available_date_and_slot(self):
        """Pick the first calendar date that actually exposes a time slot."""
        self.wait_for_visible(CareerBuddyLocators.AVAILABLE_SELECT_DATE, timeout=CARD_TIMEOUT)
        dates = self.page.locator(CareerBuddyLocators.AVAILABLE_SELECT_DATE)

        for index in range(dates.count()):
            dates.nth(index).click(force=True)
            if self.is_visible(CareerBuddyLocators.SLOT_BUTTON, timeout=SHORT_TIMEOUT):
                log.info("Slots found on date index %d", index)
                self.click(CareerBuddyLocators.SLOT_BUTTON, "available time slot")
                return
            log.info("No slots on date index %d - trying the next date", index)

        raise AssertionError("No available slots found on any date in the calendar")

    def click_session_purpose_and_select_job_search_strategy(self):
        self.validate_visible(CareerBuddyLocators.SESSION_PURPOSE_LABEL, "Session purpose label",
                              timeout=CARD_TIMEOUT)
        self.wait_for_visible(CareerBuddyLocators.SESSION_PURPOSE_SELECT, state="attached")
        self.element(CareerBuddyLocators.SESSION_PURPOSE_SELECT).evaluate(
            "el => el.querySelector('.ant-select-selector').click()")
        self.click(CareerBuddyLocators.JOB_SEARCH_STRATEGY_OPTION, "Job Search Strategy option")

    def fill_specific_outcome_and_book(self):
        self.validate_visible(CareerBuddyLocators.SPECIFIC_OUTCOME_LABEL, "Specific outcome label",
                              timeout=CARD_TIMEOUT)
        self.wait_for_visible(CareerBuddyLocators.SPECIFIC_OUTCOME_TEXTAREA, state="attached")
        self.element(CareerBuddyLocators.SPECIFIC_OUTCOME_TEXTAREA).fill(SESSION_OUTCOME, force=True)
        log.info("Entered the specific outcome for the session")

        self.click(CareerBuddyLocators.CHECKBOX_OPTION, "confirmation checkbox",
                   state="attached", force=True)
        self.click(CareerBuddyLocators.BOOK_BUTTON, "Book button")

    def click_copy_link_and_validate(self):
        self.click(CareerBuddyLocators.COPY_LINK_OPTION, "Copy Link option", timeout=CARD_TIMEOUT)
        self.validate_visible(CareerBuddyLocators.COPY_LINK_OPTION, "copied meeting link",
                              timeout=LONG_TIMEOUT)
