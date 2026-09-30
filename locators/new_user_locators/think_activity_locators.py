class ThinkActivityLocators:
    EXPLORE_THINGS_TO_DO_HEADING = "//h4[text()='Explore things to do']"
    COURSES_AND_PROGRAMS_HEADING = "//h6[text()='Programs & Courses']"
    JOBS_CONNECT_HEADING = "//h6[text()='Jobs Connect']"
    MY_CAREER_ADVISOR_HEADING = "//h6[text()='My Career Advisor']"
    PERSONAL_PITCH_TRAINER_HEADING = "//h6[text()='Personal Pitch Trainer']"
    INTERVIEW_COACH_HEADING = "//h6[text()='Interview Coach']"
    CAREER_BUDDY_HEADING = "//h6[text()='Career Buddy']"
    FORUMS_HEADING = "//h6[text()='Forums']"
    # The courses listing is its own route now (/en/course-program-list) with a
    # page title instead of the old "Courses offered by wadhwani foundation"
    # heading, which the redesign removed.
    COURSES_OFFERED_BY_WADHWANI_FOUNDATION_HEADING = (
        "//h1[contains(@class,'subpage-back-header__title')]"
        "[normalize-space()='Programs & Courses']"
    )
    COURSES_LIST_TAB = "//button[contains(@class,'programs-and-courses__tab')]"
    LEARNING_ITEM_CARD_TITLE = "//h4[contains(@class,'learning-item-card__title')]"
    LEARNING_ITEM_CARD_BY_NAME = (
        "//h4[contains(@class,'learning-item-card__title')][normalize-space()=\"{}\"]"
    )
    CAROUSEL_RIGHT_ARROW_BUTTON = "//button[@class='react-multiple-carousel__arrow react-multiple-carousel__arrow--right ']"
    DEV_THINK_LTI_OPEN_HEADING = "//h4[text()='Dev-Think LTI-Open']"

    # --- Course detail header --------------------------------------------
    # The Overview / Course Content / Performance tabs are gone: the course is
    # one scrolling page whose "Overview" (duration, language, About this
    # course) now opens as a modal from the (i) trigger beside the title.
    COURSE_DETAIL_TITLE = "//h1[contains(@class,'subpage-back-header__title')]"
    COURSE_OVERVIEW_INFO_TRIGGER = "//button[@data-testid='course-details.header.overview-trigger']"
    COURSE_OVERVIEW_MODAL = "//div[contains(@class,'course-details-header__overview-modal')]"
    VALIDATE_OVERVIEW = "//div[contains(@class,'ant-modal-title')][normalize-space()='Overview']"
    COURSE_OVERVIEW_MODAL_CLOSE = (
        "//div[contains(@class,'course-details-header__overview-modal')]"
        "//button[contains(@class,'responsive-drawer__close')]"
    )
    # The About panel renders inline on an un-enrolled course and inside the
    # Overview modal once enrolled - the same markup either way.
    ABOUT_COURSE_PANEL = "//section[contains(@class,'about-course-panel')]"
    COURSE_BANNER_IMAGE = "//img[contains(@class,'about-course-panel__thumb')]"
    VALIDATE_ABOUT_THIS_COURSE = (
        "//h5[contains(@class,'about-course-panel__title')]"
        "[normalize-space()='About this course']"
    )
    VALIDATE_LANGUAGE = "//span[@data-testid='course-details.about.language']"
    VALIDATE_DURATION = "//span[@data-testid='course-details.about.duration']"
    COURSE_INCLUDES_ITEM = "//span[contains(@class,'about-course-panel__includes-item')]"

    # --- Enrollment -------------------------------------------------------
    # The button kept its label but is now an ant-btn carrying enroll_now_btn.
    ENROLL_NOW_BUTTON = "//button[normalize-space()='Enroll Now']"
    ENROLL_NOW_BUTTON_ON_COURSE = "//button[contains(@class,'enroll_now_btn')]"
    VALIDATE_NOT_NOW_BUTTON = "//button[normalize-space()='Not now']"
    ENROLL_NOW_BUTTON_2 = "(//button[normalize-space()='Enroll Now'])[2]"
    # No Course Content tab any more - the curriculum is a section of the page.
    VALIDATE_COURSE_CONTENT = "//div[contains(@class,'Detail-parentTab-wrapper')]"
    COURSE_CURRICULUM_SECTION = "//section[@id='course-details-toc']"
    OVERALL_SCORE = "//span[contains(@class,'scoreText')]"
    OVERALL_PROGRESS = "//span[contains(@class,'newAccor_header_status')]"
    VALIDATE_ORIENTATION = "(//p[text()='Orientation'])[2]"
    START_BUTTON = "//span[text()='Start']"
    ORIENTATION_BACK_BUTTON = "//img[@class='wf_image back-btn false no-js-ArrowLeftDark']"
    VALIDATE_DEV_THINK_LTI = "(//p[text()='Dev think LTI'])[2]"
    THINK_ACTIVITY_1_START_BUTTON = "//span[text()='Start']"
    SECOND_RADIO_INPUT = "(//input[@class='ant-radio-input'])[2]"
    SUBMIT_BUTTON = "//button[text()='Submit']"
    FINISH_BUTTON = "//button[text()='Finish']"
    ATTEMPT_QUIZ_BUTTON = "//button[text()='Attempt quiz']"
    NEXT_BUTTON = "//input[@value='Next']"
    FINISH_ATTEMPT_BUTTON = "//input[@value='Finish attempt ...']"
    SUBMIT_ALL_AND_FINISH_BUTTON = "//button[text()='Submit all and finish']"
    CANCEL_BUTTON_2 = "(//button[text()='Cancel'])[2]"
    SUBMIT_ALL_AND_FINISH_BUTTON_2 = "(//button[text()='Submit all and finish'])[2]"
    ORANGE_RIGHT_ARROW_IMAGE = "//img[@class='wf_image  no-js-Orange_rightArrow']"
    # There is no Performance tab any more. What it used to show - the score,
    # the certificate and its Download/Share actions - is on the course page
    # itself, in the completion panel. ("See Details in 'Performance' Tab" is a
    # plain div on the score tile and navigates nowhere.)
    PERFORMANCE_HEADING = "//div[contains(@class,'course-completion-panel')]"
    FINAL_SCORE = "//span[contains(@class,'scoreCount')]"
    DOWNLOAD_BUTTON = "//button[@data-testid='course-details.completion.download-certificate']"
    SHARE_BUTTON = "//button[contains(@class,'course-completion-panel__btn--outlined')]"
    VALIDATE_OVERALL_SCORE = "//span[contains(@class,'scoreText')]"
    VALIDATE_OVERALL_PROGRESS = "//span[contains(@class,'newAccor_header_status')]"

    # ==================================================================
    # Added for "User validates Dev-Think LTI course, completes Think
    # activities and assessment". Each XPath below covers something the
    # scenario asserts that had no locator yet; all were read off the live
    # dev course (/en/courses/698c62788eba20b5e4936809).
    # ==================================================================

    # --- "Application update is available" modal ------------------------
    # A deploy landing mid-run unmounts the SPA and blocks behind this modal:
    # the page is still there but #app is empty, so every later locator misses
    # for reasons that look nothing like the real cause. "Update" reloads.
    APP_UPDATE_MODAL_TITLE = (
        "//div[contains(@class,'ant-modal-title')]"
        "[contains(normalize-space(),'Application update is available')]"
    )
    APP_UPDATE_BUTTON = "//div[contains(@class,'ant-modal-footer')]//button[normalize-space()='Update']"

    # --- Home: counting the "Explore things to do" cards ----------------
    # A freshly registered user gets SEVEN; the grid hydrates in stages, so
    # count only once it has settled.
    EXPLORE_CARD_TITLE = "//h6[contains(@class,'new-student-dashboard__card-title')]"

    # --- Courses listing -------------------------------------------------
    # react-multi-carousel can render several copies of a card, and only those
    # in an item marked "--active" sit in the visible window; clicking any other
    # copy fails with "Element is outside of the viewport". The item is an <li>,
    # so match on any element carrying the class rather than on a div.
    DEV_THINK_LTI_OPEN_CARD_ACTIVE = (
        "//*[contains(@class,'react-multi-carousel-item--active')]"
        "//h4[text()='Dev-Think LTI-Open']"
    )
    # The page can hold more than one carousel, so page the one that actually
    # contains this card - the first arrow on the page usually belongs to
    # another strip. react-multi-carousel hides the left arrow at position 0,
    # which is where this course normally sits.
    DEV_THINK_CAROUSEL = (
        "//div[contains(@class,'react-multi-carousel-list')]"
        "[.//h4[text()='Dev-Think LTI-Open']]"
    )
    DEV_THINK_CAROUSEL_RIGHT_ARROW = (
        DEV_THINK_CAROUSEL + "//button[contains(@class,'react-multiple-carousel__arrow--right')]"
    )
    DEV_THINK_CAROUSEL_LEFT_ARROW = (
        DEV_THINK_CAROUSEL + "//button[contains(@class,'react-multiple-carousel__arrow--left')]"
    )

    # --- Values behind the "validate ... as" steps ------------------------
    # Duration and language are pills in the About panel; the language pill
    # reads "Language: English", so the page object strips the label.
    COURSE_DURATION_VALUE = "//span[@data-testid='course-details.about.duration']"
    COURSE_LANGUAGE_VALUE = "//span[@data-testid='course-details.about.language']"
    COURSE_DESCRIPTION = (
        "//div[contains(@class,'about-course-panel__description')]"
        "//div[contains(@class,'wf_markdown')]//p"
    )
    # The old course-level score/progress widgets went with the tabs. What the
    # page carries now is the assessment score tile and, per section, the
    # accordion's "n/m Lesson Completed" status.
    OVERALL_SCORE_VALUE = "//span[contains(@class,'scoreCount')]"
    OVERALL_PROGRESS_VALUE = "//span[contains(@class,'newAccor_header_status')]"
    ASSESSMENT_SCORE_TILE = "//span[contains(@class,'scoreCount')]"
    ASSESSMENT_SCORE_LABEL = "//span[contains(@class,'scoreText')]"
    ASSESSMENT_SCORE_SUBTEXT = "//span[contains(@class,'scoreSubText')]"
    # "See Details in 'Performance' Tab" - the way into the performance view.
    PERFORMANCE_DETAILS_BUTTON = "//div[contains(@class,'assessmentSummaryBtn')]"

    # --- Enrollment -------------------------------------------------------
    # REMOVED BY THE REDESIGN: there is no "Start Course" button any more, on
    # either state of the page - an enrolled course simply drops its Enroll Now
    # button and shows the curriculum, whose first activity carries "Start".
    # Kept so the wording still resolves; it will never match.
    START_COURSE_BUTTON = "//button[normalize-space()='Start Course']"

    # --- Course Content: accordion + activity cards -----------------------
    # NOTE the app spells the assessment section "Assesment".
    ACCORDION_SECTION_BY_NAME = "//h2[contains(@class,'newAccor_header')]//p[normalize-space()=\"{}\"]"
    ACCORDION_CHILD_BY_NAME = "//h5[contains(@class,'newAccor_children')]//p[normalize-space()=\"{}\"]"
    ACTIVITY_CARD = "//div[contains(@class,'activity_container')]"
    # A card's action button reads "Start" until the activity is finished and
    # "Result" afterwards; the green tick appears alongside once completed.
    ACTIVITY_CARD_BY_NAME = (
        "//div[contains(@class,'activity_container')]"
        "[.//span[contains(@class,'activity_name')][normalize-space()=\"{}\"]]"
    )
    ACTIVITY_ACTION_BUTTON_BY_NAME = ACTIVITY_CARD_BY_NAME + "//button"
    # The Orientation lesson holds a single PDF activity whose card name is not
    # needed - opening whatever activity the lesson lists is enough.
    ACTIVITY_ACTION_BUTTON = ACTIVITY_CARD + "//button"
    # The lesson page's breadcrumb back arrow. ORIENTATION_BACK_BUTTON above
    # pins the whole class string, which the Orientation lesson does not always
    # match; this one keys on the stable part and is what both the Orientation
    # and the Assessment lessons are left by. Its presence also proves the
    # activity really opened, since it only exists on the lesson page.
    LESSON_BACK_ARROW = "//img[contains(@class,'back-btn')]"
    ACTIVITY_TICK_BY_NAME = ACTIVITY_CARD_BY_NAME + "//img[contains(@class,'activityCheckIcon')]"

    # --- Lesson page -------------------------------------------------------
    # One-time "Review Your Certificate Name" prompt, raised the FIRST time a
    # user starts any activity - a brand-new registration meets it on think 1.
    CONFIRM_AND_CONTINUE_BUTTON = "//button[text()='Confirm & Continue']"

    # --- Think activity (inside the /en/lti-think-activity iframe) ---------
    # The activity is the WSN app's own React screen, not Moodle: ant-design
    # radios whose input @value IS the option text. The answer is matched on
    # that text, never on position, so the right option is chosen deliberately.
    THINK_QUESTION_TEXT = (
        "//div[contains(@class,'think-heading-question-section')]"
        "//div[contains(@class,'wf_markdown')]//p"
    )
    THINK_OPTION = "//div[contains(@class,'each-checkbox-option')]"
    # Relative sub-locators are chained onto an option element, and Playwright
    # only auto-detects XPath for selectors starting with "//" or ".." - a
    # ".//" one is parsed as CSS unless it says "xpath=".
    THINK_OPTION_TEXT = "xpath=.//span[contains(@class,'card-text')]"
    THINK_OPTION_RADIO = "xpath=.//input[contains(@class,'ant-radio-input')]"
    THINK_SUBMIT_BUTTON = "//button[contains(@class,'lti-activity-submit-button')]"
    THINK_SUCCESS_MESSAGE = (
        "//*[contains(normalize-space(),'Congratulations') or "
        "contains(normalize-space(),'successfully') or "
        "contains(normalize-space(),'Correct') or "
        "contains(normalize-space(),'Well done')]"
    )

    # ==================================================================
    # Moodle quiz - resolve ALL of these against the quiz iframe
    # ==================================================================
    # Present on the quiz landing page whatever the attempt state, so it is
    # what proves the review handed back to the assessment.
    QUIZ_INFO_BOX = "//div[contains(@class,'quizinfo')]"

    # <div id="question-7847-1" class="que multichoice deferredfeedback ...">
    QUESTION_CONTAINER = "//div[contains(concat(' ',normalize-space(@class),' '),' que ')]"
    QUESTION_TEXT = "xpath=.//div[contains(@class,'qtext')]"
    # Each option row is <div class="r0|r1"> holding the radio and its label.
    ANSWER_OPTION_ROW = "xpath=.//div[contains(@class,'answer')]/div[input[@type='radio']]"
    ANSWER_OPTION_RADIO = "xpath=.//input[@type='radio']"
    # One button per question however they are spread across pages, which is
    # how the attempt's question count is read.
    QUIZ_NAV_BUTTON = "//a[contains(@class,'qnbutton')]"
    # The Next control is an <input> whose value becomes "Finish attempt ..."
    # on the last question's page - matching on @name covers both.
    NEXT_OR_FINISH_ATTEMPT_BUTTON = "//input[@name='next']"

    QUIZ_SUMMARY_TABLE = "//table[contains(@class,'quizsummaryofattempt')]"
    QUIZ_SUMMARY_STATUS_CELL = "//table[contains(@class,'quizsummaryofattempt')]//td[contains(@class,'c1')]"
    # "Back" is an <a class="btn btn-secondary">, not a <button>.
    BACK_BUTTON = "//a[normalize-space()='Back']"

    # The confirmation modal holds exactly one Cancel and one confirm button,
    # both identified by data-action rather than by position.
    SUBMIT_CONFIRM_TITLE = "//h5[contains(@class,'modal-title')][normalize-space()='Submit all your answers and finish?']"
    SUBMIT_CONFIRM_CANCEL_BUTTON = "//div[contains(@class,'modal')]//button[@data-action='cancel']"
    SUBMIT_CONFIRM_SUBMIT_BUTTON = "//div[contains(@class,'modal')]//button[@data-action='save']"

    QUIZ_SCORE_TITLE = "//h3[contains(@class,'quizreviewsummary-title')]"
    QUIZ_SCORE_VALUE = "//div[contains(@class,'quizreviewsummary-scorevalue')]"
    QUIZ_SCORE_PERCENT = "//div[contains(@class,'quizreviewsummary-percent')]"
    # Stat tiles, formatted with one of: total / answered / notanswered /
    # correct / partial / incorrect.
    QUIZ_STAT_VALUE = (
        "//div[contains(@class,'quizreviewsummary-stat-{}')]"
        "//div[contains(@class,'quizreviewsummary-stat-value')]"
    )
    # "The correct answer is: ..." - revealed per question once the attempt is
    # graded, which is how a question missing from the answer key is reported.
    RIGHT_ANSWER_TEXT = "xpath=.//div[contains(@class,'rightanswer')]"
    FINISH_REVIEW_LINK = "//a[normalize-space()='Finish review']"

    # --- Certificate / completion panel (on the course page) ----------------
    # Earned state is now a panel headed "Congratulations !" with the
    # certificate preview, its Download/Share actions and a CERTIFICATE
    # PROGRESS strip; the old firstScenario-heading markup is gone.
    COURSE_COMPLETION_PANEL = "//div[contains(@class,'course-completion-panel')]"
    YOUR_CERTIFICATE_IS_AVAILABLE_SECTION = (
        "//h3[contains(@class,'course-completion-panel__title')]"
    )
    # "You've successfully earned your Wadhwani Foundation Certificate of
    # Completion."
    CERTIFICATE_ELIGIBILITY_MESSAGE = "//p[contains(@class,'course-completion-panel__lead')]"
    CERTIFICATE_REQUIREMENT_ITEM = "//span[contains(@class,'course-completion-panel__list-text')]"
    CERTIFICATE_PROGRESS_SECTION = "//section[contains(@class,'certificate-progress-section')]"
    CERTIFICATE_PROGRESS_NODE = "//button[contains(@class,'certificate-progress__node')]"
    EARNED_MICRO_CERTIFICATES_COUNT = "//h5[contains(@class,'earned-micro-certificates__count')]"
    ASSESSMENTS_SECTION_TITLE = (
        "//p[contains(@class,'certificate-progress__label-text')]"
        "[normalize-space()='Assessments']"
    )
    ASSESSMENT_NAME = "//span[contains(@class,'quizName_text')]"
    ASSESSMENT_SCORE = "//div[contains(@class,'score-tooltip-parent')]//span"
    ASSESSMENT_ATTEMPT_DATE = "//span[contains(@class,'attemptDate_text')]"
    ASSESSMENT_WEIGHTAGE_CELL = "//div[contains(@class,'assessment-table')]//tbody//tr/td[4]"
    ASSESSMENTS_PROGRESS_ARROW ="//span[@class='certificate-progress__label']"
    ASSESSMENTS_PROGRESS_ARROW_POPUP_CLOSE_BUTTON = (
        "//button[contains(@class,'popup-close-btn') "
        "and contains(@class,'responsive-drawer__close')]"
    )
    DOWNLOAD_CERTIFICATE_BUTTON="//button[normalize-space()='Download Certificate']"
    SHARE_CERTIFICATE_BUTTON="//button[normalize-space()='Share']"
    EARNED_MICRO_CERTIFICATES_CARD = "(//div[@class='earned-micro-certificates'])[1]"
    EARNED_MICRO_CERTIFICATE_ARROW = "button[aria-label='Earned Micro Certificates']"
    MICRO_CERTIFICATE_DOWNLOAD_BUTTON="//button[@aria-label='Download']"
    MICRO_CERTIFICATE_SHARE_BUTTON="//button[@aria-label='Share']"
    EARNED_MICRO_CERTIFICATE_CLOSE_ARROW="//button[@aria-label='Close']"