class BusinessPlannerLocators:
    EXPLORE_THINGS_TO_DO_HEADING = "//h4[text()='Explore things to do']"
    COURSES_AND_PROGRAMS_HEADING = "//h6[text()='Programs & Courses']"
    MY_CAREER_ADVISOR_HEADING = "//h6[text()='My Career Advisor']"
    PERSONAL_PITCH_TRAINER_HEADING = "//h6[text()='Personal Pitch Trainer']"
    INTERVIEW_COACH_HEADING = "//h6[text()='Interview Coach']"
    FORUMS_HEADING = "//h6[text()='Forums']"
    # The catalogue is its own route now (/en/course-program-list) with a page
    # title; the "recommended by your institute" strip is only rendered for an
    # account that HAS an institute, which a freshly registered user does not -
    # so the page title has to satisfy this check too. (ThinkActivityLocators
    # made the same change for the Dev-Think scenarios.)
    COURSES_OFFERED_BY_WADHWANI_FOUNDATION_HEADING = (
        "//h6[text()='Programs & Courses recommended by your institute']"
        "|//h1[contains(@class,'subpage-back-header__title')]"
        "[normalize-space()='Programs & Courses']"
    )
    CAROUSEL_RIGHT_ARROW_BUTTON = "//button[@class='react-multiple-carousel__arrow react-multiple-carousel__arrow--right ']"
    BUSINESSPLANNER_LTI_HEADING = "//h4[text()='BusinessPlanner-LTI']"
    # ------------------------------------------------------------------
    # The course detail page was redesigned: the Overview / Course Content /
    # Performance tabs are gone. The course is one scrolling page, and
    # Overview - the banner, duration, language and "About this course" -
    # opens as a modal from the (i) beside the title. Everything below points
    # at what now stands for each of them, confirmed against the live dev DOM.
    # ------------------------------------------------------------------
    COURSE_OVERVIEW_INFO_TRIGGER = "//button[@data-testid='course-details.header.overview-trigger']"
    COURSE_OVERVIEW_MODAL = "//div[contains(@class,'course-details-header__overview-modal')]"
    COURSE_OVERVIEW_MODAL_CLOSE = (
        "//div[contains(@class,'course-details-header__overview-modal')]"
        "//button[contains(@class,'responsive-drawer__close')]"
    )
    ABOUT_COURSE_PANEL = "//section[contains(@class,'about-course-panel')]"
    COURSE_OVERVIEW_IMAGE_SECTION = "//img[contains(@class,'about-course-panel__thumb')]"
    COURSE_DURATION = "//span[@data-testid='course-details.about.duration']"
    # "Overview" is the (i) trigger now; Course Content is a section of the
    # page; Performance is the completion panel / assessment score tile, which
    # only renders once there is something to show.
    COURSE_OVERVIEW_HEADING = COURSE_OVERVIEW_INFO_TRIGGER
    COURSE_CONTENT_HEADING = "//div[contains(@class,'Detail-parentTab-wrapper')]"
    COURSE_CURRICULUM_SECTION = "//section[@id='course-details-toc']"
    # Both of these are state-dependent: the completion panel and the score
    # tile only render once the course has an assessment result. They resolve
    # on a finished course and are legitimately absent on one still in
    # progress - which is what the BusinessPlanner course looks like today.
    PERFORMANCE_HEADING = (
        "//div[contains(@class,'course-completion-panel')]"
        "|//span[contains(@class,'scoreText')]"
    )
    ENROLL_NOW_BUTTON = "//button[normalize-space()='Enroll Now']"
    ENROLL_NOW_BUTTON_ON_COURSE = "//button[contains(@class,'enroll_now_btn')]"
    NOT_NOW_BUTTON = "//button[normalize-space()='Not now']"
    ENROLL_NOW_BUTTON_SECOND = "(//button[normalize-space()='Enroll Now'])[2]"
    # The old gauge and progress bar went with the tabs: what the page carries
    # now is the assessment score tile and each section's "n/m Lesson
    # Completed" status.
    OVERALL_SCORE_GAUGE = "//span[contains(@class,'scoreCount')]"
    COURSE_PROGRESS_BAR_CONTAINER = "//span[contains(@class,'newAccor_header_status')]"
    VALIDATE_BUSINESSPLANNER1_HEADING = "(//p[text()='BusinessPlanner1'])[1]"
    VALIDATE_BUSINESSPLANNER1_HEADING_SECOND = "(//p[text()='BusinessPlanner1'])[2]"
    VALIDATE_ASSESSMENTS_HEADING = "//p[text()='Assessments']"
    START_BUTTON_FIRST = "(//span[text()='Start'])[1]"
    VALIDATE_REVIEW_PROFILE_BUTTON = "//button[text()='Review Profile']"
    VALIDATE_NAME_CONTENT_CERTIFCATENAME_USERNAME = "//div[@class='name-content']"
    CONFIRM_AND_CONTINUE_BUTTON = "//button[text()='Confirm & Continue']"
    WRITE_SIMPLE_SENTENCE_TEXTAREA = "//textarea[@placeholder='Write one simple sentence. Say what you will sell, to whom, and where.']"
    CONTINUE_BUTTON = "//button[text()='Continue']"
    #the answer should not match to business idea question then below locator is used
    OK_ILL_CHANGE_IT_BUTTON = "//button[text()=\"OK, I'll change it\"]"
    SUBMIT_FOR_REVIEW_BUTTON = "//button[text()='Submit for review']"
    FILL_MORE_FIELDS_BUTTON = "//button[text()='Fill More Fields']"
    SUBMIT_NOW_BUTTON = "//button[text()='Submit Now →']"
    #market Analysis
    MARKET_ANALYSIS_HEADING = "//span[text()='Market Analysis']"
    CUSTOMER_GROUP_TEXTAREA = "//textarea[@placeholder='Describe your customer group. Say who they are and where they are.']"
    MARKET_ANALYSIS_TEXTAREA = "//textarea[@placeholder='Show simple proof with numbers. Examples: surveys, sign-ups, pre-orders, visits.']"
    LOCAL_COMPETITORS_TEXTAREA = "//textarea[@placeholder='List 1-3 local competitors. Say what makes their offers strong or weak.']"
    #product And Services
    PRODUCTS_AND_SERVICES_HEADING = "//span[text()='Products and Services']"
    MAIN_OFFER= "//textarea[@placeholder='Write your core offer. Keep it short and clear.']"
    SELLING_PROPOSITIONS = "//textarea[@placeholder='Describe why your offer is better than your competitors.']"
    #Marketing
    MARKETING_HEADING = "//span[text()='Marketing']"
    MAIN_CHANNEL_WHATSAPP_SELECT = "//select[.//option[@value='WhatsApp']]"
    MAIN_CHANNEL_WHATSAPP_MESSAGE_TEXTAREA = "//textarea[@placeholder='Write one short message describing the benefit and price.']"
    #Financial Plan
    FINANCIAL_PLAN_HEADING = "//span[text()='Financial Plan']"
    STARTUP_BUDGET_TOTAL_AMOUNT_TEXTAREA = "//textarea[@placeholder='Enter only the total amount as a number. This will be used for calculations. The breakdown should be entered in the next field below.']"
    STARTUP_BUDGET_BREAKDOWN_TEXTAREA = "//textarea[@placeholder='Write the total amount and list 2-4 major items with their costs. The total here should match the amount you entered above.']"
    MONTHLY_EXPENSES_FIXEDCOST_AMOUNT_TEXTAREA = "//textarea[@placeholder='Enter only the total monthly amount as a number. This will be used for calculations. Do not include your own labour costs. The breakdown should be entered in the next field below.']"
    MONTHLY_FIXEDCOST_BREAKDOWN_VARIABLECOST_AMOUNT_TEXTAREA = "//textarea[@placeholder='Write the total monthly amount and list 3-6 major expense items. Do not include your own labour costs. The total here should match the amount you entered above.']"
    UNIT_NAME_TEXTAREA = "//textarea[@placeholder='Name the unit that you will sell.']"
    NUMBER_OF_UNITS_SOLD_MONTHLY_SALES_VOLUME_TEXTAREA = "//textarea[@placeholder='Write how many units you will sell per month.']"
    PRICE_TEXTAREA = "//textarea[@placeholder='Enter only the price as a number. This will be used for calculations. What is included/excluded should be described in the next field below.']"
    PRICE_PERUNIT_TEXTAREA = "//textarea[@placeholder='Write the price and describe what is included and what costs extra.']"
    TOTAL_COST_BREAKDOWN_TEXTAREA = "//textarea[@placeholder='Write the total cost and list 2-3 items with their costs. Do not include your own labour costs. The total here should match the amount you entered above.']"
    #Operations
    OPERATIONS_HEADING = "//span[text()='Operations']"
    WORK_SCHEDULE_TEXTAREA = "//textarea[@placeholder='Write which days and what time you will work.']"
    NUMBER_OF_PEOPLE_WORKING_TEXTAREA = "//textarea[@placeholder='Write how many people will work, including you.']"
    WHERE_ARE_YOU_WORK_FROM_MAIN_PLACE_OF_WORK_OR_STORAGE_TEXTAREA = "//textarea[@placeholder='Write your main place of work or storage (do not write full home address).']"
    SERVICE_AREA_TEXTAREA = "//textarea[@placeholder='Write the main area or distance you will serve.']"
    CUSTOMER_JOURNEY_TEXTAREA = "//textarea[@placeholder='Write 3 short steps: from customer call to payment.']"
    INCOME_AND_EXPENSES_NOTE_TEXTAREA = "//textarea[@placeholder='Write how you will note income and expenses.']"
    # Growth Plan
    GROWTH_PLAN_HEADING = "//span[text()='Growth Plan']"
    MONTHLY_EARNINGS_TARGET_TEXTAREA = "//textarea[@placeholder='Write how much money you want to earn per month after 12 months.']"
    CUSTOMER_ACQUISITION_ACTION_TEXTAREA = "//textarea[@placeholder='Write one main action to increase customers.']"
    BIGGEST_RISK_TEXTAREA = "//textarea[@placeholder='Write the one biggest risk to your business in a short sentence.']"
    RISK_REDUCTION_ACTION_TEXTAREA = "//textarea[@placeholder='Write one simple action to reduce the risk you mentioned.']"
    SUBMIT_FOR_REVIEW_BUTTON = "//button[text()='Submit for review']"

    # ------------------------------------------------------------------
    # Added for features/newuser.feature > "User validates Business Planner
    # LTI course and completes all required activities". Everything above
    # this line came from the original hand-captured list; everything below
    # was read off the live dev DOM unless marked "best guess".
    # ------------------------------------------------------------------
    HOME_BUTTON = "//div[@id='Home']"
    ENROLL_NOW_BUTTON_FIRST = "(//button[text()='Enroll Now'])[1]"

    # --- Courses listing (/en/course-list) ---
    # COURSE_OVERVIEW_IMAGE_SECTION above is the banner on the course DETAIL
    # page; the listing renders "new-recommended-course-card" cards instead
    # (same class the student-persona courses_locators.py uses).
    # The listing moved to /en/course-program-list and its cards are
    # "learning-item-card" now, not "course-card".
    # Matched on the whole class token: "learning-item-card" is also the prefix
    # of every inner element's class (__body, __meta, ...), and contains() alone
    # counts all of them.
    COURSE_CARD = (
        "//div[contains(concat(' ',normalize-space(@class),' '),' learning-item-card ')]"
    )
    BUSINESSPLANNER_LTI_CARD = (
        "//h4[text()='BusinessPlanner-LTI']"
        "/ancestor::div[contains(@class,'learning-item-card')][1]"
    )
    BUSINESSPLANNER_LTI_CARD_IMAGE = BUSINESSPLANNER_LTI_CARD + "//img"
    # The card's duration is a "__meta-text" <p> ("10 hours"), NOT a
    # "duration"-classed element - that only exists in the About panel.
    BUSINESSPLANNER_LTI_CARD_DURATION = (
        BUSINESSPLANNER_LTI_CARD + "//p[contains(@class,'meta-text')]"
    )
    COURSE_NAVIGATION_BUTTON = BUSINESSPLANNER_LTI_CARD + "//button[contains(@class,'arrow-btn')]"

    # --- Course detail page ---
    # The listing card's title is an <h4>; on the detail page the same text is
    # the page's <h1>, so BUSINESSPLANNER_LTI_HEADING above does not match here.
    COURSE_TITLE_HEADING = "//h1[text()='BusinessPlanner-LTI']"
    START_LEARNING_WITH_YOUR_COURSE_TEXT = "//*[contains(normalize-space(.),'Start learning with your course')]"
    SUCCESSFULLY_ENROLLED_TEXT = "//*[contains(normalize-space(.),'Successfully Enrolled')]"

    # --- Overview (the (i) modal; rendered inline before enrollment) ---
    ABOUT_THIS_COURSE_HEADING = (
        "//h5[contains(@class,'about-course-panel__title')]"
        "[normalize-space()='About this course']"
    )
    COURSE_DESCRIPTION = (
        "//div[contains(@class,'about-course-panel__description')]"
        "//div[contains(@class,'wf_markdown')]//p"
    )
    COURSE_DESCRIPTION_FALLBACK = "//div[contains(@class,'about-course-panel__description')]"
    COURSE_LANGUAGE = "//span[@data-testid='course-details.about.language']"
    # Lessons and assessments are both "__includes-item" pills ("1 Lessons",
    # "1 Assessment") and are told apart by their text.
    NUMBER_OF_LESSONS = (
        "//span[contains(@class,'about-course-panel__includes-item')][contains(.,'Lesson')]"
    )
    NUMBER_OF_ASSESSMENTS = (
        "//span[contains(@class,'about-course-panel__includes-item')][contains(.,'Assessment')]"
    )

    # --- Course Content tab ---
    # NOTE: the app spells this heading "Assesments" (one 's').
    # VALIDATE_ASSESSMENTS_HEADING above uses the correct spelling and so never
    # matches - this is the one that does.
    VALIDATE_ASSESMENTS_HEADING_ACTUAL = "//p[text()='Assesments']"
    # The activity rows are "activity_name" spans; the repeated
    # <p>BusinessPlanner1</p> elements are the lesson/section headers.
    BUSINESSPLANNER1_ACTIVITY = "//span[contains(@class,'activity_name') and text()='BusinessPlanner1']"
    BUSINESSPLANNER2_ACTIVITY = "//span[contains(@class,'activity_name') and text()='BusinessPlanner2']"
    VALIDATE_BUSINESSPLANNER2_HEADING = BUSINESSPLANNER2_ACTIVITY
    ACTIVITY_COUNT = "//span[contains(@class,'activity-count')]"
    # Best guess - no completion indicator renders before the course is enrolled,
    # so this could not be captured from the pre-enrollment DOM.
    LESSON_COMPLETION_STATUS = (
        "//*[contains(@class,'lesson') or contains(@class,'progress') or contains(@class,'status')]"
        "[contains(normalize-space(.),'Complet') or contains(normalize-space(.),'/')]"
    )
    # Each Start button renders its label twice (a "text" and an "expand-text"
    # span), so this locator's count is 2x the number of buttons - count and
    # click via START_BUTTON_ELEMENT instead.
    START_BUTTON = "//span[text()='Start']"
    START_BUTTON_SECOND = "(//span[text()='Start'])[2]"
    # The captured Start locators point at the inner <span>; clicking the button
    # element itself is more reliable, so prefer this and fall back to the span.
    START_BUTTON_ELEMENT = "//button[.//span[text()='Start'] or normalize-space()='Start']"
    RESULT_BUTTON = "//span[text()='Result']"
    COMPLETED_STATUS = "//*[normalize-space(text())='Completed']"

    # Certificate-name modal (shown only the FIRST time an activity is started -
    # it does NOT reappear for the BusinessPlanner2 activity).
    REVIEW_YOUR_CERTIFICATE_NAME_TEXT = "//*[contains(normalize-space(.),'Review Your Certificate Name')]"

    # --- Activity (embedded LTI iframe) content ---
    BUSINESS_IDEA_HEADING = "//*[contains(normalize-space(text()),'Business Idea')]"
    # The instruction text sits next to the heading, but the element type varies
    # between screens, so the page object tries these in order.
    BUSINESS_IDEA_INSTRUCTIONS = "//*[contains(normalize-space(text()),'Business Idea')]/following::p[1]"
    BUSINESS_IDEA_INSTRUCTIONS_ANY = (
        "//*[contains(normalize-space(text()),'Business Idea')]"
        "/following::*[self::p or self::span or self::label or self::div][1]"
    )
    # Read off the live DOM: the activity's progress is a plain
    # <span class="ml-auto text-gray-600">81% complete</span> next to a
    # "Progress" label, with "70% Pass" / "11% With suggestions" beside it.
    # Nothing carries a "progress" class or a progressbar role, which is why
    # the two locators below it never matched.
    # NOTE: match on <span>, never on //* - "//*[contains(text(),'%')]" hits
    # every <style> block on the page (CSS is full of "%"), and because
    # _is_visible waits on .first it would then wait on a hidden stylesheet
    # and always time out.
    ACTIVITY_PROGRESS = "//span[contains(text(),'% complete')]"
    ACTIVITY_PROGRESS_ROLE = "//*[@role='progressbar']|//progress"
    ACTIVITY_PROGRESS_TEXT = (
        "//span[contains(text(),'%')]|//p[contains(text(),'%')]"
        "|//*[normalize-space(text())='Progress']"
    )
    ANY_ANSWER_TEXTAREA = "//textarea"
    # BusinessPlanner2 inherits the plan BusinessPlanner1 submitted, so it opens
    # on the reviewed plan instead of a blank question: every answer renders
    # read-only behind an "Edit" button and there is no textarea on screen until
    # a section is expanded. These are what that landing screen does show.
    # Confirmed against the live DOM: a reviewed plan has exactly ONE "Edit"
    # button, on the Business Idea. Everything else is edited by expanding its
    # section, whose textareas are directly writable.
    ANSWER_EDIT_BUTTON = "//button[normalize-space()='Edit']"
    # "Edit" only opens a confirmation ("Are you sure you want to edit?" -
    # "Changing your Business Idea will automatically re-trigger the review").
    # The field stays read-only until this is accepted, and the Edit button
    # itself never goes away - so clicking Edit repeatedly achieves nothing.
    EDIT_CONFIRM_YES_BUTTON = "//button[normalize-space()='Yes, Edit']"
    # The confirmation's own text. Matched on contains(text(),...) rather than
    # normalize-space(.) for the reason spelled out on REVIEWING_YOUR_PLAN_OVERLAY
    # below: the latter tests an element's whole string-value, so //* would also
    # match <html>/<body> and _is_visible would wait on that container instead.
    EDIT_CONFIRM_POPUP_MESSAGE = (
        "//*[contains(text(),'Are you sure you want to edit')]"
        "|//*[contains(text(),'re-trigger the review')]"
    )
    # The confirmation's dismiss button. The footer of an unlocked answer also
    # carries a "Cancel" (next to "Save & Re-evaluate"), so this XPath is only
    # meaningful while the confirmation is actually open.
    EDIT_CONFIRM_CANCEL_BUTTON = "//button[normalize-space()='Cancel']"
    # Once confirmed, the footer Save / Submit are replaced by Cancel and
    # "Save & Re-evaluate", which starts out disabled and enables as soon as
    # the answer text changes.
    SAVE_AND_RE_EVALUATE_BUTTON = "//button[normalize-space()='Save & Re-evaluate']"
    # The blocking overlay re-evaluation raises: "Reviewing your plan / Please
    # wait while we review your answers for N questions. / May take up to 15
    # seconds". Matched on text() rather than normalize-space(.) because the
    # latter tests an element's whole string-value, so //* would also match
    # <html> and <body> - and _is_visible waits on .first, which would then be
    # a container that never hides.
    REVIEWING_YOUR_PLAN_OVERLAY = (
        "//*[normalize-space(text())='Reviewing your plan']"
        "|//*[contains(text(),'Please wait while we review')]"
    )
    PLAN_FORM_LANDED = (
        "//button[normalize-space()='Submit for review']"
        "|//button[normalize-space()='Save']"
        "|//button[normalize-space()='Edit']"
    )



    