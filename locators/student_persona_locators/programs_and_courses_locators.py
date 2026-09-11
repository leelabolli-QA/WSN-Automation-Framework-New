"""Locators for the merged 'Programs & Courses' screen (/en/course-program-list).

The application used to have two separate dashboard cards - "Courses" and
"Programs" - each opening its own screen. They are now a single
"Programs & Courses" card opening one combined screen.

Both `CoursesPage` and `ProgramsPage` drive this screen, so the selectors that
describe it live here once. Each page object keeps its own locator class for
the parts specific to its scenario, so the two scenarios stay independent.

Element hooks preferred here, in order: the app's own ids
(`programs-and-courses.tab.*`), then BEM-ish class names
(`learning-item-card--enrolled`), then text. Positional indexes are avoided -
page objects resolve `.first` themselves.
"""


class ProgramsAndCoursesLocators:
    # --- entry point -------------------------------------------------------
    PROGRAMS_AND_COURSES_CARD = "//h6[text()='Programs & Courses']"

    # --- tabs (the app exposes real ids for these) -------------------------
    IN_PROGRESS_TAB = "//*[@id='programs-and-courses.tab.in-progress']"
    COMPLETED_TAB = "//*[@id='programs-and-courses.tab.completed']"

    ENROLLED_COURSE_CARD = "//div[contains(@class,'learning-item-card--enrolled')]"
    COMPLETED_COURSE_CARD = "//div[contains(@class,'learning-item-card--completed')]"
    RECOMMENDED_CARD = "//div[contains(@class,'learning-item-card--recommended')]"
    PROGRAM_CARD = "//div[contains(@class,'learning-item-card--program')]"
    # Courses and programs are listed side by side on the merged screen, so a
    # course-only title selector is needed to avoid opening a program by accident.
    COURSE_CARD_TITLE = "//h4[text()='QA-Emp skill Test-V2-Open']"

    RESUME_COURSE_BUTTON = ("//button[contains(@class,'learning-item-card__btn')]"
                            "[normalize-space()='Resume Course']")
    PRE_VIDEO_ICON = "//p[text()='Pre Video']"
    VALIDATE_PITCH_TRAINER_PRE_VIDEO_ICON = "(//p[text()='Pitch Trainer Pre Video'])[2]"
    POPUP_CLOSE_BUTTON = "//button[@class='popup-close-btn responsive-drawer__close']"
    COLLABORATE_ICON = "//p[text()='Collaborate']"
    POPUP_CLOSE_BUTTON = "//button[@class='popup-close-btn responsive-drawer__close']"
    ASSESSMENTS_ICON = "//p[text()='Assessments']"
    POPUP_CLOSE_BUTTON = "//button[@class='popup-close-btn responsive-drawer__close']"
    POST_VIDEO_ICON = "//p[text()='Post Video']"
    POPUP_CLOSE_BUTTON = "//button[@class='popup-close-btn responsive-drawer__close']"
    EARNED_MICRO_CERTIFICATES_GO_BUTTON = "//button[@class='earned-micro-certificates__go']"
    CERTIFICATION_CLOSE_BUTTON = "//button[@class='popup-close-btn responsive-drawer__close']"
    COURSE_BACK_BUTTON = "//button[@class='subpage-back-header__back-btn']"
    HPS_TEST_QA2_COURSE_TITLE = "//h4[text()=' HPS Test-QA2']"
    COURSE_COMPLETED_LABEL = "c"
    VALIDATE_SCORECARD_BUTTON = "(//button[text()='Scorecard'])[1]"
    VALIDATE_CERTIFICATE_BUTTON = "(//button[text()='Certificate'])[1]"
    COURSE_COMPLETION_PANEL_PREVIEW_IMAGE = "//img[@class='wf_image course-completion-panel__preview no-js-png']"
    SHARE_BUTTON = "//button[text()='Share']"
    SCORECARD_DOWNLOAD_LINK = "//a[text()='Download']"
    COURSE_BACK_BUTTON = "//button[@class='subpage-back-header__back-btn']"
    DEV_THINK_LTI_OPEN_COURSE_TITLE = "//h4[text()='Dev-Think LTI-Open']"
    COURSE_COMPLETED_LABEL_2 = "(//span[text()='Course Completed'])[2]"
    VALIDATE_CERTIFICATE_BUTTON_2 = "(//button[text()='Certificate'])[2]"
    DEV_TRY_ACTIVITY_SELF_SERVE_COURSE_TITLE = "(//h4[text()='Dev-Try activity-Self serve'])[1]"
    RESUME_COURSE_BUTTON = "(//button[text()='Resume Course'])[1]"
    COMPLETE_ALL_CRITERIA_MESSAGE = "(//p[text()='Complete all certificate criteria activities to unlock certificate'])[1]"



    SCORECARD_BUTTON = ("//button[contains(@class,'learning-item-card__btn')]"
                        "[normalize-space()='Scorecard']")
    CERTIFICATE_BUTTON = ("//button[contains(@class,'learning-item-card__btn')]"
                          "[normalize-space()='Certificate']")

    # --- recommendation sections ------------------------------------------
    RECOMMENDED_BY_INSTITUTE = "//h6[text()='Programs & Courses recommended by your institute']"
    RECOMMENDED_BY_WADHWANI = "//h6[text()='Programs & Courses recommended by Wadhwani Foundation']"
    RECOMMENDED_SECTION = "//div[contains(@class,'programs-and-courses__recommended')]"
    JOIN_A_BATCH = "//h6[text()='Join a batch']"

    # --- course detail page (/en/courses/<id>) -----------------------------
    COURSE_TITLE = "//h1[contains(@class,'course-title-heading')]"
    LESSON_ACCORDION = "//button[contains(@class,'accordion-trigger')]"
    CERTIFICATE_PROGRESS = "//*[contains(@class,'certificate-progress__title')]"
    EARNED_MICRO_CERTIFICATES = "//*[contains(@class,'earned-micro-certificates__title')]"
    ASSESSMENT_SCORE_VALUE = "//*[contains(@class,'scoreCount')]"
    ASSESSMENT_SCORE_LABEL = "//*[contains(@class,'scoreText')]"

    BACK_BUTTON = "//button[contains(@class,'subpage-back-header__back-btn')]"
