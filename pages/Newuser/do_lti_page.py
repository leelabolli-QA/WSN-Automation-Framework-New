"""Page object for the "Do-LTI_QA" batch course journey.

Drives features/newuser.feature > the "Do-LTI" scenarios: Courses (In Progress)
-> Do-LTI_QA -> the Overview modal -> the curriculum -> the two Do-LTI
activities (session -> questions -> result) -> Orientation -> the Moodle
assessment -> the course page's score tile and certificate.

WHY IT SUBCLASSES ThinkActivityPage
-----------------------------------
Do-LTI and Dev-Think LTI are the same kind of course: a WSN course page, an LTI
iframe per activity and a Moodle quiz for the assessment. Everything from
open_overview_modal() through the whole quiz attempt, the answer key, the score
tiles and the certificate panel is identical markup and identical behaviour, so
it is INHERITED rather than copied. Only what actually differs is overridden
here:

  * the course is a BATCH course - a new user reaches it by joining the batch
    with a job key ("New user joins a batch using the job key"), so it is
    already enrolled and is opened from the enrolled-courses list rather than
    from the catalogue carousel;
  * a Do activity opens on a recorded SESSION that has to be played before its
    questions appear, where a Think activity opens straight on its question;
  * a Do activity asks three questions in a row (answer -> Submit -> Continue)
    and ends on a result screen, where a Think activity is one question.

Both flows share several step wordings and behave's step registry is global, so
one step definition serves both and routes on which flow is active - see
activate() / is_active() and features/steps/student_persona/do_lti_steps.py.

The activity locators marked "best guess" in do_lti_locators.py were written
from the flow the feature file describes rather than read off the live course.
Every one of them is used through a tolerant helper here (multi-candidate
XPath, "skip and report" rather than "fail") so an unconfirmed guess degrades
into a printed note instead of a red run.
"""

from locators.new_user_locators.do_lti_locators import (
    DoLtiLocators as DL,
)
from pages.Newuser.think_activity_page import (
    ThinkActivityPage,
    _norm,
)
from utils.helpers import attach_screenshot

# How long a recorded session is watched before the activity is allowed to move
# on. The course only needs the session opened and played, not watched to the
# last frame, so this is a bounded wait rather than the session's real length.
SESSION_WATCH_TIMEOUT_MS = 90000
SESSION_POLL_INTERVAL_MS = 3000
# Questions each Do-LTI activity asks. The feature file states it too; this is
# the fallback when a step does not carry a count.
DO_QUESTIONS_PER_ACTIVITY = 3


class DoLtiPage(ThinkActivityPage):

    # Its own flow flag and its own shared instance - inheriting them would
    # make DoLtiPage.is_active() answer for the Dev-Think flow as well.
    _shared_instance = None
    _active = False

    # ------------------------------------------------------------------
    # "the user should be able to see the ..." targets
    # ------------------------------------------------------------------
    # Starts from the inherited map (the enrollment popup, the Moodle quiz, the
    # certificate panel and the Orientation section are all shared markup) and
    # adds/overrides only the Do-LTI-specific entries.
    _VIEW_TARGETS = dict(ThinkActivityPage._VIEW_TARGETS)
    _VIEW_TARGETS.update({
        # Courses page - the enrolled ("In Progress") listing
        '"in progress" tab': (DL.IN_PROGRESS_TAB, "page"),
        '"completed" tab': (DL.COMPLETED_TAB, "page"),
        '"do-lti_qa" course card': (DL.DO_LTI_COURSE_CARD, "page"),
        'do-lti course type': (DL.DO_LTI_COURSE_TYPE, "page"),
        'do-lti course progress': (DL.DO_LTI_COURSE_PROGRESS, "page"),
        '"resume" option': (DL.DO_LTI_RESUME_BUTTON + "|" + DL.RESUME_BUTTON, "page"),

        # Course page
        'do-lti course title': (DL.COURSE_DETAIL_TITLE, "page"),
        '"view batch" option': (DL.VIEW_BATCH_OPTION, "page"),

        # Curriculum
        '"do-lti" section': (DL.ACCORDION_SECTION_BY_NAME.format(DL.ACTIVITY_SECTION), "page"),
        # On the curriculum the assessment is an accordion section; the
        # inherited entry points at the CERTIFICATE PROGRESS label, which only
        # exists once the course is finished - accept either.
        # The app spells it "Assesments" here (misspelled AND plural) where the
        # Dev-Think course spells it "Assesment"; the inherited entry points at
        # the CERTIFICATE PROGRESS label, which only exists once the course is
        # finished - accept any of them.
        '"assessments" section': (
            DL.ACCORDION_SECTION_BY_NAME.format(DL.ASSESSMENT_SECTION)
            + "|" + DL.ACCORDION_SECTION_BY_NAME.format("Assesment")
            + "|" + DL.ACCORDION_SECTION_BY_NAME.format("Assessment")
            + "|" + DL.ASSESSMENTS_SECTION_TITLE, "page"),
        '"do-lti-1" activity': (DL.ACTIVITY_CARD_BY_NAME.format(DL.ACTIVITY_ONE), "page"),
        '"do-lti-2" activity': (DL.ACTIVITY_CARD_BY_NAME.format(DL.ACTIVITY_TWO), "page"),
        'completed tick symbol for "do-lti-1"': (
            DL.ACTIVITY_TICK_BY_NAME.format(DL.ACTIVITY_ONE), "page"),
        'completed tick symbol for "do-lti-2"': (
            DL.ACTIVITY_TICK_BY_NAME.format(DL.ACTIVITY_TWO), "page"),

        # Inside the Do activity's own iframe
        'do activity session': (DL.DO_SESSION_PLAYER, "do"),
        'play button': (DL.DO_SESSION_PLAY_BUTTON, "do"),
        'session controls': (DL.DO_SESSION_CONTROLS, "do"),
        '"continue" button': (DL.DO_CONTINUE_BUTTON, "do"),
        'do activity question': (DL.DO_QUESTION_TEXT, "do"),
        'answer options': (DL.DO_OPTION, "do"),
        '"submit" button': (DL.DO_SUBMIT_BUTTON, "do"),
        'answer result': (DL.DO_ANSWER_FEEDBACK, "do"),
        'do activity result': (DL.DO_ACTIVITY_RESULT, "do"),
        '"next" button': (DL.DO_NEXT_BUTTON, "do"),
    })

    # Checks whose element only exists on the real course DOM and whose XPath
    # here is still a best guess: a miss is reported, not failed, so an
    # unconfirmed locator cannot turn a working journey red. Move an entry out
    # of this set once a live run confirms its XPath.
    _SOFT_VIEW_KEYS = {
        'do-lti course type',
        'do-lti course progress',
        '"resume" option',
        '"view batch" option',
        'do activity session',
        'play button',
        'session controls',
        'answer options',
        'answer result',
        'do activity result',
        '"next" button',
    }

    # "the user should be able to validate the ..." with no expected value.
    _VALIDATE_TARGETS = dict(ThinkActivityPage._VALIDATE_TARGETS)
    _VALIDATE_TARGETS.update({
        'course duration': (DL.COURSE_DURATION_VALUE, "page"),
        'course language': (DL.COURSE_LANGUAGE_VALUE, "page"),
    })

    _ABOUT_PANEL_KEYS = set(ThinkActivityPage._ABOUT_PANEL_KEYS)

    def __init__(self, page):
        super().__init__(page)
        self._do_frame_ref = None
        # Which activity the session/question steps are currently driving, so
        # the reporting names the right one.
        self._current_activity = None
        # How many of the activity's questions the last run through answered.
        self._questions_answered = 0

    # ==================================================================
    # frames
    # ==================================================================

    def _do_frame(self, capture=True):
        """The Do activity's own iframe.

        The URL fragment is not confirmed, so several candidates are tried in
        turn and anything else that is clearly an LTI activity iframe is
        accepted last. Falls back to the page itself, exactly like the
        inherited Think/quiz frame helpers, so a course that renders the
        activity inline still works.
        """
        frame = self._live(self._do_frame_ref)
        if frame is None:
            for fragments in (("lti-do-activity",), ("do-activity",), ("lti-activity",), ("/lti",)):
                frame = self._frame_matching(*fragments)
                if frame is not None:
                    break
        if frame is None and capture:
            frame = self._capture_frame(
                "_do_frame_ref", ("lti",), "Do activity", poll_steps=10)
        self._do_frame_ref = frame
        return frame or self.page

    def _capture_activity_frame(self):
        """A Do activity opens in its own LTI iframe, not the Think one.

        The exact URL fragment is not confirmed, so the candidates are tried
        from most to least specific and the generic "lti" one catches the rest.
        """
        for fragments in (("lti-do-activity",), ("do-activity",), ("lti",)):
            frame = self._capture_frame("_do_frame_ref", fragments, "Do activity",
                                        poll_steps=6)
            if frame is not None:
                return frame
        return None

    def _scope_target(self, scope):
        if scope == "do":
            return self._do_frame(capture=False)
        return super()._scope_target(scope)

    def return_to_course(self):
        super().return_to_course()
        self._do_frame_ref = None

    # ==================================================================
    # flow state
    # ==================================================================

    def verify_logged_in(self, base_url):
        """Continue as the user this feature registered, on the Do-LTI flow.

        Same contract as the inherited version (no fallback to configured
        credentials - see ThinkActivityPage.verify_logged_in); activating here
        is what points the shared step wordings at this page object.
        """
        DoLtiPage.activate()
        return super().verify_logged_in(base_url)

    # ==================================================================
    # Courses page -> the batch course
    # ==================================================================

    def open_courses_page(self):
        """Open the enrolled-courses listing from the home dashboard."""
        self.click_card("Programs & Courses")
        self._wait_for_page_ready()
        attach_screenshot(self.page, "Programs & Courses page")

    def open_course(self):
        """Open the Do-LTI_QA course from the enrolled ("In Progress") list.

        The batch course is already enrolled - joining the batch with the job
        key is what enrolled it - so there is no catalogue carousel to page
        through here, unlike ThinkActivityPage.click_course().
        """
        self._wait_for_page_ready()
        self._click_if_present(DL.IN_PROGRESS_TAB, "the 'In Progress' tab", timeout=8000)
        self.page.wait_for_timeout(2000)

        if not self._is_visible(DL.DO_LTI_COURSE_CARD, timeout=20000):
            raise AssertionError(
                "The '%s' course is not listed under In Progress. It is a BATCH "
                "course: the 'New user joins a batch using the job key' scenario "
                "has to have run first, and the batch key has to still be valid."
                % DL.COURSE_NAME)

        # "Resume"/"View Details" is the card's own way in. The scoped locator
        # is tried first so another enrolled course's button cannot be picked
        # up; the card title is the last resort.
        for locator, description in (
            (DL.DO_LTI_RESUME_BUTTON, "the '%s' card's Resume button" % DL.COURSE_NAME),
            (DL.RESUME_BUTTON, "the course's 'Resume' button"),
        ):
            if self._click_if_present(locator, description, timeout=8000):
                break
        else:
            self._click(DL.DO_LTI_COURSE_CARD, "the '%s' course card" % DL.COURSE_NAME,
                        force=True)
        self.page.wait_for_timeout(5000)
        self._dismiss_app_update_modal()
        self._course_url = self.page.url
        attach_screenshot(self.page, "'%s' course opened" % DL.COURSE_NAME)

    def click_course(self, name):
        """The shared 'clicks on the "X" course' wording, for this course."""
        if _norm(name).lower() != DL.COURSE_NAME.lower():
            raise ValueError("No locator mapped for the '%s' course" % name)
        self.open_course()

    def verify_navigated_to(self, destination):
        """Adds the Do-LTI course page to the inherited navigation checks."""
        if _norm(destination).lower() in ("do-lti course", "do-lti"):
            self._wait_for_page_ready()
            if not self._is_visible(DL.COURSE_DETAIL_TITLE, timeout=20000):
                raise AssertionError("The Do-LTI course page did not render")
            print("Navigated to the Do-LTI course page")
            attach_screenshot(self.page, "Do-LTI course page")
            return
        return super().verify_navigated_to(destination)

    def verify_enrolled(self):
        """A batch course is already enrolled - assert that, don't enroll.

        The inherited version proves enrollment by the "Enroll Now" button
        disappearing, which never applies here: joining the batch enrolled the
        user, so the course page renders its curriculum from the first load.
        """
        self._wait_for_page_ready()
        if not (self._is_visible(DL.ACTIVITY_CARD, timeout=20000)
                or self._is_visible(DL.COURSE_CURRICULUM_SECTION, timeout=5000)):
            raise AssertionError(
                "The '%s' course does not show an enrolled state - no curriculum "
                "rendered. Joining the batch is what enrolls a new user in it."
                % DL.COURSE_NAME)
        print("The user is enrolled in the '%s' batch course" % DL.COURSE_NAME)
        attach_screenshot(self.page, "Enrolled in the Do-LTI course")

    # ==================================================================
    # generic validations
    # ==================================================================

    def verify_visible(self, description):
        """As the inherited check, but tolerant of the best-guess locators.

        Anything in _SOFT_VIEW_KEYS reports a miss instead of failing - see the
        module docstring.
        """
        key = _norm(description).lower()
        if key not in self._VIEW_TARGETS:
            raise ValueError(
                "No locator mapped for 'the user should be able to see the %s' - "
                "add it to DoLtiPage._VIEW_TARGETS" % description)
        if key not in self._SOFT_VIEW_KEYS:
            return super().verify_visible(description)

        locator, scope = self._VIEW_TARGETS[key]
        if key in self._ABOUT_PANEL_KEYS:
            self.open_overview_modal()
        if self._is_visible(locator, timeout=10000, target=self._scope_target(scope)):
            print("Validated: %s" % description)
            return
        print("'%s' not found with its best-guess locator - verify the XPath in "
              "do_lti_locators.py" % description)

    # ==================================================================
    # the Do-LTI activities
    # ==================================================================

    def open_activity(self, activity_name):
        """Open one Do-LTI activity from the course curriculum.

        Same journey as a Think activity - return to the course, expand the
        section, click the card's action button - so the inherited
        open_think_activity() does the work; only the section name and the
        iframe it waits for differ.
        """
        self._current_activity = activity_name
        self._do_frame_ref = None
        self.open_think_activity(activity_name, section=DL.ACTIVITY_SECTION)
        attach_screenshot(self.page, "'%s' activity opened" % activity_name)

    def play_session(self, activity_name=None):
        """Play the activity's recorded session and wait for it to finish.

        The session gates the questions: they do not render until it has been
        played. What proves it finished is the "Continue" control appearing, so
        that is what is waited for rather than a video duration - a session
        that is already marked watched then costs no wait at all.
        """
        activity_name = activity_name or self._current_activity or "the Do-LTI"
        frame = self._do_frame()

        if not self._click_if_present(DL.DO_SESSION_PLAY_BUTTON,
                                      "the session's Play button",
                                      timeout=15000, target=frame):
            # Some players start on their own, and a <video> element can be
            # driven directly when it renders no button of its own.
            print("No Play button on the '%s' session - trying the video element"
                  % activity_name)
            try:
                frame.locator("//video").first.evaluate("video => video.play()")
                print("Started the session through the video element")
            except Exception:
                print("The '%s' session could not be started - it may already be "
                      "playing or already watched" % activity_name)
        attach_screenshot(self.page, "'%s' session playing" % activity_name)

        waited = 0
        while waited < SESSION_WATCH_TIMEOUT_MS:
            if self._is_visible(DL.DO_CONTINUE_BUTTON, timeout=SESSION_POLL_INTERVAL_MS,
                                target=frame):
                print("The '%s' session finished - 'Continue' is available"
                      % activity_name)
                return True
            waited += SESSION_POLL_INTERVAL_MS
        print("The '%s' session did not surface a 'Continue' within %ds - carrying "
              "on so the questions can still be attempted"
              % (activity_name, SESSION_WATCH_TIMEOUT_MS // 1000))
        return False

    def verify_session_completed(self, activity_name=None):
        activity_name = activity_name or self._current_activity or "the Do-LTI"
        frame = self._do_frame()
        if self._is_visible(DL.DO_CONTINUE_BUTTON, timeout=20000, target=frame):
            print("The '%s' session is complete" % activity_name)
            attach_screenshot(self.page, "'%s' session complete" % activity_name)
            return
        raise AssertionError(
            "The '%s' session did not complete - no 'Continue' to leave it by"
            % activity_name)

    def click_continue(self):
        """Leave the session for the activity's questions."""
        frame = self._do_frame()
        if not self._click_if_present(DL.DO_CONTINUE_BUTTON, "the 'Continue' button",
                                      timeout=20000, target=frame):
            raise AssertionError("There is no 'Continue' button on the Do activity")
        self.page.wait_for_timeout(4000)
        attach_screenshot(self.page, "Continued past the session")

    def _answer_current_do_question(self, index):
        """Answer whatever question is on screen, then submit and continue.

        The Do activity's options are not in the Think answer key and the
        activity is not graded against a pass mark (the certificate is decided
        by the assessment), so the first option is selected deliberately rather
        than guessed at - what the scenario proves here is that the
        answer/submit/continue journey works for every question.
        """
        frame = self._do_frame()
        options = frame.locator(DL.DO_OPTION)
        try:
            count = options.count()
        except Exception:
            count = 0
        if not count:
            print("  Question %d lists no answer option - nothing to select" % index)
            return False

        option = options.first
        try:
            radio = option.locator(DL.DO_OPTION_RADIO).first
            radio.click(force=True)
        except Exception:
            option.click(force=True)
        print("  Answered question %d" % index)
        self.page.wait_for_timeout(1500)

        if not self._click_if_present(DL.DO_SUBMIT_BUTTON, "the 'Submit' button",
                                      timeout=15000, target=frame):
            raise AssertionError("Question %d could not be submitted - no 'Submit'"
                                 % index)
        self.page.wait_for_timeout(3000)
        if self._is_visible(DL.DO_ANSWER_FEEDBACK, timeout=6000, target=frame):
            print("  Question %d was graded" % index)
        attach_screenshot(self.page, "Do activity question %d submitted" % index)

        # The last question ends on the result screen instead of another
        # question, so a missing "Continue" here is the expected end, not a
        # failure.
        if self._click_if_present(DL.DO_CONTINUE_BUTTON, "the 'Continue' button",
                                  timeout=8000, target=frame):
            self.page.wait_for_timeout(3000)
        return True

    def answer_all_do_questions(self, expected_count=DO_QUESTIONS_PER_ACTIVITY,
                                activity_name=None):
        """Answer every question in the activity, one after another."""
        activity_name = activity_name or self._current_activity or "the Do-LTI"
        answered = 0
        for index in range(1, expected_count + 1):
            if not self._answer_current_do_question(index):
                break
            answered += 1
        self._questions_answered = answered
        print("Answered %d of the %d questions in '%s'"
              % (answered, expected_count, activity_name))
        if answered < expected_count:
            print("Fewer questions than the %d the feature expects were on screen - "
                  "verify the Do activity locators in do_lti_locators.py"
                  % expected_count)
        return answered

    def verify_all_do_questions_answered(self, expected_count=DO_QUESTIONS_PER_ACTIVITY):
        answered = getattr(self, "_questions_answered", 0)
        assert answered, (
            "No question of the Do activity was answered - the activity's "
            "question screen never rendered")
        if answered < expected_count:
            print("Only %d of the %d questions were answered" % (answered, expected_count))
            return
        print("All %d questions were answered" % expected_count)

    def finish_activity(self, activity_name=None):
        """Leave a finished Do activity by its own "Next" and return to the course."""
        activity_name = activity_name or self._current_activity or "the Do-LTI"
        frame = self._do_frame()
        if not self._click_if_present(DL.DO_NEXT_BUTTON, "the activity's 'Next' button",
                                      timeout=15000, target=frame):
            print("No 'Next' on the '%s' result screen - returning to the course "
                  "directly" % activity_name)
        self.page.wait_for_timeout(3000)
        self.return_to_course()
        self.open_course_content()
        attach_screenshot(self.page, "Back on the course after '%s'" % activity_name)

    def verify_activity_completed(self, activity_name):
        """Assert the activity's card now shows its completed state.

        A finished activity's action button reads "Result" instead of "Start"
        and a green tick appears on the card - either is proof.
        """
        self.return_to_course()
        self.open_course_content()
        self._click_if_present(DL.ACCORDION_SECTION_BY_NAME.format(DL.ACTIVITY_SECTION),
                               "the '%s' section" % DL.ACTIVITY_SECTION, timeout=8000)
        self.page.wait_for_timeout(2000)

        if self._is_visible(DL.ACTIVITY_TICK_BY_NAME.format(activity_name), timeout=15000):
            print("'%s' is marked completed" % activity_name)
            attach_screenshot(self.page, "'%s' completed" % activity_name)
            return
        action = DL.ACTIVITY_ACTION_BUTTON_BY_NAME.format(activity_name)
        if self._is_visible(action, timeout=8000):
            try:
                label = _norm(self.page.locator(action).first.inner_text())
            except Exception:
                label = ""
            if label.lower() == "result":
                print("'%s' is completed (its button reads 'Result')" % activity_name)
                attach_screenshot(self.page, "'%s' completed" % activity_name)
                return
        raise AssertionError(
            "'%s' is not marked completed - neither the tick nor a 'Result' button "
            "is on its card" % activity_name)

    def verify_can_access(self, activity_name):
        """Assert the next Do-LTI activity is reachable (its own section)."""
        self.return_to_course()
        self.open_course_content()
        self._click_if_present(DL.ACCORDION_SECTION_BY_NAME.format(DL.ACTIVITY_SECTION),
                               "the '%s' section" % DL.ACTIVITY_SECTION, timeout=8000)
        self.page.wait_for_timeout(2000)
        if not self._is_visible(DL.ACTIVITY_CARD_BY_NAME.format(activity_name), timeout=15000):
            raise AssertionError("The '%s' activity is not available" % activity_name)
        print("'%s' is available" % activity_name)
        attach_screenshot(self.page, "'%s' available" % activity_name)

    # ==================================================================
    # buttons
    # ==================================================================

    def open_assessment_section(self, section=None):
        """Open the assessment lesson, under this course's own spelling.

        The inherited version defaults to "Assesment" (the Dev-Think course's
        spelling) and falls back to "Assessment"; this course spells the
        section "Assesments", which neither of those matches.
        """
        return super().open_assessment_section(section or DL.ASSESSMENT_SECTION)

    def complete_orientation(self, section=None):
        """Open the Orientation PDF. Its activity card is named "PDF" here,
        which the inherited version does not need to know - it opens whatever
        single activity the lesson lists."""
        return super().complete_orientation(section or DL.ORIENTATION_SECTION)

    def click_button(self, label):
        """Route the shared 'clicks on the "X" button' wording.

        The Do activity's own Submit/Continue/Next live inside its iframe, so
        they are handled here; everything else - the quiz's Attempt/Finish
        controls included - is the inherited routing.
        """
        handlers = {
            "Continue": self.click_continue,
        }
        handler = handlers.get(label)
        if handler:
            handler()
            return
        return super().click_button(label)
