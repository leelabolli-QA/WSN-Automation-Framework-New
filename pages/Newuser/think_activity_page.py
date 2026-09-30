"""Page object for the "Dev-Think LTI-Open" course journey.

Drives features/newuser.feature > "User validates Dev-Think LTI course,
completes Think activities and assessment": home -> Courses -> Dev-Think
LTI-Open -> enroll -> Overview validations -> the two Think activities ->
the Assesment quiz -> the Performance tab and its certificate.

Four things about the real course shape this file:

1. THREE documents, not one. The WSN app renders the course pages; the Think
   activities render inside an /en/lti-think-activity iframe; the assessment is
   a Moodle quiz inside an lms.<env>/mod/quiz iframe. Every check declares
   which of the three it belongs to - see _think_frame() / _quiz_frame().

2. The assessment draws a RANDOM five questions from a large bank, so there is
   no fixed answer list to replay and no safe way to guess. _ANSWER_KEY maps
   each question to its correct option and answers are matched on option TEXT,
   because the option ORDER is not stable between attempts. The certificate
   needs a 70% average and the quiz is marked out of 5, so at least 4 of the 5
   must be right - which is why every question is looked up rather than
   answered by position. Anything the key does not recognise is printed with
   the correct answer the review page reveals, so the key can be extended.

3. It runs as a BRAND-NEW user. newuser.feature's first scenario registers one
   through the manual email/OTP flow and this scenario continues as that user,
   which is what makes the fresh-course states real: the Enroll Now popup, a 0%
   score, two unstarted Think activities and a quiz with no attempts.

4. The app interrupts. A deploy landing mid-run raises an "Application update
   is available" modal that unmounts the SPA, and the first activity a user
   ever starts raises a one-time "Review Your Certificate Name" prompt. Both
   are cleared where they appear.
"""

import difflib
import re

from pages.base_page import BasePage
from locators.new_user_locators.think_activity_locators import (
    ThinkActivityLocators as TA,
)
from utils.helpers import attach_screenshot, highlight_element

# How long to give an embedded activity's own content time to render.
ACTIVITY_CONTENT_TIMEOUT_MS = 25000
# Seconds to keep looking for an activity iframe after a Start / Attempt click.
FRAME_POLL_STEPS = 20
# The average score the course requires before it releases the certificate.
CERTIFICATE_PASS_PERCENT = 70


def _norm(text):
    """Collapse whitespace - used before any text comparison."""
    return re.sub(r"\s+", " ", (text or "")).strip()


def _flow_classes():
    """Every page object that can own newuser.feature's shared step wordings.

    Imported lazily: BusinessPlannerPage and DoLtiPage both reach back into
    this module, so importing them at module level would be circular.
    """
    classes = [ThinkActivityPage]
    for module_name, class_name in (
        ("pages.Newuser.business_planner_page", "BusinessPlannerPage"),
        ("pages.Newuser.do_lti_page", "DoLtiPage"),
    ):
        try:
            module = __import__(module_name, fromlist=[class_name])
            classes.append(getattr(module, class_name))
        except Exception:
            pass
    return classes


def _slug(text):
    """Normalised comparison key: lower-case, alphanumerics and spaces only.

    Strips the curly quotes and stray punctuation that differ between how a
    question is written in the bank and how the app renders it.
    """
    return re.sub(r"[^a-z0-9 ]", "", _norm(text).lower())


class ThinkActivityPage(BasePage):

    # ------------------------------------------------------------------
    # Assessment answer key
    # ------------------------------------------------------------------
    # question -> the TEXT of its correct option, harvested from the quiz's own
    # review pages. Looked up with _slug plus a close-match fallback, so small
    # wording changes still resolve.
    _ANSWER_KEY = {
        (
            "Ali is reading a scientific article about climate change. How can he "
            "apply the 'Questioning' technique of effective reading to deepen his "
            "understanding of the topic?"):
            "By generating inquiries to challenge assumptions and clarify concepts.",
        (
            "Anita is reading a descriptive passage about a tropical rainforest. "
            "How can she apply the 'Visualizing' technique of effective reading to "
            "enhance her understanding of the ecosystem described in the passage?"):
            (
                "By creating mental images of the plants and animals mentioned in the "
                "passage."),
        (
            "How can one apply the 'Predicting' technique of effective reading in "
            "real life?"):
            "By anticipating traffic patterns before leaving for work.",
        (
            "How can the 'Evaluating' technique of effective reading be applied in "
            "a professional context?"):
            "By assessing the reliability of information in a research paper.",
        (
            "How can we punctuate the sentence 'Lets eat grandma' to ensure "
            "clarity?"):
            "Let's eat, grandma.",
        "How can you emphasize when you like something very much?":
            "a lot",
        (
            "How does the 'Connecting' technique of effective reading deepen "
            "understanding of the text?"):
            "By relating the text to personal experiences.",
        (
            "How does the verb typically change when referring to an action that "
            "has happened in the past?"):
            "It undergoes a change in tense to indicate past actions.",
        "How should we consider others' preferences?":
            "Respect others’ likes and dislikes",
        "How would someone say they have a strong liking for painting?":
            "I’m crazy about painting.",
        (
            "If Ravi says, \"I adore trekking in the mountains,\" what can be "
            "inferred about his feelings towards trekking?"):
            "He strongly admires trekking.",
        (
            "If someone is talking about an action they plan to do \"next month\", "
            "which tense are they using?"):
            "Future",
        (
            "If you are talking about more than one man, what form of the naming "
            "word should you use?"):
            "Men",
        (
            "If you neither dislike nor have a positive feeling about reading "
            "books, which phrase suits best?"):
            "I don’t mind reading books.",
        (
            "In the sentence \"A man in the shop is buying some biscuits\", what is "
            "the function of the naming word \"man\"?"):
            "To identify a person",
        (
            "In the sentence \"Maria and John are siblings,\" which pronoun can "
            "replace \"Maria and John\"?"):
            "They are siblings.",
        (
            "In the sentence \"Sophia and I went to the park,\" which pronoun can "
            "replace \"Sophia and I\"?"):
            "We",
        (
            "In the sentence, \"The book is on the table, and it is open,\" what "
            "does the pronoun \"it\" refer to?"):
            "The book",
        (
            "In which situation does the form of the verb change but its meaning "
            "remains the same?"):
            "Depending on past, present, or future",
        (
            "Ria wants to improve her language skills and broaden her knowledge "
            "using techniques of effective reading. Which of the following "
            "activities would be most beneficial for achieving her goal?"):
            "Reading books and articles on various subjects.",
        (
            "Sara is reading a news article discussing the effects of social media "
            "on mental health. How can she apply the 'Evaluating' technique of "
            "effective reading to critically assess the information presented in "
            "the article?"):
            (
                "By assessing the reliability and credibility of the sources cited in "
                "the article."),
        "What are naming words also called?":
            "Common Nouns",
        "What can adjectives do in a sentence?":
            "All the given options.",
        (
            "What does the verb express in the sentence \"Rohit studied "
            "yesterday\"?"):
            "An action that happened in the past",
        "Which of the following sentences correctly uses a pronoun?":
            "The cat has a ball. It plays with the ball.",
        "What do verbs express about?":
            "Physical actions, mental actions, and states of being",
        "What do we add to most naming words to make them plural?":
            "s or es",
        "What does the naming word \"clouds\" refer to?":
            "Many clouds",
        (
            "What does the verb in the sentence \"We celebrate Children’s Day on "
            "14th November every year\" express?"):
            "A fact",
        "What emotion do we feel towards things we like?":
            "Joy",
        "What is a pronoun used for?":
            "To avoid repetition of a naming word",
        "What is another term for action words?":
            "Verb",
        (
            "What is one benefit of reading regularly using techniques of effective "
            "reading?"):
            "It expands understanding of the world around us",
        "What is the singular form of the word \"Mangoes\"?":
            "Mango",
        "What pronoun do you use for the students going to a museum?":
            "They",
        "What pronoun is used to refer to an object?":
            "It",
        (
            "What's the main benefit of proofreading an email before sending it in "
            "a professional context?"):
            "Correcting errors.",
        "When we say \"You or Your,\" to whom are we referring to?":
            "A person you are speaking to",
        "Which of the following is a naming word for a place?":
            "Office",
        "Which of the following is used to show a break within a sentence?":
            "Comma",
        (
            "Which of the following represents the six techniques of effective "
            "reading?"):
            (
                "Predicting, Visualizing, Connecting, Questioning, Clarifying, and "
                "Evaluating."),
        (
            "Which of the following sentence has correct capitalization and "
            "punctuation?"):
            "\"The sun was shining and the birds were singing.\"",
        "Which of these sentences has the verb expressing a state of being?":
            "I am a teacher.",
        "Which pronoun is appropriate for referring to a singular male?":
            "He",
        "Which pronoun is used to refer to a group of people?":
            "They",
        "Which sentence correctly uses punctuation to indicate a list of items?":
            "I like apples, bananas, and grapes.",
        "Which sentence correctly uses the plural form of a naming word?":
            "There are five boxes in the garage.",
        "Which verb form indicates the action is happening right now?":
            "Present",
        "Which word expresses a very strong negative emotion?":
            "detest",
        "Which word is in its plural form?":
            "Boxes",
        "Why are specific details important in a message about a lost item?":
            "Helps in identifying the item.",
        "Why do we use a full stop?":
            "To indicate the end of a sentence.",
        "Why do we use punctuation marks when writing?":
            "To make a sentence clear and easier to read.",
    }

    # Think activities are separate content from the assessment bank, so they
    # get their own key. Anything not listed falls back to _best_think_option.
    _THINK_ANSWER_KEY = {
        (
            "Which of the following situations best shows how AI is different "
            "from a regular computer program?"):
            "A Maps app that changes your route based on live traffic updates.",
    }

    # ------------------------------------------------------------------
    # "the user clicks on the ..." targets
    # ------------------------------------------------------------------
    # The course page lost its Overview / Course Content / Performance tabs in
    # the redesign: Overview is a modal behind the (i) beside the title, and
    # the curriculum and the certificate panel are both sections of the one
    # page. The feature still speaks in tabs, so the wording is kept and
    # routed to whatever now stands for it.
    _TAB_LOCATORS = {
        "Overview": TA.VALIDATE_OVERVIEW,
        "Course Content": TA.VALIDATE_COURSE_CONTENT,
        "Performance": TA.PERFORMANCE_HEADING,
    }

    # Everything the About panel carries. These are only on screen once the
    # Overview modal is open (an un-enrolled course renders the panel inline).
    _ABOUT_PANEL_KEYS = {
        'course overview page',
        'course duration',
        'course language',
        'course image',
        '"about this course" heading',
        'course content',
    }

    # ------------------------------------------------------------------
    # "the user should be able to see the ..." targets
    # ------------------------------------------------------------------
    # description (lower-cased, exactly as the feature writes it after
    # "the user should be able to see the ") -> (locator, scope)
    #   scope "page"  - the WSN page
    #   scope "think" - the Think activity iframe
    #   scope "quiz"  - the Moodle quiz iframe
    _VIEW_TARGETS = {
        # Home dashboard cards
        '"courses and programs" card': (TA.COURSES_AND_PROGRAMS_HEADING, "page"),
        '"programs & courses" card': (TA.COURSES_AND_PROGRAMS_HEADING, "page"),
        '"jobs connect" card': (TA.JOBS_CONNECT_HEADING, "page"),
        '"my career advisor" card': (TA.MY_CAREER_ADVISOR_HEADING, "page"),
        '"personal pitch trainer" card': (TA.PERSONAL_PITCH_TRAINER_HEADING, "page"),
        '"interview coach" card': (TA.INTERVIEW_COACH_HEADING, "page"),
        '"career buddy" card': (TA.CAREER_BUDDY_HEADING, "page"),
        '"forums" card': (TA.FORUMS_HEADING, "page"),

        # Courses listing / course detail
        'courses offered by wadhwani foundation': (
            TA.COURSES_OFFERED_BY_WADHWANI_FOUNDATION_HEADING, "page"),
        'course overview page': (TA.VALIDATE_ABOUT_THIS_COURSE, "page"),

        # Enrollment
        '"enroll now" popup': (TA.VALIDATE_NOT_NOW_BUTTON, "page"),
        '"not now" button': (TA.VALIDATE_NOT_NOW_BUTTON, "page"),
        '"enroll now" button': (TA.ENROLL_NOW_BUTTON, "page"),
        '"start course" button': (TA.START_COURSE_BUTTON, "page"),

        # Course Content
        '"orientation" section': (
            TA.ACCORDION_SECTION_BY_NAME.format("Orientation"), "page"),
        '"dev think lti" section': (
            TA.ACCORDION_SECTION_BY_NAME.format("Dev think LTI"), "page"),
        'completed tick symbol for "think 1"': (
            TA.ACTIVITY_TICK_BY_NAME.format("think 1"), "page"),
        'completed tick symbol for "think 2"': (
            TA.ACTIVITY_TICK_BY_NAME.format("think 2"), "page"),

        # Think activity (its own iframe)
        'think activity question': (TA.THINK_QUESTION_TEXT, "think"),
        'successful completion message': (TA.THINK_SUCCESS_MESSAGE, "think"),
        '"finish" button': (TA.FINISH_BUTTON, "think"),

        # Moodle quiz
        'quiz summary page': (TA.QUIZ_SUMMARY_TABLE, "quiz"),
        '"back" button': (TA.BACK_BUTTON, "quiz"),
        '"submit all and finish" button': (TA.SUBMIT_ALL_AND_FINISH_BUTTON, "quiz"),
        '"submit all your answers and finish?" popup': (TA.SUBMIT_CONFIRM_TITLE, "quiz"),
        '"cancel" button': (TA.SUBMIT_CONFIRM_CANCEL_BUTTON, "quiz"),
        'quiz score page': (TA.QUIZ_SCORE_TITLE, "quiz"),

        # Performance tab
        'overall score': (TA.OVERALL_SCORE, "page"),
        'overall progress': (TA.OVERALL_PROGRESS, "page"),
        'final score': (TA.FINAL_SCORE, "page"),
        # The earned-certificate block is headed "Congratulations !" now; the
        # old "Your Certificate Is Available" wording is kept as an alias so
        # either phrasing resolves.
        '"your certificate is available" section': (
            TA.YOUR_CERTIFICATE_IS_AVAILABLE_SECTION, "page"),
        '"congratulations" section': (
            TA.YOUR_CERTIFICATE_IS_AVAILABLE_SECTION, "page"),
        'certificate eligibility message': (TA.CERTIFICATE_ELIGIBILITY_MESSAGE, "page"),
        '"download" option': (TA.DOWNLOAD_BUTTON, "page"),
        '"download certificate" option': (TA.DOWNLOAD_BUTTON, "page"),
        '"share" option': (TA.SHARE_BUTTON, "page"),
        '"assessments" section': (TA.ASSESSMENTS_SECTION_TITLE, "page"),
        'assessment name': (TA.ASSESSMENT_NAME, "page"),
        'assessment score': (TA.ASSESSMENT_SCORE, "page"),
        'attempt date': (TA.ASSESSMENT_ATTEMPT_DATE, "page"),
        'assessment weightage': (TA.ASSESSMENT_WEIGHTAGE_CELL, "page"),
    }

    _OPTIONAL_DASHBOARD_CARD_KEYS = {
        '"jobs connect" card',
        '"career buddy" card',
    }

    _PERFORMANCE_ACTIONS = {
        '"download certificate" option and click on the "download certificate" button':
            "download_certificate",
        '"share certificate" option and click on the "share certificate" button and paste the link in new tab':
            "share_certificate_and_open_link",
        '"assessments" section and click on the "assessments progress arrow" and should see the data in assessments popup':
            "expand_assessment_progress",
        '"assessments" section and click on the "assessments progress arrow" and should see the data in assessments popup and then close the popup':
            "expand_assessment_progress",
        '"assessments" section and click on the "assessments progress arrow" and should see the data in assessments popup and then click on the assessments_progress_arrow_popup_close_button':
            "expand_assessment_progress",
        '"earned micorcertificates" card and click on the earned microcertificate button':
            "open_earned_microcertificate",
        '"earned microcertifacate" details with download & share certificate buttons':
            "verify_microcertificate_details",
    }

    # "the user should be able to validate the ..." with no expected value.
    _VALIDATE_TARGETS = {
        'course image': (TA.COURSE_BANNER_IMAGE, "page"),
        '"about this course" heading': (TA.VALIDATE_ABOUT_THIS_COURSE, "page"),
        'course content': (TA.COURSE_DESCRIPTION, "page"),
    }

    # "the user should be able to validate the ... as "<value>"".
    _VALUE_TARGETS = {
        'course duration': TA.COURSE_DURATION_VALUE,
        'course language': TA.COURSE_LANGUAGE_VALUE,
        'overall score': TA.OVERALL_SCORE_VALUE,
        'overall progress': TA.OVERALL_PROGRESS_VALUE,
    }

    # Score-page tiles, checked together so the figures can be cross-checked.
    _SCORE_PAGE_STATS = {
        'total number of questions': "total",
        'number of answered questions': "answered",
        'number of correct answers': "correct",
        'number of partially correct answers': "partial",
        'number of incorrect answers': "incorrect",
    }

    # ------------------------------------------------------------------
    # scenario-scoped instance
    # ------------------------------------------------------------------
    _shared_instance = None
    _active = False

    @classmethod
    def for_page(cls, page):
        """Return the scenario-scoped page object, rebuilding it if the
        underlying Playwright page was replaced (environment.py recreates the
        tab after a crash)."""
        instance = cls._shared_instance
        if instance is None or instance.page is not page:
            instance = cls(page)
            cls._shared_instance = instance
        return instance

    @classmethod
    def activate(cls):
        """Mark this course flow as the running one.

        newuser.feature's course scenarios share several step wordings and
        behave's registry is global, so one definition serves them all and
        routes on this flag. Activating one flow deactivates every other:
        they live in the same feature and before_feature only resets between
        features, so whichever Given ran last has to win.

        Called on the subclass too (DoLtiPage.activate()), which is why the
        flag is set through `cls` and the others are cleared by identity.
        """
        cls._active = True
        for other in _flow_classes():
            if other is not cls:
                other._active = False

    @classmethod
    def is_active(cls):
        return cls._active

    @classmethod
    def reset_shared_state(cls):
        cls._shared_instance = None
        cls._active = False

    def __init__(self, page):
        super().__init__(page)
        self._course_url = None
        self._think_frame_ref = None
        self._quiz_frame_ref = None
        # Assessment bookkeeping, read back by the verification steps.
        self._questions_seen = 0
        self._next_clicks = 0
        self._unrecognised_questions = []
        self._score_stats = {}

    # ==================================================================
    # frames
    # ==================================================================

    def _frame_matching(self, *fragments):
        for frame in self.page.frames:
            url = frame.url or ""
            if all(fragment in url for fragment in fragments):
                return frame
        return None

    def _capture_frame(self, ref_attr, fragments, description, poll_steps=FRAME_POLL_STEPS):
        for _ in range(poll_steps):
            frame = self._frame_matching(*fragments)
            if frame is not None:
                setattr(self, ref_attr, frame)
                print("%s frame captured" % description)
                return frame
            # An update modal here is why the iframe never arrives - clear it
            # and stop polling so the caller can redo the click.
            if self._dismiss_app_update_modal():
                break
            self.page.wait_for_timeout(1000)
        print("%s frame not found - falling back to the page itself" % description)
        setattr(self, ref_attr, None)
        return None

    def _live(self, frame):
        if frame is None:
            return None
        try:
            return None if frame.is_detached() else frame
        except Exception:
            return None

    def _think_frame(self, capture=True):
        """The Think activity's iframe (/en/lti-think-activity)."""
        frame = self._live(self._think_frame_ref) or self._frame_matching("lti-think-activity")
        if frame is None and capture:
            frame = self._capture_frame(
                "_think_frame_ref", ("lti-think-activity",), "Think activity", poll_steps=8)
        self._think_frame_ref = frame
        return frame or self.page

    def _quiz_frame(self, capture=True):
        """The Moodle quiz iframe (lms.<env>/mod/quiz/...)."""
        frame = self._live(self._quiz_frame_ref) or self._frame_matching("lms.", "/mod/")
        if frame is None and capture:
            frame = self._capture_frame(
                "_quiz_frame_ref", ("lms.", "/mod/"), "Assessment quiz", poll_steps=10)
        self._quiz_frame_ref = frame
        return frame or self.page

    def _scope_target(self, scope):
        if scope == "think":
            return self._think_frame(capture=False)
        if scope == "quiz":
            return self._quiz_frame(capture=False)
        return self.page

    # ==================================================================
    # low-level helpers
    # ==================================================================

    def _is_visible(self, locator, timeout=6000, target=None):
        target = target or self.page
        try:
            target.locator(locator).first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def _click(self, locator, description, timeout=20000, target=None, force=False):
        target = target or self.page
        element = target.locator(locator).first
        element.wait_for(state="visible", timeout=timeout)
        self._bring_into_view(element)
        try:
            highlight_element(self.page, element)
        except Exception:
            pass
        element.click(force=force)
        print("Clicked %s" % description)

    def _click_if_present(self, locator, description, timeout=5000, target=None, force=True):
        target = target or self.page
        try:
            element = target.locator(locator).first
            element.wait_for(state="visible", timeout=timeout)
            self._bring_into_view(element)
            element.click(force=force)
            print("Clicked %s" % description)
            return True
        except Exception:
            return False

    def _bring_into_view(self, element):
        """Scroll an element to the middle of the window before clicking it.

        force=True skips the actionability checks but NOT the viewport one, so
        anything below the fold still fails with "Element is outside of the
        viewport". scroll_into_view_if_needed() alone is not enough here: the
        run uses a maximized window with no fixed viewport, and a course card
        sits far enough down the page that it can land just outside. A JS
        scrollIntoView centred on the element handles both the vertical page
        scroll and a horizontally overflowing carousel.
        """
        try:
            element.scroll_into_view_if_needed(timeout=8000)
        except Exception:
            pass
        try:
            element.evaluate(
                "el => el.scrollIntoView({block: 'center', inline: 'center'})")
            self.page.wait_for_timeout(400)
        except Exception:
            pass

    def _text_of(self, locator, target=None, timeout=10000):
        target = target or self.page
        element = target.locator(locator).first
        element.wait_for(state="visible", timeout=timeout)
        return _norm(element.inner_text())

    def _dismiss_app_update_modal(self):
        """Clear the app's "Application update is available" modal.

        A deploy landing mid-run unmounts the SPA and blocks behind it: the page
        is still there but #app is empty, so every later locator misses for
        reasons that look nothing like the real cause. Update reloads onto the
        new build. Returns True when one was dismissed, so callers can redo
        whatever it interrupted.
        """
        if not self._is_visible(TA.APP_UPDATE_MODAL_TITLE, timeout=2500):
            return False
        print("'Application update is available' modal shown - a deploy landed "
              "mid-run; updating and reloading")
        attach_screenshot(self.page, "Application update modal")
        self._click_if_present(TA.APP_UPDATE_BUTTON, "the 'Update' button", timeout=8000)
        self.page.wait_for_timeout(8000)
        return True

    def _wait_for_page_ready(self, timeout=60000):
        """Wait out the course page's skeleton placeholders.

        The redesigned course page renders ant-skeleton blocks for tens of
        seconds before any real content arrives, so a check that fires too
        early sees an empty page and reports a missing element - "no Enroll Now
        button" for what is only a slow render.
        """
        for selector in (".wf_spinner", ".ant-skeleton"):
            try:
                self.page.wait_for_selector(selector, state="detached", timeout=timeout)
            except Exception:
                print("The page still shows '%s' after %ds - carrying on"
                      % (selector, timeout / 1000))
        self.page.wait_for_timeout(1500)

    def open_overview_modal(self):
        """Show the course's About panel.

        Duration, language, the banner image and "About this course" moved off
        the course page into an Overview modal opened by the (i) beside the
        title. An un-enrolled course still renders the same panel inline, so
        the modal is only opened when the panel is not already on screen.
        """
        self._wait_for_page_ready()
        if self._is_visible(TA.ABOUT_COURSE_PANEL, timeout=4000):
            return True
        if not self._click_if_present(TA.COURSE_OVERVIEW_INFO_TRIGGER,
                                      "the course Overview (i) button", timeout=15000):
            print("No Overview (i) trigger on this screen")
            return False
        self.page.wait_for_timeout(2000)
        return self._is_visible(TA.ABOUT_COURSE_PANEL, timeout=10000)

    def close_overview_modal(self):
        """Close the Overview modal if it is the thing on screen."""
        if not self._is_visible(TA.COURSE_OVERVIEW_MODAL, timeout=2000):
            return False
        self._click_if_present(TA.COURSE_OVERVIEW_MODAL_CLOSE,
                               "the Overview modal's close button", timeout=8000)
        self.page.wait_for_timeout(1500)
        return True

    # ==================================================================
    # login / navigation
    # ==================================================================

    def verify_logged_in(self, base_url):
        """Continue as the user the feature's first scenario just registered.

        The scenario only means anything on a brand-new account: an existing one
        is already enrolled, has the Think activities finished and has quiz
        attempts on record, so every fresh-course check below would be testing
        nothing. newuser.feature's first scenario creates that account through
        the manual email/OTP flow, and this step adopts the session it leaves
        open.

        There is deliberately NO fallback to configured credentials: logging in
        here would silently swap the freshly registered user for a stale account
        and hollow out the rest of the scenario.
        """
        type(self).activate()
        page = self.page
        self._dismiss_app_update_modal()

        if self._is_visible(TA.EXPLORE_THINGS_TO_DO_HEADING, timeout=10000):
            print("Continuing as the user registered earlier in this feature")
            attach_screenshot(page, "Logged into the WSN application")
            return

        # Signed in but parked elsewhere - the registration scenario can finish
        # on a profile or course screen.
        if page.url and not any(f in page.url for f in ("/guest", "/login", "about:blank")):
            print("A session is open at %s - navigating home to continue as the "
                  "registered user" % page.url)
            page.goto(base_url.replace("/guest", "/home"),
                      wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)
            self._dismiss_app_update_modal()
            if self._is_visible(TA.EXPLORE_THINGS_TO_DO_HEADING, timeout=20000):
                attach_screenshot(page, "Logged into the WSN application")
                return

        raise AssertionError(
            "No signed-in session to continue. This scenario runs as the user "
            "registered by newuser.feature's first scenario, which needs the "
            "email and OTP typed in manually - run the whole feature "
            "(behave features/newuser.feature), not this scenario on its own."
        )

    def verify_navigated_to(self, destination):
        """Assert a page/tab actually rendered after a navigation click."""
        checks = {
            "Home": TA.EXPLORE_THINGS_TO_DO_HEADING,
            "Courses": TA.COURSES_OFFERED_BY_WADHWANI_FOUNDATION_HEADING,
            "Performance": TA.COURSE_COMPLETION_PANEL,
            "Course Content": TA.ACTIVITY_CARD,
            "Overview": TA.VALIDATE_ABOUT_THIS_COURSE,
        }
        target = destination.strip()
        locator = checks.get(target)
        if locator is None:
            raise ValueError("No navigation check mapped for the '%s' page" % destination)

        self._wait_for_page_ready()

        # Overview is a modal now, not a tab - open it before looking for the
        # About panel.
        if target == "Overview":
            self.open_overview_modal()

        # "Performance" no longer exists as a tab or a route: the score tile
        # and the certificate panel it used to hold are sections of the course
        # page, so being back on the course page is what proves the step.
        if target == "Performance" and not self._is_visible(locator, timeout=8000):
            self.return_to_course()
            self._wait_for_page_ready()

        if not self._is_visible(locator, timeout=20000):
            raise AssertionError("The %s page did not render" % destination)
        print("Navigated to the %s page" % destination)
        attach_screenshot(self.page, "%s page" % destination)

    def verify_explore_cards(self, expected_count, section):
        """Assert the "Explore things to do" grid and count its cards.

        The grid hydrates in stages, so the count is read repeatedly until two
        consecutive reads agree - otherwise the check races the dashboard and
        sees whatever had rendered by then.
        """
        self.page.locator(TA.EXPLORE_THINGS_TO_DO_HEADING).first.wait_for(
            state="visible", timeout=20000)

        titles, previous = [], None
        for _ in range(12):
            titles = [_norm(t) for t in self.page.locator(TA.EXPLORE_CARD_TITLE).all_inner_texts()]
            if titles and titles == previous:
                break
            previous = titles
            self.page.wait_for_timeout(1500)

        optional_cards = {"jobs connect", "career buddy"}
        missing_optional = optional_cards.difference(title.lower() for title in titles)
        adjusted_expected = expected_count - len(missing_optional)
        print("Cards under '%s' (%d): %s" % (section, len(titles), ", ".join(titles)))
        for card in sorted(missing_optional):
            print("Optional dashboard card '%s' is unavailable; excluding it from the count"
                  % card)
        attach_screenshot(self.page, "'%s' cards" % section)
        assert len(titles) == adjusted_expected, (
            "Expected %d cards under '%s' after excluding unavailable optional cards, "
            "but the dashboard rendered %d: %s"
            % (adjusted_expected, section, len(titles), ", ".join(titles)))

    _CARD_LOCATORS = {
        # The dashboard renders this card as "Programs & Courses"; the feature
        # calls it by its product name, so the label is mapped rather than
        # matched on text.
        'courses and programs': TA.COURSES_AND_PROGRAMS_HEADING,
        'my career advisor': TA.MY_CAREER_ADVISOR_HEADING,
        'personal pitch trainer': TA.PERSONAL_PITCH_TRAINER_HEADING,
        'interview coach': TA.INTERVIEW_COACH_HEADING,
        'career buddy': TA.CAREER_BUDDY_HEADING,
        'forums': TA.FORUMS_HEADING,
    }

    def click_card(self, label):
        """Click one of the "Explore things to do" cards."""
        locator = self._CARD_LOCATORS.get(_norm(label).lower(),
                                          "//h6[normalize-space()='%s']" % label)
        self._click(locator, "the '%s' card" % label)
        self.page.wait_for_timeout(4000)
        self._dismiss_app_update_modal()

    def click_tab(self, name):
        """Open what the feature still calls a tab.

        Only Overview is clickable now - as the (i) modal. Course Content and
        Performance are sections of the course page, so there is nothing to
        click: the page just has to be the course page, fully rendered.
        """
        if name not in self._TAB_LOCATORS:
            raise ValueError("No locator mapped for the '%s' tab" % name)
        if name == "Overview":
            if not self.open_overview_modal():
                raise AssertionError("The course Overview could not be opened")
            attach_screenshot(self.page, "Course Overview")
            return
        self.close_overview_modal()
        self._wait_for_page_ready()
        if name == "Course Content":
            self.open_course_content()
            return
        if not self._is_visible(TA.COURSE_COMPLETION_PANEL, timeout=10000):
            print("No completion panel on the course page yet - the certificate "
                  "block only renders once the course is finished")
        self.page.wait_for_timeout(1500)

    def click_course(self, name):
        """Open the course from the carousel.

        The carousel clones every card three times and only the copies inside a
        "--active" item are in the visible window, so the active one is what
        gets clicked; the rest sit outside the viewport where a click fails.
        """
        if name != "Dev-Think LTI-Open":
            raise ValueError("No locator mapped for the '%s' course" % name)
        self._wait_for_page_ready()
        if self.scroll_carousel_to_course(name):
            self._click(TA.DEV_THINK_LTI_OPEN_CARD_ACTIVE, "the '%s' course" % name, force=True)
        else:
            # The listing renders the card several times (the carousel clones
            # every item); when none of the copies is in the active window,
            # click whichever one is there - _bring_into_view scrolls it into
            # the viewport first, horizontally included.
            self._click(TA.DEV_THINK_LTI_OPEN_HEADING, "the '%s' course" % name, force=True)
        self.page.wait_for_timeout(4000)
        self._dismiss_app_update_modal()
        self._course_url = self.page.url
        # No Overview click here: an un-enrolled course opens on Overview
        # already, and this scenario always runs as a freshly registered user.
        # Clicking the tab anyway navigated on every run for no reason.
        attach_screenshot(self.page, "'%s' course opened" % name)

    def scroll_carousel_to_course(self, name, max_clicks=8):
        """Page the carousel until the card is in its active (visible) window.

        The course normally sits FIRST in its strip, so most runs need no
        paging at all. When paging is needed, both arrows are tried - and both
        are scoped to the carousel that actually holds this card, because the
        page can carry several strips and the first arrow on the page usually
        belongs to a different one.
        """
        if self._is_visible(TA.DEV_THINK_LTI_OPEN_CARD_ACTIVE, timeout=8000):
            print("'%s' card is already in the carousel's active window" % name)
            return True
        for arrow, direction in ((TA.DEV_THINK_CAROUSEL_LEFT_ARROW, "previous"),
                                 (TA.DEV_THINK_CAROUSEL_RIGHT_ARROW, "next")):
            for attempt in range(max_clicks):
                if not self._click_if_present(
                        arrow, "carousel %s arrow (%d)" % (direction, attempt + 1),
                        timeout=4000):
                    break
                self.page.wait_for_timeout(1200)
                if self._is_visible(TA.DEV_THINK_LTI_OPEN_CARD_ACTIVE, timeout=3000):
                    print("'%s' card reached after %d %s click(s)"
                          % (name, attempt + 1, direction))
                    return True
        print("'%s' card not brought into the carousel's active window" % name)
        return False

    def return_to_course(self):
        """Go back to the course page.

        The activities run behind iframe-based routing, so browser history lands
        on unpredictable states - navigate to the remembered course URL instead.
        """
        if not self._course_url:
            print("No stored course URL - staying on the current page")
            return
        self.page.goto(self._course_url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(3000)
        self._dismiss_app_update_modal()
        self._think_frame_ref = None
        self._quiz_frame_ref = None

    def open_course_content(self):
        """Make sure the course curriculum is the thing on screen.

        There is no Course Content tab to click any more - the curriculum is a
        section of the course page. What can hide it is the Overview modal
        sitting on top, or the page still being drawn as skeletons.
        """
        self.close_overview_modal()
        if self._is_visible(TA.ACTIVITY_CARD, timeout=4000):
            return
        self._wait_for_page_ready()
        if self._is_visible(TA.COURSE_CURRICULUM_SECTION, timeout=10000):
            return
        print("The course curriculum section has not rendered yet")

    # ==================================================================
    # enrollment
    # ==================================================================

    def click_enroll_now(self):
        """Open the enrollment popup.

        The scenario runs as the user registered in this feature's first
        scenario, so the course is always un-enrolled here. No Enroll Now button
        means the run is not on a fresh account, which is a real failure.
        """
        # The redesigned course page draws skeletons for tens of seconds; check
        # for the button only once they are gone, or a slow render reads as a
        # missing button.
        self._wait_for_page_ready()
        if not (self._is_visible(TA.ENROLL_NOW_BUTTON_ON_COURSE, timeout=15000)
                or self._is_visible(TA.ENROLL_NOW_BUTTON, timeout=5000)):
            raise AssertionError(
                "No 'Enroll Now' button on the Dev-Think LTI-Open course. This "
                "scenario has to run as a freshly registered user - run the whole "
                "feature (behave features/newuser.feature) so the manual email/OTP "
                "registration creates a new account first.")
        self._click(TA.ENROLL_NOW_BUTTON, "the 'Enroll Now' button")
        self.page.wait_for_timeout(2500)
        attach_screenshot(self.page, "Enroll Now popup")

    def click_enroll_now_in_popup(self):
        locator = (TA.ENROLL_NOW_BUTTON_2
                   if self.page.locator(TA.ENROLL_NOW_BUTTON).count() > 1
                   else TA.ENROLL_NOW_BUTTON)
        self._click(locator, "the 'Enroll Now' button in the popup")
        self.page.wait_for_timeout(5000)
        self._dismiss_app_update_modal()
        self._course_url = self.page.url
        attach_screenshot(self.page, "Enrolled in the course")

    def verify_enrolled(self):
        """Assert the course now shows its enrolled state.

        The redesign removed the "Start Course" button that used to prove this
        - neither state of the page has one. What separates the two states now
        is the Enroll Now button itself: it is on an un-enrolled course and
        gone once the enrollment goes through, leaving the curriculum with its
        per-activity Start buttons.
        """
        self._wait_for_page_ready()
        for _ in range(10):
            if not self._is_visible(TA.ENROLL_NOW_BUTTON_ON_COURSE, timeout=2000):
                break
            self.page.wait_for_timeout(2000)
        else:
            raise AssertionError(
                "The course still offers 'Enroll Now' - the enrollment did not "
                "go through")
        if not (self._is_visible(TA.ACTIVITY_CARD, timeout=15000)
                or self._is_visible(TA.COURSE_CURRICULUM_SECTION, timeout=5000)):
            raise AssertionError(
                "The course does not show an enrolled state - no curriculum "
                "rendered after enrolling")
        print("The user is enrolled in the Dev-Think LTI-Open course")
        attach_screenshot(self.page, "Enrolled in the course")

    # ==================================================================
    # generic validations
    # ==================================================================

    def verify_visible(self, description):
        """Assert one "the user should be able to see the ..." element."""
        key = _norm(description).lower()
        action = self._PERFORMANCE_ACTIONS.get(key)
        if action is not None:
            getattr(self, action)()
            return
        entry = self._VIEW_TARGETS.get(key)
        if entry is None:
            raise ValueError(
                "No locator mapped for 'the user should be able to see the %s' - "
                "add it to ThinkActivityPage._VIEW_TARGETS" % description)
        locator, scope = entry
        if key in self._ABOUT_PANEL_KEYS:
            self.open_overview_modal()
        visible = self._is_visible(locator, timeout=20000, target=self._scope_target(scope))
        if not visible and key in self._OPTIONAL_DASHBOARD_CARD_KEYS:
            print("Optional dashboard card %s is unavailable; skipping this check"
                  % description)
            return
        if not visible:
            raise AssertionError("'%s' is not visible" % description)
        print("Validated: %s" % description)

    def _click_for_download(self, locator, description):
        """Click a certificate download control and require a real download."""
        button = self.page.locator(locator).first
        button.wait_for(state="visible", timeout=15000)
        with self.page.expect_download(timeout=30000) as download_info:
            button.click()
        download = download_info.value
        failure = download.failure()
        assert failure is None, "%s failed: %s" % (description, failure)
        print("Downloaded %s: %s" % (description, download.suggested_filename))

    def _share_and_open_link(self, locator, description):
        """Click Share, open the resulting/copied URL in a new tab, then close it."""
        button = self.page.locator(locator).first
        button.wait_for(state="visible", timeout=15000)
        origin = "/".join(self.page.url.split("/")[:3])
        try:
            self.page.context.grant_permissions(
                ["clipboard-read", "clipboard-write"], origin=origin)
        except Exception:
            pass
        new_tab = None
        try:
            with self.page.context.expect_page(timeout=2500) as page_info:
                button.click()
            new_tab = page_info.value
        except Exception:
            try:
                shared_url = self.page.evaluate(
                    "() => navigator.clipboard.readText()")
            except Exception as error:
                raise AssertionError(
                    "%s did not open a new tab or provide a readable share link: %s"
                    % (description, error)) from error
            if not shared_url or not shared_url.startswith(("http://", "https://")):
                raise AssertionError("%s did not provide a valid share URL" % description)
            new_tab = self.page.context.new_page()
            new_tab.goto(shared_url, wait_until="domcontentloaded", timeout=30000)

        try:
            new_tab.wait_for_load_state("domcontentloaded", timeout=30000)
            assert new_tab.url and new_tab.url != "about:blank", (
                "%s opened a blank tab" % description)
            print("Opened the %s link in a new tab: %s" % (description, new_tab.url))
            attach_screenshot(new_tab, "%s link opened" % description)
        finally:
            if new_tab is not None and not new_tab.is_closed():
                new_tab.close()
            self.page.bring_to_front()

    def download_certificate(self):
        self._click_for_download(TA.DOWNLOAD_CERTIFICATE_BUTTON, "certificate")

    def share_certificate_and_open_link(self):
        self._share_and_open_link(TA.SHARE_CERTIFICATE_BUTTON, "certificate share")

    def expand_assessment_progress(self):
        self._click(TA.ASSESSMENTS_PROGRESS_ARROW,
                    "the Assessments progress arrow", timeout=15000)
        if not self._is_visible(TA.ASSESSMENT_NAME, timeout=10000):
            raise AssertionError("Assessment progress opened without assessment data")
        if not self._is_visible(TA.ASSESSMENT_SCORE, timeout=10000):
            raise AssertionError("Assessment progress does not show the score")
        print("Assessment progress data is visible")
        self._click(TA.ASSESSMENTS_PROGRESS_ARROW_POPUP_CLOSE_BUTTON,
                    "the Assessments progress popup close icon", timeout=10000)
        if self._is_visible(TA.ASSESSMENT_NAME, timeout=3000):
            raise AssertionError("The Assessments progress popup did not close")
        print("Assessment progress popup closed")

    def open_earned_microcertificate(self):
        card = self.page.locator(TA.EARNED_MICRO_CERTIFICATES_CARD).first
        try:
            card.wait_for(state="visible", timeout=15000)
        except Exception:
            raise AssertionError("The Earned Microcertificates card is not visible")
        arrow = card.locator(TA.EARNED_MICRO_CERTIFICATE_ARROW).first
        try:
            arrow.wait_for(state="visible", timeout=10000)
        except Exception:
            raise AssertionError(
                "The Earned Microcertificates card has no visible details button")
        self._click(TA.EARNED_MICRO_CERTIFICATE_ARROW,
                    "the earned microcertificate button", timeout=15000, target=card)
        self.verify_microcertificate_details()

    def verify_microcertificate_details(self):
        for locator, label in (
            (TA.MICRO_CERTIFICATE_DOWNLOAD_BUTTON, "Microcertificate download"),
            (TA.MICRO_CERTIFICATE_SHARE_BUTTON, "Microcertificate share"),
        ):
            if not self._is_visible(locator, timeout=15000):
                raise AssertionError("The earned microcertificate details lack %s" % label)
        print("Earned microcertificate details and actions are visible")

    def download_microcertificate_and_share(self):
        self._click_for_download(TA.MICRO_CERTIFICATE_DOWNLOAD_BUTTON, "microcertificate")
        self._share_and_open_link(TA.MICRO_CERTIFICATE_SHARE_BUTTON,
                                  "microcertificate share")

    def validate(self, description):
        """Handle "the user should be able to validate the ..." (no value)."""
        key = _norm(description).lower()

        if key in self._SCORE_PAGE_STATS:
            self._validate_score_page_stat(key)
            return
        if key == "overall score":
            self._validate_quiz_overall_score()
            return

        entry = self._VALIDATE_TARGETS.get(key)
        if entry is None:
            # Anything the scenario only asks to "see" is equally valid to
            # "validate" - reuse that mapping rather than duplicating it.
            if key in self._VIEW_TARGETS:
                self.verify_visible(description)
                return
            raise ValueError(
                "No locator mapped for 'the user should be able to validate the %s' - "
                "add it to ThinkActivityPage._VALIDATE_TARGETS" % description)
        locator, scope = entry
        if key in self._ABOUT_PANEL_KEYS:
            self.open_overview_modal()
        target = self._scope_target(scope)
        if not self._is_visible(locator, timeout=20000, target=target):
            raise AssertionError("'%s' could not be validated" % description)
        try:
            print("Validated %s: %s" % (description, self._text_of(locator, target=target)))
        except Exception:
            print("Validated %s" % description)

    def validate_value(self, description, expected):
        """Handle '... validate the {field} as "{value}"'."""
        key = _norm(description).lower()
        locator = self._VALUE_TARGETS.get(key)
        if locator is None:
            raise ValueError(
                "No locator mapped for 'validate the %s as \"%s\"' - add it to "
                "ThinkActivityPage._VALUE_TARGETS" % (description, expected))
        if key in self._ABOUT_PANEL_KEYS:
            self.open_overview_modal()
        actual = self._text_of(locator, timeout=20000)
        # The About panel's pills carry their own label ("Language: English"),
        # while the feature states the value alone.
        if ":" in actual:
            actual = actual.split(":", 1)[1].strip()
        assert _slug(actual) == _slug(expected), (
            "Expected the %s to be '%s' but it is '%s'" % (description, expected, actual))
        print("Validated %s: %s" % (description, actual))

    # ==================================================================
    # Orientation
    # ==================================================================

    def complete_orientation(self, section="Orientation"):
        """Open the Orientation PDF and come back to the Course Content tab.

        The PDF has no submit or finish of its own: opening it is what the
        course counts, and the lesson page's back arrow is how it is left. The
        arrow lands back on the course, so the step after this one can go
        straight on to the next section.
        """
        self.return_to_course()
        self.open_course_content()
        self._click_if_present(TA.ACCORDION_SECTION_BY_NAME.format(section),
                               "the '%s' section" % section, timeout=10000)
        self.page.wait_for_timeout(2000)
        self._click_if_present(TA.ACCORDION_CHILD_BY_NAME.format(section),
                               "the '%s' lesson" % section, timeout=8000)
        self.page.wait_for_timeout(3000)

        if not self._click_if_present(TA.ACTIVITY_ACTION_BUTTON,
                                      "the Orientation PDF activity's 'Start' button",
                                      timeout=15000):
            raise AssertionError("The Orientation lesson lists no activity to open")
        self.page.wait_for_timeout(6000)
        self._dismiss_certificate_name_popup()
        self._dismiss_app_update_modal()

        # The back arrow only exists on the lesson page, so it doubles as proof
        # the PDF really opened. Dismissing the certificate-name modal does not
        # always enter the lesson, so Start is used once more when it did not.
        if not self._is_visible(TA.LESSON_BACK_ARROW, timeout=10000):
            print("The Orientation PDF did not open on the first 'Start' - clicking it again")
            self._click_if_present(TA.ACTIVITY_ACTION_BUTTON,
                                   "the Orientation PDF activity's 'Start' button (again)",
                                   timeout=10000)
            self.page.wait_for_timeout(6000)
            self._dismiss_app_update_modal()
        if not self._is_visible(TA.LESSON_BACK_ARROW, timeout=15000):
            raise AssertionError(
                "The Orientation PDF did not open - no lesson page to go back from")
        # Let the PDF render before leaving, so the course records the visit.
        self.page.wait_for_timeout(4000)
        attach_screenshot(self.page, "Orientation PDF opened")

        self._click(TA.LESSON_BACK_ARROW, "the Orientation back arrow", timeout=12000)
        self.page.wait_for_timeout(5000)
        self._dismiss_app_update_modal()
        self.open_course_content()
        attach_screenshot(self.page, "Back on Course Content after Orientation")

    # ==================================================================
    # Think activities
    # ==================================================================

    def open_think_activity(self, activity_name, section="Dev think LTI", _retry=True):
        """Open one Think activity from the Course Content tab.

        On the freshly registered user this runs as, the card's action button
        reads "Start" (or "Resume" if the lesson was opened before). A finished
        activity shows "Result" instead, which means the run is not on a fresh
        account - reported as a failure, because a completed activity cannot
        exercise the answer/submit/finish journey below.
        """
        self.return_to_course()
        self.open_course_content()
        self._click_if_present(TA.ACCORDION_SECTION_BY_NAME.format(section),
                               "the '%s' section" % section, timeout=10000)
        self.page.wait_for_timeout(2000)
        self._click_if_present(TA.ACCORDION_CHILD_BY_NAME.format(section),
                               "the '%s' lesson" % section, timeout=8000)
        self.page.wait_for_timeout(3000)

        self.page.locator(TA.ACTIVITY_CARD_BY_NAME.format(activity_name)).first.wait_for(
            state="visible", timeout=20000)
        action = self.page.locator(
            TA.ACTIVITY_ACTION_BUTTON_BY_NAME.format(activity_name)).first
        action.wait_for(state="visible", timeout=15000)
        label = _norm(action.inner_text())
        if label.lower() == "result":
            raise AssertionError(
                "The '%s' activity is already completed (its button reads '%s'), so "
                "it cannot be answered. This scenario has to run as a freshly "
                "registered user - run the whole feature "
                "(behave features/newuser.feature)." % (activity_name, label))
        try:
            highlight_element(self.page, action)
        except Exception:
            pass
        action.click(force=True)
        print("Clicked the '%s' button for the '%s' activity" % (label, activity_name))
        self.page.wait_for_timeout(6000)

        self._dismiss_certificate_name_popup()
        frame = self._capture_activity_frame()
        if frame is None and _retry:
            # Almost always an app-update modal that unmounted the SPA while the
            # activity was loading; _capture_frame has cleared it by now, so the
            # click just has to be made again on the reloaded build.
            print("'%s' did not open - retrying once on the reloaded app" % activity_name)
            self.open_think_activity(activity_name, section=section, _retry=False)
            return
        attach_screenshot(self.page, "'%s' activity opened" % activity_name)

    def _capture_activity_frame(self):
        """The iframe an activity of THIS course opens in.

        Overridden by DoLtiPage, whose activities run in their own LTI iframe -
        open_think_activity() is otherwise identical for both courses.
        """
        return self._capture_frame("_think_frame_ref", ("lti-think-activity",),
                                   "Think activity")

    def _dismiss_certificate_name_popup(self):
        """Clear the one-time "Review Your Certificate Name" prompt.

        It is raised the first time a user starts ANY activity, so a run that
        began with the manual new-user registration meets it on think 1 and
        never again.
        """
        if not self._is_visible(TA.CONFIRM_AND_CONTINUE_BUTTON, timeout=6000):
            return
        print("'Review Your Certificate Name' popup shown (first activity for this "
              "user) - confirming the certificate name")
        attach_screenshot(self.page, "Review Your Certificate Name popup")
        self._click(TA.CONFIRM_AND_CONTINUE_BUTTON, "the 'Confirm & Continue' button")
        self.page.wait_for_timeout(5000)

    def _think_options(self, frame):
        rows = frame.locator(TA.THINK_OPTION)
        try:
            rows.first.wait_for(state="visible", timeout=ACTIVITY_CONTENT_TIMEOUT_MS)
        except Exception:
            return []
        return [rows.nth(i) for i in range(rows.count())]

    def _best_think_option(self, question, labels):
        """Choose a Think option: the answer key first, then a heuristic.

        The heuristic prefers the longest option that is not an
        "all/none of the above" catch-all - a far better default than a fixed
        index when the key has no entry for this question.
        """
        wanted = self._lookup(self._THINK_ANSWER_KEY, question)
        if wanted:
            index = self._match_option(wanted, labels)
            if index is not None:
                return index, "answer key (%s)" % wanted
        catch_alls = ("all of the above", "none of the above", "both",
                      "all the given options")
        ranked = sorted(range(len(labels)),
                        key=lambda i: (_slug(labels[i]) in catch_alls, -len(labels[i])))
        return (ranked[0] if ranked else 0), "heuristic (no answer-key entry)"

    def answer_think_activity(self, activity_number):
        """Answer the Think question currently on screen."""
        frame = self._think_frame()
        question = ""
        try:
            question = self._text_of(TA.THINK_QUESTION_TEXT, target=frame,
                                     timeout=ACTIVITY_CONTENT_TIMEOUT_MS)
        except Exception:
            print("Could not read the Think question text")
        options = self._think_options(frame)
        if not options:
            raise AssertionError("Think %d rendered no answer options" % activity_number)

        labels = [_norm(o.locator(TA.THINK_OPTION_TEXT).first.inner_text()) for o in options]
        index, why = self._best_think_option(question, labels)
        options[index].locator(TA.THINK_OPTION_RADIO).first.check(force=True)
        print("Think %d: '%s'\n  answered '%s' via %s"
              % (activity_number, question, labels[index], why))
        self.page.wait_for_timeout(1500)
        attach_screenshot(self.page, "Think %d answered" % activity_number)

    def click_think_submit(self):
        frame = self._think_frame()
        self._click(TA.THINK_SUBMIT_BUTTON, "the 'Submit' button", target=frame, timeout=15000)
        self.page.wait_for_timeout(4000)
        attach_screenshot(self.page, "Think activity submitted")

    def click_think_finish(self):
        """Finish a Think activity and come back to the Course Content tab.

        The Finish click leaves you on the LESSON page, but the step straight
        after asserts the activity's completed tick, which only exists on the
        Course Content activity cards - so this always returns there.
        """
        frame = self._think_frame()
        if not self._click_if_present(TA.FINISH_BUTTON, "the 'Finish' button",
                                      timeout=10000, target=frame):
            raise AssertionError("The Think activity's 'Finish' button was not clickable")
        self.page.wait_for_timeout(4000)
        self.return_to_course()
        self.open_course_content()
        attach_screenshot(self.page, "Back on Course Content")

    def verify_can_access(self, activity_name):
        """Assert the next Think activity is reachable."""
        self.return_to_course()
        self.open_course_content()
        self._click_if_present(TA.ACCORDION_SECTION_BY_NAME.format("Dev think LTI"),
                               "the 'Dev think LTI' section", timeout=8000)
        self.page.wait_for_timeout(2000)
        if not self._is_visible(TA.ACTIVITY_CARD_BY_NAME.format(activity_name), timeout=15000):
            raise AssertionError("The '%s' activity is not available" % activity_name)
        print("'%s' is available" % activity_name)
        attach_screenshot(self.page, "'%s' available" % activity_name)

    # ==================================================================
    # Assessment - navigation
    # ==================================================================

    def open_assessment_section(self, section="Assesment"):
        """Open the Assesment lesson (note the app's own spelling)."""
        self.return_to_course()
        self.open_course_content()
        for name in (section, "Assessment"):
            if self._click_if_present(TA.ACCORDION_SECTION_BY_NAME.format(name),
                                      "the '%s' section" % name, timeout=8000):
                self.page.wait_for_timeout(2500)
                self._click_if_present(TA.ACCORDION_CHILD_BY_NAME.format(name),
                                       "the '%s' lesson" % name, timeout=8000)
                self.page.wait_for_timeout(4000)
                print("Opened the '%s' section" % name)
                attach_screenshot(self.page, "Assessment section")
                return
        raise AssertionError("The Assesment section could not be opened")

    def start_quiz_attempt(self):
        """Open the quiz activity and start the attempt.

        Two buttons stand between the lesson and the questions: the WSN activity
        card's own Start, then Moodle's "Attempt quiz". On the fresh account
        this runs as, that is the only label the quiz can show.
        """
        quiz_button = TA.ACTIVITY_ACTION_BUTTON_BY_NAME.format("Quiz")
        if self._is_visible(quiz_button, timeout=8000):
            self._click(quiz_button, "the Quiz activity's action button", force=True)
            self.page.wait_for_timeout(9000)

        frame = self._capture_frame("_quiz_frame_ref", ("lms.", "/mod/"), "Assessment quiz")
        if frame is None:
            raise AssertionError("The assessment's quiz iframe did not load")

        if not self._click_if_present(TA.ATTEMPT_QUIZ_BUTTON, "'Attempt quiz'",
                                      timeout=10000, target=frame):
            raise AssertionError(
                "No 'Attempt quiz' button on the quiz. A quiz that instead offers "
                "'Re-attempt quiz' or 'Continue your attempt' already has an attempt "
                "on record, so this is not a freshly registered user - run the whole "
                "feature (behave features/newuser.feature).")
        self.page.wait_for_timeout(8000)
        self._quiz_frame_ref = self._frame_matching("lms.", "/mod/")
        attach_screenshot(self.page, "Assessment started")

    def verify_assessment_started(self):
        frame = self._quiz_frame()
        if not self._is_visible(TA.QUESTION_CONTAINER, timeout=25000, target=frame):
            raise AssertionError("The assessment attempt did not open")
        print("The assessment attempt is open")
        attach_screenshot(self.page, "Assessment attempt open")

    def verify_question_count(self, expected):
        """Assert how many questions this attempt has.

        Counted from the quiz navigation block, which lists one button per
        question regardless of how they are spread across pages.
        """
        frame = self._quiz_frame()
        nav = frame.locator(TA.QUIZ_NAV_BUTTON)
        try:
            nav.first.wait_for(state="attached", timeout=15000)
            actual = nav.count()
        except Exception:
            actual = frame.locator(TA.QUESTION_CONTAINER).count()
        self._questions_seen = actual
        print("The assessment presents %d question(s)" % actual)
        assert actual == expected, (
            "Expected the assessment to have %d questions but it presents %d"
            % (expected, actual))

    # ==================================================================
    # Assessment - answering
    # ==================================================================

    def _lookup(self, key_map, question):
        """Find a question in an answer key, tolerating small wording drift."""
        wanted = _slug(question)
        if not wanted:
            return None
        index = {_slug(q): a for q, a in key_map.items()}
        if wanted in index:
            return index[wanted]
        close = difflib.get_close_matches(wanted, list(index), n=1, cutoff=0.85)
        return index[close[0]] if close else None

    def _match_option(self, wanted, labels):
        """Index of the option whose TEXT is the wanted answer, or None.

        Matching on text rather than position is what makes the answer correct:
        Moodle shuffles the options between attempts, so a fixed index would
        pick a different answer every run.

        Punctuation is compared FIRST and only then ignored. Some questions ask
        which sentence is punctuated correctly, and their options differ by
        nothing but the commas - "I like apples, bananas, and grapes." against
        "I like apples bananas and grapes." Those collapse to the same _slug, so
        a slug-first match can pick the wrong one and lose the mark.
        """
        exact = [_norm(l) for l in labels]
        target_exact = _norm(wanted)
        if target_exact in exact:
            return exact.index(target_exact)
        # Same text bar the surrounding quotes some options are wrapped in.
        quotes = '"' + "'"
        stripped = [e.strip(quotes) for e in exact]
        if target_exact.strip(quotes) in stripped:
            return stripped.index(target_exact.strip(quotes))

        slugs = [_slug(l) for l in labels]
        target = _slug(wanted)
        if target in slugs:
            # Ambiguous only when several options share the slug - that is the
            # punctuation case, and without the exact text there is nothing to
            # separate them, so report no match rather than guess wrong.
            if slugs.count(target) > 1:
                print("  !! %d options are identical once punctuation is ignored; "
                      "cannot tell them apart from '%s'" % (slugs.count(target), wanted))
                return None
            return slugs.index(target)
        close = difflib.get_close_matches(target, slugs, n=1, cutoff=0.7)
        if close:
            return slugs.index(close[0])
        for i, sl in enumerate(slugs):
            if sl and (sl in target or target in sl):
                return i
        return None

    def _answer_question(self, question_element):
        """Answer one Moodle question from the key."""
        question = _norm(question_element.locator(TA.QUESTION_TEXT).first.inner_text())
        rows = question_element.locator(TA.ANSWER_OPTION_ROW)
        count = rows.count()
        if not count:
            print("No selectable options for: %s" % question)
            return
        options = [rows.nth(i) for i in range(count)]
        # Strip the "a. " / "b. " prefix Moodle prints before each option.
        labels = [re.sub(r"^[a-h]\.\s*", "", _norm(o.inner_text())) for o in options]

        wanted = self._lookup(self._ANSWER_KEY, question)
        if wanted is None:
            self._unrecognised_questions.append(question)
            index = 0
            print("  ?? no answer-key entry for: %s\n     picking '%s' - the review "
                  "page will reveal the correct answer at the end of the attempt"
                  % (question, labels[index]))
        else:
            index = self._match_option(wanted, labels)
            if index is None:
                self._unrecognised_questions.append(question)
                index = 0
                print("  !! key says '%s' but no option matches it for: %s"
                      % (wanted, question))
            else:
                print("  Q: %s\n     -> %s" % (question, labels[index]))
        options[index].locator(TA.ANSWER_OPTION_RADIO).first.check(force=True)

    def answer_all_questions(self, expected_count=None):
        """Answer every question in the attempt, paging forward as it goes.

        Moodle serves one question per page here and its Next control saves the
        page before advancing, so answering and paging are one loop; it ends on
        the summary of attempt, which is where the feature file picks up.
        """
        answered = 0
        for _ in range((expected_count or 10) + 5):
            frame = self._quiz_frame()
            questions = frame.locator(TA.QUESTION_CONTAINER)
            if not questions.count():
                break
            for i in range(questions.count()):
                self._answer_question(questions.nth(i))
                answered += 1
            nxt = frame.locator(TA.NEXT_OR_FINISH_ATTEMPT_BUTTON)
            if not nxt.count():
                break
            value = nxt.first.get_attribute("value") or ""
            nxt.first.click()
            self._next_clicks += 1
            self.page.wait_for_timeout(5000)
            self._quiz_frame_ref = self._frame_matching("lms.", "/mod/")
            if "Finish attempt" in value:
                break
        self._questions_seen = max(self._questions_seen, answered)
        print("Answered %d question(s) over %d page advance(s)"
              % (answered, self._next_clicks))
        if self._unrecognised_questions:
            print("%d question(s) were not in the answer key"
                  % len(self._unrecognised_questions))
        attach_screenshot(self.page, "All questions answered")

    def verify_clicked_next_for_each_question(self):
        assert self._next_clicks > 0, "The attempt was never advanced with 'Next'"
        print("'Next' was used %d time(s) to move through the attempt" % self._next_clicks)

    def verify_navigated_to_next_question(self):
        assert self._next_clicks > 1 or self._is_visible(
            TA.QUIZ_SUMMARY_TABLE, timeout=10000, target=self._quiz_frame()), (
            "The attempt never advanced past its first question")
        print("The attempt advanced through its questions")

    def verify_answers_saved(self):
        """Assert the summary of attempt reports every question as answered."""
        frame = self._quiz_frame()
        cells = frame.locator(TA.QUIZ_SUMMARY_STATUS_CELL)
        try:
            cells.first.wait_for(state="visible", timeout=20000)
        except Exception:
            raise AssertionError("The summary of attempt did not render")
        statuses = [_norm(t) for t in cells.all_inner_texts()]
        print("Summary of attempt statuses: %s" % statuses)
        unsaved = [s for s in statuses if "answer saved" not in s.lower()]
        assert not unsaved, "Some answers were not saved: %s" % unsaved

    def complete_all_questions(self, expected_count=None):
        """Assert the attempt reached its summary with every question listed."""
        frame = self._quiz_frame()
        rows = frame.locator(TA.QUIZ_SUMMARY_STATUS_CELL)
        try:
            rows.first.wait_for(state="visible", timeout=20000)
        except Exception:
            raise AssertionError("The attempt did not reach the summary page")
        actual = rows.count()
        print("The summary of attempt lists %d question(s)" % actual)
        if expected_count is not None:
            assert actual == expected_count, (
                "Expected %d questions on the summary but it lists %d"
                % (expected_count, actual))
        attach_screenshot(self.page, "Summary of attempt")

    def click_finish_attempt(self):
        """Reach the summary of attempt.

        answer_all_questions already pages through the last question, so the
        summary is usually up by the time this runs; the button is only clicked
        when it is not.
        """
        frame = self._quiz_frame()
        if self._is_visible(TA.QUIZ_SUMMARY_TABLE, timeout=5000, target=frame):
            print("Already on the summary of attempt")
            return
        if not self._click_if_present(TA.NEXT_OR_FINISH_ATTEMPT_BUTTON,
                                      "the 'Finish attempt ...' button",
                                      timeout=8000, target=frame):
            raise AssertionError("The 'Finish attempt ...' button was not found")
        self.page.wait_for_timeout(6000)
        self._quiz_frame_ref = self._frame_matching("lms.", "/mod/")

    def click_submit_all_and_finish(self):
        frame = self._quiz_frame()
        self._click(TA.SUBMIT_ALL_AND_FINISH_BUTTON, "the 'Submit all and finish' button",
                    target=frame, timeout=15000)
        self.page.wait_for_timeout(3000)
        attach_screenshot(self.page, "Submit confirmation")

    def click_submit_all_and_finish_in_popup(self):
        frame = self._quiz_frame()
        self._click(TA.SUBMIT_CONFIRM_SUBMIT_BUTTON,
                    "the 'Submit all and finish' button in the popup",
                    target=frame, timeout=15000)
        self.page.wait_for_timeout(12000)
        self._quiz_frame_ref = self._frame_matching("lms.", "/mod/")
        self._report_unrecognised_questions()
        attach_screenshot(self.page, "Quiz score page")

    # ==================================================================
    # Assessment - score page
    # ==================================================================

    def _report_unrecognised_questions(self):
        """Print, paste-ready, the answers the review page reveals.

        Moodle's review shows "The correct answer is: ..." for every question,
        so anything the key did not recognise can be added to _ANSWER_KEY from
        the run's own output instead of another manual pass over the bank.
        """
        if not self._unrecognised_questions:
            return
        frame = self._quiz_frame()
        questions = frame.locator(TA.QUESTION_CONTAINER)
        learned = []
        for i in range(questions.count()):
            que = questions.nth(i)
            try:
                text = _norm(que.locator(TA.QUESTION_TEXT).first.inner_text())
            except Exception:
                continue
            if not any(_slug(text) == _slug(u) for u in self._unrecognised_questions):
                continue
            node = que.locator(TA.RIGHT_ANSWER_TEXT)
            if not node.count():
                continue
            revealed = re.sub(r"^The correct answers? (?:are|is):\s*", "",
                              _norm(node.first.inner_text()))
            learned.append((text, revealed))
        if not learned:
            return
        print("\nAdd these to ThinkActivityPage._ANSWER_KEY so the next run scores them:")
        for question, answer in learned:
            print('        "%s":\n            "%s",' % (question, answer))
        print("")

    def _read_score_stats(self):
        if self._score_stats:
            return self._score_stats
        frame = self._quiz_frame()
        stats = {}
        for name in ("total", "answered", "notanswered", "correct", "partial", "incorrect"):
            try:
                stats[name] = int(self._text_of(TA.QUIZ_STAT_VALUE.format(name),
                                                target=frame, timeout=10000))
            except Exception:
                stats[name] = None
        try:
            stats["score"] = self._text_of(TA.QUIZ_SCORE_VALUE, target=frame)
            stats["percent"] = self._text_of(TA.QUIZ_SCORE_PERCENT, target=frame)
        except Exception:
            stats["score"] = stats["percent"] = None
        print("Quiz score page: %s" % stats)
        self._score_stats = stats
        return stats

    def _validate_score_page_stat(self, description):
        name = self._SCORE_PAGE_STATS[description]
        stats = self._read_score_stats()
        value = stats.get(name)
        assert value is not None, "The score page does not show the %s" % description

        # Cross-check the tile against the rest of the page rather than only
        # asserting that a number rendered.
        total, answered = stats.get("total"), stats.get("answered")
        not_answered = stats.get("notanswered")
        graded = [stats.get(k) for k in ("correct", "partial", "incorrect")]
        if name == "total" and self._questions_seen:
            assert value == self._questions_seen, (
                "The score page reports %s questions but the attempt had %s"
                % (value, self._questions_seen))
        if name == "answered" and None not in (total, not_answered):
            assert answered + not_answered == total, (
                "answered (%s) + not answered (%s) != total (%s)"
                % (answered, not_answered, total))
        if name in ("correct", "partial", "incorrect") and None not in graded \
                and answered is not None:
            assert sum(graded) == answered, (
                "correct+partial+incorrect (%s) != answered (%s)" % (sum(graded), answered))
        print("Validated the %s: %s" % (description, value))

    def _validate_quiz_overall_score(self):
        """Validate the score, and that it clears the certificate threshold."""
        stats = self._read_score_stats()
        percent, score = stats.get("percent"), stats.get("score")
        assert percent, "The score page does not show a percentage"
        value = int(re.sub(r"[^0-9]", "", percent) or 0)
        print("Validated the overall score: %s (%s)" % (score, percent))
        assert value >= CERTIFICATE_PASS_PERCENT, (
            "The attempt scored %s, below the %d%% the certificate needs. Questions "
            "missing from the answer key this run: %s"
            % (percent, CERTIFICATE_PASS_PERCENT,
               self._unrecognised_questions or "none"))

    def click_finish_review(self):
        frame = self._quiz_frame()
        self._click(TA.FINISH_REVIEW_LINK, "the 'Finish review' link",
                    target=frame, timeout=15000)
        self.page.wait_for_timeout(8000)
        self._quiz_frame_ref = self._frame_matching("lms.", "/mod/")
        attach_screenshot(self.page, "Back on the assessment page")

    def verify_back_on_assessment(self):
        """Assert the review handed back to the assessment's own page."""
        frame = self._quiz_frame(capture=False)
        if not self._is_visible(TA.QUIZ_INFO_BOX, timeout=15000, target=frame):
            raise AssertionError(
                "The Assessment page did not render after finishing the review")
        print("Back on the Assessment page")
        attach_screenshot(self.page, "Assessment page")

    def click_assessment_back_arrow(self):
        """Leave the assessment lesson via its breadcrumb back arrow."""
        if not self._click_if_present(TA.LESSON_BACK_ARROW,
                                      "the Assessment back arrow", timeout=12000):
            print("No back arrow on this screen - navigating back to the course instead")
            self.return_to_course()
            return
        self.page.wait_for_timeout(6000)
        self._dismiss_app_update_modal()
        self._quiz_frame_ref = None
        attach_screenshot(self.page, "Left the assessment")

    # ==================================================================
    # button routing
    # ==================================================================

    def click_button(self, label):
        """Route 'the user clicks on the "X" button' to the right document.

        The same wording covers buttons on the WSN page, inside the Think
        activity's iframe and inside the Moodle quiz's iframe, so the label is
        what decides which one is meant.
        """
        handlers = {
            "Enroll Now": self.click_enroll_now,
            "Submit": self.click_think_submit,
            "Finish": self.click_think_finish,
            "Attempt quiz": self.start_quiz_attempt,
            "Finish attempt": self.click_finish_attempt,
            "Submit all and finish": self.click_submit_all_and_finish,
            "Finish review": self.click_finish_review,
        }
        handler = handlers.get(label)
        if handler:
            handler()
            return
        page_buttons = {
            "Not now": TA.VALIDATE_NOT_NOW_BUTTON,
            "Start Course": TA.START_COURSE_BUTTON,
        }
        locator = page_buttons.get(label)
        if not locator:
            raise ValueError("No locator mapped for the '%s' button" % label)
        self._click(locator, "the '%s' button" % label)
        self.page.wait_for_timeout(2500)

    def click_popup_button(self, label):
        """'the user clicks on the "X" button in the popup'."""
        handlers = {
            "Enroll Now": self.click_enroll_now_in_popup,
            "Submit all and finish": self.click_submit_all_and_finish_in_popup,
        }
        handler = handlers.get(label)
        if not handler:
            raise ValueError("No popup handler mapped for the '%s' button" % label)
        handler()
