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
    COURSE_CARD_TITLE = "//h4[text()='QA-Emp skill Test-V2']"

    RESUME_COURSE_BUTTON = ("//button[contains(@class,'learning-item-card__btn')]"
                            "[normalize-space()='Resume Course']")
    PRE_VIDEO_ICON = "//p[text()='Pre Video']"
    VALIDATE_PITCH_TRAINER_PRE_VIDEO_ICON = "(//p[text()='Pitch Trainer Pre Video'])[2]"
    PRE_VIDEO_NOTSTARTED_RIGHTARROW="//button[@aria-label='Pitch Trainer Pre Video']"
    PRE_VIDEO_BACKNAVIATION_ARROW="//img[@class='wf_image back-btn false no-js-ArrowLeftDark']"
    POPUP_CLOSE_BUTTON = "//button[@class='popup-close-btn responsive-drawer__close']"
    COLLABORATE_ICON = "//p[text()='Collaborate']"
    ASSESSMENTS_ICON = "//p[text()='Assessments']"
    POST_VIDEO_ICON = "//p[text()='Post Video']"
    EARNED_MICRO_CERTIFICATES_GO_BUTTON = "//button[@class='earned-micro-certificates__go']"
    CERTIFICATION_CLOSE_BUTTON = "//button[@class='popup-close-btn responsive-drawer__close']"
    COURSE_BACK_BUTTON = "//button[@class='subpage-back-header__back-btn']"
    HPS_TEST_QA2_COURSE_TITLE = "//h4[text()=' HPS Test-QA2']"
    COURSE_COMPLETED_LABEL = "c"
    VALIDATE_SCORECARD_BUTTON = "(//button[text()='Scorecard'])[1]"
    HPS_TEST_QA2_COURSE_CERTIFICATE = "//*[normalize-space()='HPS Test-QA2']/following::button[contains(@data-testid,'certificate-cta')][1]"
    COURSE_COMPLETION_PANEL_PREVIEW_IMAGE = (
        "//div[contains(@class,'course-completion-panel')]"
        " | //img[contains(@class,'course-completion-panel__preview')]"
    )
    DOWNLOAD_CERTIFICATE_BUTTON = (
        "//button[@data-testid='course-details.completion.download-certificate']"
        " | //button[contains(normalize-space(), 'Download Certificate')]"
    )
    SHARE_BUTTON = "//button[text()='Share']"
    SCORECARD_DOWNLOAD_LINK = "//a[text()='Download']"
    DEV_THINK_LTI_OPEN_COURSE_TITLE = "//h4[text()='Dev-Think LTI-Open']"
    COURSE_COMPLETED_LABEL_2 = "(//span[text()='Course Completed'])[2]"
    DEV_THINK_LTI_OPEN_COURSE_CERTIFICATE="//*[normalize-space()='Dev-Think LTI-Open']/following::button[contains(@data-testid,'certificate-cta')][1]"
    DEV_TRY_ACTIVITY_SELF_SERVE_COURSE_TITLE = "(//h4[text()='Dev-Try activity-Self serve'])[1]"
    RESUME_COURSE_BUTTON = "(//span[text()='Resume Course'])[1]"
    # The course-content arrow is rendered as an image inside the clickable
    # breadcrumb control. Target the control first and retain the image as a
    # fallback for layouts where the image itself receives the click.
    COURSE_CONTENT_BACK_ARROW = (
        "//button[.//img[contains(@class,'back-btn')]]"
        " | //img[contains(@class,'back-btn') and contains(@class,'no-js-ArrowLeftDark')]"
    )
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
