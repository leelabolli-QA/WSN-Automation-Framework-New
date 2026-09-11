"""Page object for the "BusinessPlanner-LTI" course journey.

Drives features/newuser.feature > "User validates Business Planner LTI course
and completes all required activities": home -> Courses -> BusinessPlanner-LTI
-> enroll -> Overview / Course Content validations -> complete the
BusinessPlanner1 and BusinessPlanner2 activities.

Two behaviours of the real app shape most of this file:

1. The activity content is served through an embedded LTI iframe, so every
   in-activity locator has to be resolved against that frame, not the page.
2. The "Review Your Certificate Name" modal (Review Profile / Confirm &
   Continue) is a ONE-TIME prompt shown when the FIRST activity is started.
   Starting the BusinessPlanner2 activity does NOT show it again, even though
   the feature file describes it for both. Everything gated on
   `_certificate_popup_shown` is therefore validated when the modal really
   appeared and reported as skipped when it did not, so the scenario reads the
   same for both activities without failing on the second one.

The feature file runs the SAME step sequence over both activities (start ->
certificate modal -> activity page / progress / Business Idea question ->
answer -> Continue -> complete all questions). The two activities are separate
LTI launches, so BusinessPlanner2's first screen is not guaranteed to be the
Business Idea question that BusinessPlanner1 opens on. Anything specific to
that opening screen (`_FIRST_ACTIVITY_SCREEN_TARGETS`, the Business Idea answer
and the first Continue) is asserted strictly on the first activity and reported
as skipped on a later one instead of failing, and falls back to whatever answer
field the screen does render - so the shared wording drives both activities.
"""

from pages.base_page import BasePage
from locators.new_user_locators.business_planner_locators import (
    BusinessPlannerLocators as BP,
)
from utils.helpers import attach_screenshot, highlight_element

# How long to give the embedded LTI activity's own content time to render
# before deciding nothing is there (matches new_user_page.py's LTI timeout).
LTI_CONTENT_LOAD_TIMEOUT_MS = 25000
# How long to let "Save & Re-evaluate" re-review the plan. The overlay says it
# may take up to 15 seconds; this leaves generous room over that.
PLAN_REVIEW_TIMEOUT_MS = 90000
# Seconds to keep looking for the LTI iframe after a Start / Confirm & Continue.
LTI_FRAME_POLL_STEPS = 20


class BusinessPlannerPage(BasePage):

    # ---------- "the user clicks on the ..." targets ----------

    _BUTTON_LOCATORS = {
        "Home": BP.HOME_BUTTON,
        "Not now": BP.NOT_NOW_BUTTON,
    }

    _OPTION_LOCATORS = {
        # The dashboard card is labelled "Programs & Courses" now; the older
        # wordings the feature used are kept as aliases.
        "Programs & Courses": BP.COURSES_AND_PROGRAMS_HEADING,
        "Courses": BP.COURSES_AND_PROGRAMS_HEADING,
        "Courses and Programs": BP.COURSES_AND_PROGRAMS_HEADING,
        "My Career Advisor": BP.MY_CAREER_ADVISOR_HEADING,
        "Personal Pitch Trainer": BP.PERSONAL_PITCH_TRAINER_HEADING,
        "Interview Coach": BP.INTERVIEW_COACH_HEADING,
        "Forums": BP.FORUMS_HEADING,
    }

    _TAB_LOCATORS = {
        "Overview": BP.COURSE_OVERVIEW_HEADING,
        "Course Content": BP.COURSE_CONTENT_HEADING,
        "Performance": BP.PERFORMANCE_HEADING,
    }

    _COURSE_LOCATORS = {
        "BusinessPlanner-LTI": BP.BUSINESSPLANNER_LTI_HEADING,
    }

    # ---------- "the user should be able to see the ..." targets ----------
    #
    # description (lower-cased, exactly as written in the feature file after
    # "the user should be able to see the ") -> (locator, scope, soft)
    #
    #   locator             - one XPath, or a list of candidates tried in order
    #                         (the first visible one satisfies the check) for
    #                         elements whose exact markup was not captured
    #   scope "page"        - resolved against the browser page
    #   scope "frame"       - resolved against the embedded LTI activity iframe
    #   scope "certificate" - part of the one-time certificate-name modal, so it
    #                         is only asserted when that modal actually appeared
    #   soft=True           - best-guess locator (see the "Added for" block in
    #                         business_planner_locators.py); logged, not failed,
    #                         when absent so an unverified XPath cannot fail an
    #                         otherwise-passing run
    _VIEW_TARGETS = {
        # Home
        '"explore things to do" section': (BP.EXPLORE_THINGS_TO_DO_HEADING, "page", False),
        '"courses and programs" option': (BP.COURSES_AND_PROGRAMS_HEADING, "page", False),
        '"programs & courses" option': (BP.COURSES_AND_PROGRAMS_HEADING, "page", False),
        '"my career advisor" option': (BP.MY_CAREER_ADVISOR_HEADING, "page", False),
        '"personal pitch trainer" option': (BP.PERSONAL_PITCH_TRAINER_HEADING, "page", False),
        '"interview coach" option': (BP.INTERVIEW_COACH_HEADING, "page", False),
        '"forums" option': (BP.FORUMS_HEADING, "page", False),

        # Courses listing
        '"courses offered by wadhwani foundation" section': (
            BP.COURSES_OFFERED_BY_WADHWANI_FOUNDATION_HEADING, "page", False),
        'available courses': (BP.COURSE_CARD, "page", False),
        '"businessplanner-lti" course': (BP.BUSINESSPLANNER_LTI_HEADING, "page", False),
        'businessplanner-lti course image': (
            [BP.BUSINESSPLANNER_LTI_CARD_IMAGE, BP.COURSE_CARD + "//img"], "page", True),
        'businessplanner-lti course duration': (
            [BP.BUSINESSPLANNER_LTI_CARD_DURATION, BP.COURSE_DURATION], "page", False),
        'course navigation button': (
            [BP.COURSE_NAVIGATION_BUTTON, BP.CAROUSEL_RIGHT_ARROW_BUTTON], "page", False),

        # Course detail / enrollment
        '"businessplanner-lti" course title': (BP.COURSE_TITLE_HEADING, "page", False),
        '"overview" tab': (BP.COURSE_OVERVIEW_HEADING, "page", False),
        '"course content" tab': (BP.COURSE_CONTENT_HEADING, "page", False),
        '"performance" tab': (BP.PERFORMANCE_HEADING, "page", False),
        '"enroll now" button': (BP.ENROLL_NOW_BUTTON, "page", False),
        '"start learning with your course" message': (BP.START_LEARNING_WITH_YOUR_COURSE_TEXT, "page", True),
        '"not now" button': (BP.NOT_NOW_BUTTON, "page", False),
        'second "enroll now" button': (BP.ENROLL_NOW_BUTTON_SECOND, "page", False),
        '"successfully enrolled!" message': (BP.SUCCESSFULLY_ENROLLED_TEXT, "page", True),
        'course progress section': (BP.COURSE_PROGRESS_BAR_CONTAINER, "page", False),
        'overall score': (BP.OVERALL_SCORE_GAUGE, "page", False),
        'overall progress': (BP.COURSE_PROGRESS_BAR_CONTAINER, "page", False),

        # Overview tab
        'businessplanner-lti course banner': (BP.COURSE_OVERVIEW_IMAGE_SECTION, "page", False),
        '"about this course" section': (BP.ABOUT_THIS_COURSE_HEADING, "page", False),
        'course description': (
            [BP.COURSE_DESCRIPTION, BP.COURSE_DESCRIPTION_FALLBACK], "page", True),
        'course duration': (BP.COURSE_DURATION, "page", False),
        'course language': (BP.COURSE_LANGUAGE, "page", False),
        'number of lessons': (BP.NUMBER_OF_LESSONS, "page", False),
        'number of assessments': (BP.NUMBER_OF_ASSESSMENTS, "page", False),

        # Course Content tab
        '"businessplanner1" section': (BP.VALIDATE_BUSINESSPLANNER1_HEADING, "page", False),
        'lesson completion status': (BP.LESSON_COMPLETION_STATUS, "page", True),
        'updated lesson completion status': (BP.LESSON_COMPLETION_STATUS, "page", True),
        '"businessplanner1" activity': (BP.BUSINESSPLANNER1_ACTIVITY, "page", False),
        '"businessplanner2" activity': (BP.BUSINESSPLANNER2_ACTIVITY, "page", False),
        # The app's heading is misspelled "Assesments" - try that first and fall
        # back to the correct spelling in case it is ever fixed.
        '"assessments" section': (
            [BP.VALIDATE_ASSESMENTS_HEADING_ACTUAL, BP.VALIDATE_ASSESSMENTS_HEADING], "page", False),
        'activity count': (BP.ACTIVITY_COUNT, "page", False),
        'first "start" button': (BP.START_BUTTON_FIRST, "page", False),
        # A finished activity's own "Completed" label was not present; its Start
        # button turning into "Result" is the observable completed state.
        'completed status for the businessplanner1 activity': (
            [BP.COMPLETED_STATUS, BP.RESULT_BUTTON], "page", False),
        'completed status for the businessplanner2 activity': (
            [BP.COMPLETED_STATUS, BP.RESULT_BUTTON], "page", False),
        '"result" button for the completed activity': (BP.RESULT_BUTTON, "page", True),
        '"start" button for the businessplanner2 activity': (BP.START_BUTTON, "page", True),

        # Certificate-name modal (first activity only - see the module docstring)
        '"review your certificate name" message': (BP.REVIEW_YOUR_CERTIFICATE_NAME_TEXT, "certificate", True),
        'certificate name': (BP.VALIDATE_NAME_CONTENT_CERTIFCATENAME_USERNAME, "certificate", False),
        '"review profile" button': (BP.VALIDATE_REVIEW_PROFILE_BUTTON, "certificate", False),
        '"confirm & continue" button': (BP.CONFIRM_AND_CONTINUE_BUTTON, "certificate", False),

        # Inside the activity (embedded LTI iframe)
        'businessplanner1 activity page': (BP.WRITE_SIMPLE_SENTENCE_TEXTAREA, "frame", False),
        # BusinessPlanner2 runs the same checks; its opening screen is not
        # guaranteed to be the Business Idea one - it inherits the plan
        # BusinessPlanner1 submitted and opens on the reviewed form, where the
        # answers are read-only Edit blocks - so the plan form counts too.
        'businessplanner2 activity page': (
            [BP.WRITE_SIMPLE_SENTENCE_TEXTAREA, BP.ANY_ANSWER_TEXTAREA, BP.PLAN_FORM_LANDED],
            "frame", False),
        'activity progress': (
            [BP.ACTIVITY_PROGRESS, BP.ACTIVITY_PROGRESS_ROLE, BP.ACTIVITY_PROGRESS_TEXT],
            "frame", True),
        '"business idea" question': (BP.BUSINESS_IDEA_HEADING, "frame", False),
        'instructions for the business idea question': (
            [BP.BUSINESS_IDEA_INSTRUCTIONS, BP.BUSINESS_IDEA_INSTRUCTIONS_ANY], "frame", True),
        # On the reviewed plan form the answer is behind an "Edit" button rather
        # than in a live textarea - both are "the answer field" for this check.
        'answer field': (
            [BP.WRITE_SIMPLE_SENTENCE_TEXTAREA, BP.ANY_ANSWER_TEXTAREA, BP.ANSWER_EDIT_BUTTON],
            "frame", False),
        'required answer field': (
            [BP.ANY_ANSWER_TEXTAREA, BP.ANSWER_EDIT_BUTTON], "frame", False),
        'required answer fields': (
            [BP.ANY_ANSWER_TEXTAREA, BP.ANSWER_EDIT_BUTTON], "frame", False),
        'required questions': (
            [BP.ANY_ANSWER_TEXTAREA, BP.ANSWER_EDIT_BUTTON], "frame", False),
        '"continue" button': (BP.CONTINUE_BUTTON, "frame", False),

        # Editing the Business Idea on an already-reviewed plan (the
        # BusinessPlanner2 case). Two extra scopes carry these:
        #   "edit"       - only meaningful on a plan whose answers are locked
        #                  behind "Edit"; skipped when this screen has none
        #   "edit_popup" - part of the "Are you sure you want to edit?"
        #                  confirmation, so the check RAISES that confirmation
        #                  first (the feature file has no separate "clicks on
        #                  the Edit button" step) and then asserts
        'edit button': (BP.ANSWER_EDIT_BUTTON, "edit", False),
        '"cancel" button': (BP.EDIT_CONFIRM_CANCEL_BUTTON, "edit_popup", False),
        '"yes, edit" button': (BP.EDIT_CONFIRM_YES_BUTTON, "edit_popup", False),
        'answer field for the business idea question': (
            [BP.WRITE_SIMPLE_SENTENCE_TEXTAREA, BP.ANY_ANSWER_TEXTAREA], "edit", False),
        '"save and re evaluate" button for the business idea question': (
            BP.SAVE_AND_RE_EVALUATE_BUTTON, "edit", False),
    }

    # Validations that describe the FIRST activity's opening screen. The feature
    # file replays them for BusinessPlanner2, which is a separate LTI launch and
    # may open on a different question, so on any activity after the first these
    # are logged as skipped instead of failing the scenario.
    _FIRST_ACTIVITY_SCREEN_TARGETS = {
        '"business idea" question',
        'instructions for the business idea question',
        '"continue" button',
    }

    # The business plan is a set of COLLAPSIBLE sections: only the open one's
    # textareas are visible/fillable at any moment. Filling "whatever is on
    # screen" therefore leaves every other section blank, so each section's
    # heading is clicked to expand it before its own fields are filled.
    # (name, heading locator, [(field locator, answer), ...])
    _SECTIONS = [
        ("Market Analysis", BP.MARKET_ANALYSIS_HEADING, [
            (BP.MARKET_ANALYSIS_TEXTAREA,
             "I surveyed 60 families near my area and 42 said they would buy every week. "
             "I already have 25 pre-orders and 120 sign-ups on my WhatsApp list."),
            (BP.LOCAL_COMPETITORS_TEXTAREA,
             "1. Shree Bakery - good taste but no home delivery. 2. Fresh Corner - fast "
             "delivery but very limited variety. 3. Local kirana shop - cheap but the "
             "stock is often a day old."),
        ]),
        ("Products and Services", BP.PRODUCTS_AND_SERVICES_HEADING, [
            (BP.MAIN_OFFER,
             "Freshly baked breads, cakes and cookies delivered to homes and offices "
             "every morning."),
            (BP.SELLING_PROPOSITIONS,
             "My products are baked the same morning, cost about 10% less than the "
             "nearby bakeries and are delivered free within 3 km."),
        ]),
        ("Marketing", BP.MARKETING_HEADING, [
            (BP.MAIN_CHANNEL_WHATSAPP_MESSAGE_TEXTAREA,
             "Fresh bread and cakes baked this morning, delivered free to your door. "
             "Bread Rs.40, cake Rs.250. Order on WhatsApp before 8 AM."),
        ]),
        ("Financial Plan", BP.FINANCIAL_PLAN_HEADING, [
            (BP.STARTUP_BUDGET_TOTAL_AMOUNT_TEXTAREA, "150000"),
            (BP.STARTUP_BUDGET_BREAKDOWN_TEXTAREA,
             "Total Rs.1,50,000 - oven Rs.60,000, mixer and baking tools Rs.30,000, "
             "shop deposit Rs.40,000, first raw material stock Rs.20,000."),
            (BP.MONTHLY_EXPENSES_FIXEDCOST_AMOUNT_TEXTAREA, "35000"),
            (BP.MONTHLY_FIXEDCOST_BREAKDOWN_VARIABLECOST_AMOUNT_TEXTAREA,
             "Total Rs.35,000 per month - rent Rs.12,000, electricity Rs.5,000, gas "
             "Rs.4,000, packaging Rs.4,000, delivery fuel Rs.5,000, phone and internet "
             "Rs.5,000."),
            (BP.UNIT_NAME_TEXTAREA, "One bread loaf of 400 grams"),
            (BP.NUMBER_OF_UNITS_SOLD_MONTHLY_SALES_VOLUME_TEXTAREA, "1200"),
            (BP.PRICE_TEXTAREA, "40"),
            (BP.PRICE_PERUNIT_TEXTAREA,
             "Rs.40 per loaf including packaging and free delivery within 3 km. "
             "Delivery beyond 3 km costs Rs.20 extra."),
            (BP.TOTAL_COST_BREAKDOWN_TEXTAREA,
             "Total Rs.22 per loaf - flour and yeast Rs.14, gas Rs.4, packaging Rs.4."),
        ]),
        ("Operations", BP.OPERATIONS_HEADING, [
            (BP.WORK_SCHEDULE_TEXTAREA,
             "Monday to Saturday, 5 AM to 1 PM for baking and 4 PM to 7 PM for deliveries."),
            (BP.NUMBER_OF_PEOPLE_WORKING_TEXTAREA,
             "3 people including me - one baking helper and one delivery person."),
            (BP.WHERE_ARE_YOU_WORK_FROM_MAIN_PLACE_OF_WORK_OR_STORAGE_TEXTAREA,
             "A rented 200 sq ft shop with a small storage room in the Kothrud market area."),
            (BP.SERVICE_AREA_TEXTAREA,
             "Kothrud and the nearby colonies, up to 5 km from the shop."),
            (BP.CUSTOMER_JOURNEY_TEXTAREA,
             "1. Customer places the order on WhatsApp. 2. We bake and pack it the same "
             "morning. 3. We deliver it and collect payment by UPI or cash."),
            (BP.INCOME_AND_EXPENSES_NOTE_TEXTAREA,
             "I will note every sale and expense daily in a register and enter them in a "
             "simple mobile app every evening."),
        ]),
        ("Growth Plan", BP.GROWTH_PLAN_HEADING, [
            (BP.MONTHLY_EARNINGS_TARGET_TEXTAREA,
             "I want to earn Rs.60,000 profit per month after 12 months."),
            (BP.CUSTOMER_ACQUISITION_ACTION_TEXTAREA,
             "Run a weekly WhatsApp offer and give a free sample with every first order "
             "to bring in new customers."),
            (BP.BIGGEST_RISK_TEXTAREA,
             "A sudden rise in flour and gas prices could sharply cut my profit."),
            (BP.RISK_REDUCTION_ACTION_TEXTAREA,
             "Buy flour in bulk on a monthly contract with one supplier to lock the price."),
        ]),
    ]

    # Flat view of every field, used when filling whatever happens to be on
    # screen (the Business Idea screen, and as a safety net for any field the
    # section sweep did not reach).
    _ANSWER_SEQUENCE = [
        (BP.WRITE_SIMPLE_SENTENCE_TEXTAREA,
         "I will sell freshly baked breads and cakes to families and small offices "
         "in my neighbourhood in Pune."),
        (BP.MARKET_ANALYSIS_TEXTAREA,
         "I surveyed 60 families near my area and 42 said they would buy every week. "
         "I already have 25 pre-orders and 120 sign-ups on my WhatsApp list."),
        (BP.LOCAL_COMPETITORS_TEXTAREA,
         "1. Shree Bakery - good taste but no home delivery. 2. Fresh Corner - fast "
         "delivery but very limited variety. 3. Local kirana shop - cheap but the "
         "stock is often a day old."),
        (BP.MAIN_OFFER,
         "Freshly baked breads, cakes and cookies delivered to homes and offices "
         "every morning."),
        (BP.SELLING_PROPOSITIONS,
         "My products are baked the same morning, cost about 10% less than the "
         "nearby bakeries and are delivered free within 3 km."),
        (BP.MAIN_CHANNEL_WHATSAPP_MESSAGE_TEXTAREA,
         "Fresh bread and cakes baked this morning, delivered free to your door. "
         "Bread Rs.40, cake Rs.250. Order on WhatsApp before 8 AM."),
        (BP.STARTUP_BUDGET_TOTAL_AMOUNT_TEXTAREA, "150000"),
        (BP.STARTUP_BUDGET_BREAKDOWN_TEXTAREA,
         "Total Rs.1,50,000 - oven Rs.60,000, mixer and baking tools Rs.30,000, "
         "shop deposit Rs.40,000, first raw material stock Rs.20,000."),
        (BP.MONTHLY_EXPENSES_FIXEDCOST_AMOUNT_TEXTAREA, "35000"),
        (BP.MONTHLY_FIXEDCOST_BREAKDOWN_VARIABLECOST_AMOUNT_TEXTAREA,
         "Total Rs.35,000 per month - rent Rs.12,000, electricity Rs.5,000, gas "
         "Rs.4,000, packaging Rs.4,000, delivery fuel Rs.5,000, phone and internet "
         "Rs.5,000."),
        (BP.UNIT_NAME_TEXTAREA, "One bread loaf of 400 grams"),
        (BP.NUMBER_OF_UNITS_SOLD_MONTHLY_SALES_VOLUME_TEXTAREA, "1200"),
        (BP.PRICE_TEXTAREA, "40"),
        (BP.PRICE_PERUNIT_TEXTAREA,
         "Rs.40 per loaf including packaging and free delivery within 3 km. "
         "Delivery beyond 3 km costs Rs.20 extra."),
        (BP.TOTAL_COST_BREAKDOWN_TEXTAREA,
         "Total Rs.22 per loaf - flour and yeast Rs.14, gas Rs.4, packaging Rs.4."),
        (BP.WORK_SCHEDULE_TEXTAREA,
         "Monday to Saturday, 5 AM to 1 PM for baking and 4 PM to 7 PM for deliveries."),
        (BP.NUMBER_OF_PEOPLE_WORKING_TEXTAREA,
         "3 people including me - one baking helper and one delivery person."),
        (BP.WHERE_ARE_YOU_WORK_FROM_MAIN_PLACE_OF_WORK_OR_STORAGE_TEXTAREA,
         "A rented 200 sq ft shop with a small storage room in the Kothrud market area."),
        (BP.SERVICE_AREA_TEXTAREA,
         "Kothrud and the nearby colonies, up to 5 km from the shop."),
        (BP.CUSTOMER_JOURNEY_TEXTAREA,
         "1. Customer places the order on WhatsApp. 2. We bake and pack it the same "
         "morning. 3. We deliver it and collect payment by UPI or cash."),
        (BP.INCOME_AND_EXPENSES_NOTE_TEXTAREA,
         "I will note every sale and expense daily in a register and enter them in a "
         "simple mobile app every evening."),
        (BP.MONTHLY_EARNINGS_TARGET_TEXTAREA,
         "I want to earn Rs.60,000 profit per month after 12 months."),
        (BP.CUSTOMER_ACQUISITION_ACTION_TEXTAREA,
         "Run a weekly WhatsApp offer and give a free sample with every first order "
         "to bring in new customers."),
        (BP.BIGGEST_RISK_TEXTAREA,
         "A sudden rise in flour and gas prices could sharply cut my profit."),
        (BP.RISK_REDUCTION_ACTION_TEXTAREA,
         "Buy flour in bulk on a monthly contract with one supplier to lock the price."),
    ]

    # The activity checks that the Business Idea answer actually reads like a
    # business idea and, when it does not, blocks with "OK, I'll change it"
    # (see the comment on that locator). Each rejection moves to the next
    # rewording rather than resubmitting the same text.
    _BUSINESS_IDEA_ALTERNATIVES = [
        "I will sell freshly baked breads and cakes to families and small offices "
        "in my neighbourhood in Pune.",
        "I will sell home-baked bread, cakes and cookies to families living within "
        "5 km of my shop in Kothrud, Pune, with free morning delivery.",
        "I will bake and sell fresh bread and cakes every morning to households and "
        "small offices in Kothrud, Pune, and deliver the orders to their door.",
    ]

    # ---------- BusinessPlanner2's own business ----------
    # BusinessPlanner2 opens on the plan BusinessPlanner1 submitted, with every
    # answer already filled in. Re-submitting those answers would exercise
    # nothing, so the second activity is given a DIFFERENT business and every
    # field is overwritten with it - the same fill-and-submit journey as the
    # first activity, on content the activity has not seen before.
    # Same field layout as _SECTIONS / _ANSWER_SEQUENCE above; only the text
    # differs, so this is an overlay keyed by locator rather than a second copy
    # of the section tree (see _plan_answers).
    _PLAN2_IDEA_ALTERNATIVES = [
        "I will repair mobile phones and sell accessories for students and shop "
        "owners in Kothrud, Pune.",
        "I will run a mobile phone repair counter in Kothrud, Pune, fixing screens "
        "and batteries the same day and selling chargers and covers.",
        "I will offer same-day mobile phone screen and battery repair, plus phone "
        "accessories, to students and small shop owners around Kothrud, Pune.",
    ]

    _PLAN2_ANSWERS = {
        BP.WRITE_SIMPLE_SENTENCE_TEXTAREA: _PLAN2_IDEA_ALTERNATIVES[0],
        BP.MARKET_ANALYSIS_TEXTAREA:
            "I asked 55 students and 20 shop owners nearby and 38 of them said they "
            "wait 2-3 days for a screen repair today. 18 have already booked a repair "
            "slot with me for this month.",
        BP.LOCAL_COMPETITORS_TEXTAREA:
            "1. Mobile Care - reliable but takes three days. 2. Screen Point - fast "
            "but charges almost double. 3. The service centre in the mall - genuine "
            "parts but only handles two brands.",
        BP.MAIN_OFFER:
            "Same-day mobile phone screen and battery replacement, plus chargers, "
            "covers and screen guards sold over the counter.",
        BP.SELLING_PROPOSITIONS:
            "I return the phone the same day, charge about 20% less than the mall "
            "service centre and give a three month written warranty on every repair.",
        BP.MAIN_CHANNEL_WHATSAPP_MESSAGE_TEXTAREA:
            "Cracked screen or weak battery? Same-day repair with a 3 month warranty. "
            "Screen from Rs.900, battery from Rs.700. Send us a WhatsApp message.",
        BP.STARTUP_BUDGET_TOTAL_AMOUNT_TEXTAREA: "120000",
        BP.STARTUP_BUDGET_BREAKDOWN_TEXTAREA:
            "Total Rs.1,20,000 - repair tools and soldering station Rs.35,000, "
            "spare screens and batteries Rs.45,000, counter and display rack "
            "Rs.20,000, shop deposit Rs.20,000.",
        BP.MONTHLY_EXPENSES_FIXEDCOST_AMOUNT_TEXTAREA: "28000",
        BP.MONTHLY_FIXEDCOST_BREAKDOWN_VARIABLECOST_AMOUNT_TEXTAREA:
            "Total Rs.28,000 per month - rent Rs.10,000, electricity Rs.3,000, "
            "helper salary Rs.9,000, phone and internet Rs.2,000, packaging and "
            "consumables Rs.4,000.",
        BP.UNIT_NAME_TEXTAREA: "One mobile phone screen replacement",
        BP.NUMBER_OF_UNITS_SOLD_MONTHLY_SALES_VOLUME_TEXTAREA: "90",
        BP.PRICE_TEXTAREA: "900",
        BP.PRICE_PERUNIT_TEXTAREA:
            "Rs.900 per screen replacement including fitting and a 3 month warranty. "
            "Premium phone models cost Rs.400 extra.",
        BP.TOTAL_COST_BREAKDOWN_TEXTAREA:
            "Total Rs.520 per repair - spare screen Rs.450, adhesive and consumables "
            "Rs.40, packaging Rs.30.",
        BP.WORK_SCHEDULE_TEXTAREA:
            "Monday to Saturday, 10 AM to 8 PM, with repairs taken in until 6 PM so "
            "they can be returned the same day.",
        BP.NUMBER_OF_PEOPLE_WORKING_TEXTAREA:
            "2 people including me - one trained repair helper at the counter.",
        BP.WHERE_ARE_YOU_WORK_FROM_MAIN_PLACE_OF_WORK_OR_STORAGE_TEXTAREA:
            "A rented 150 sq ft shop with a locked spare-parts cabinet near the "
            "Kothrud bus stop.",
        BP.SERVICE_AREA_TEXTAREA:
            "Kothrud and the college area around it, up to 4 km from the shop.",
        BP.CUSTOMER_JOURNEY_TEXTAREA:
            "1. Customer sends the phone model and problem on WhatsApp. 2. We quote a "
            "price and book a slot. 3. We repair it the same day and return it, "
            "collecting payment by UPI or cash.",
        BP.INCOME_AND_EXPENSES_NOTE_TEXTAREA:
            "I will record every repair and part used in a daily register and enter "
            "the totals into a simple mobile app each evening.",
        BP.MONTHLY_EARNINGS_TARGET_TEXTAREA:
            "I want to earn Rs.45,000 profit per month after 12 months.",
        BP.CUSTOMER_ACQUISITION_ACTION_TEXTAREA:
            "Give every college student a 10% discount card and pay a small referral "
            "fee to nearby mobile shops that send me repair work.",
        BP.BIGGEST_RISK_TEXTAREA:
            "A delay or price rise from my spare-parts supplier would stop me "
            "promising same-day repairs.",
        BP.RISK_REDUCTION_ACTION_TEXTAREA:
            "Keep one month of fast-moving screens and batteries in stock and hold "
            "accounts with two suppliers instead of one.",
    }

    # One page object per scenario run, so the state carried between steps
    # (course-content URL, activity iframe, whether the certificate modal was
    # shown) survives the whole journey. behave drops context attributes at the
    # end of each scenario, so this is held on the class - the same pattern
    # new_user_page.py uses, and reset the same way by environment.py.
    _shared_instance = None
    _active = False

    @classmethod
    def for_page(cls, page):
        """Return the scenario-scoped page object, creating it if needed.

        A new instance is built whenever the underlying Playwright page changed
        (environment.py rebuilds the tab after a crash) so a stale object never
        keeps driving a dead page.
        """
        instance = cls._shared_instance
        if instance is None or instance.page is not page:
            instance = cls(page)
            cls._shared_instance = instance
        return instance

    @classmethod
    def activate(cls):
        """Mark the BusinessPlanner flow as the one currently running.

        newuser.feature's two scenarios share the wording of the ordinal
        button step ('the user clicks on the first "Enroll Now" button'), and
        behave's step registry is global - one definition has to serve both, so
        it routes on this flag. See features/steps/student_persona/newuser_steps.py.

        Activating one flow deactivates every other: newuser.feature's
        BusinessPlanner, Dev-Think and Do-LTI scenarios live in the same
        feature and before_feature only resets between features, so whichever
        Given ran last has to win.
        """
        cls._active = True
        try:
            from pages.Newuser.think_activity_page import _flow_classes
            for other in _flow_classes():
                if other is not cls:
                    other._active = False
        except Exception:
            pass

    @classmethod
    def is_active(cls):
        return cls._active

    @classmethod
    def reset_shared_state(cls):
        cls._shared_instance = None
        cls._active = False

    def __init__(self, page):
        super().__init__(page)
        self._activity_frame = None
        self._course_content_url = None
        self._certificate_popup_shown = False
        # Which activity is running (1 = BusinessPlanner1, 2 = BusinessPlanner2).
        # Set by click_start; used to keep the shared step wording strict on the
        # first activity and tolerant on the later ones.
        self._activity_index = 0
        self._business_idea_attempt = 0
        self._fill_more_fields_used = False
        self._submitted_for_review = False
        # How many answers this activity has taken. verify_answer_entered uses
        # it because the form is submitted (or scrolled to a fresh, empty
        # section) by the time the "answer should be entered" step runs, so
        # "some visible field currently holds text" is not a reliable check.
        self._answers_entered = 0

    # ---------- internal helpers ----------

    def _is_visible(self, locator, timeout=6000, target=None):
        target = target or self.page
        try:
            target.locator(locator).first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def _click(self, locator, description, timeout=20000, force=False):
        target = self.page.locator(locator).first
        target.wait_for(state="visible", timeout=timeout)
        try:
            highlight_element(self.page, target)
        except Exception:
            pass
        target.click(force=force)
        print(f"Clicked {description}")

    def _click_if_present(self, locator, description, timeout=5000, target=None, force=True):
        target = target or self.page
        try:
            element = target.locator(locator).first
            element.wait_for(state="visible", timeout=timeout)
            element.click(force=force)
            print(f"Clicked {description}")
            return True
        except Exception:
            return False

    def _activity_target(self):
        """The embedded LTI iframe if one was captured, else the page itself.

        Falling back to the page keeps every in-activity locator working if the
        course ever renders its content inline instead of in an iframe.
        """
        frame = self._activity_frame
        if frame is None:
            return self.page
        try:
            if frame.is_detached():
                self._activity_frame = None
                return self.page
        except Exception:
            return self.page
        return frame

    def _capture_activity_frame(self, poll_steps=LTI_FRAME_POLL_STEPS):
        """Find the LTI iframe the activity loads into the same tab."""
        for _ in range(poll_steps):
            for frame in self.page.frames:
                if "lti" in (frame.url or ""):
                    self._activity_frame = frame
                    print("Activity content frame captured")
                    return frame
            self.page.wait_for_timeout(1000)
        print("Activity content frame not found - falling back to the page itself")
        self._activity_frame = None
        return None

    def _return_to_course_content(self):
        """Go back to the course's Course Content tab.

        The activity runs behind iframe-based routing, so browser history lands
        on unpredictable states - navigate to the remembered course URL and
        re-open the tab instead (the same approach new_user_page.py uses).
        """
        if not self._course_content_url:
            print("No stored Course Content URL - staying on the current page")
            return
        self.page.goto(self._course_content_url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(1500)
        # No Course Content tab to click any more - the curriculum is part of
        # the course page; it just has to finish rendering.
        self.close_overview_modal()
        self._wait_for_page_ready()
        self._activity_frame = None

    # ---------- navigation ----------

    def click_button(self, label):
        if label == "Confirm & Continue":
            self.click_confirm_and_continue()
            return
        if label == "Continue":
            self.click_continue()
            return
        # Lives inside the activity iframe on the edit confirmation, not on the
        # page, so it needs its own handler rather than a _BUTTON_LOCATORS entry.
        if label == "Yes, Edit":
            self.click_yes_edit()
            return
        locator = self._BUTTON_LOCATORS.get(label)
        if not locator:
            raise ValueError(f"No locator mapped for the '{label}' button")
        self._click(locator, f"the '{label}' button")
        self.page.wait_for_timeout(1500)

    def click_option(self, label):
        locator = self._OPTION_LOCATORS.get(label)
        if not locator:
            raise ValueError(f"No locator mapped for the '{label}' option")
        self._click(locator, f"the '{label}' option")
        self.page.wait_for_timeout(2000)

    # Everything the (i) Overview modal carries. The redesign moved these off
    # the course page, so they are only on screen once it is open (before
    # enrollment the same panel still renders inline).
    _ABOUT_PANEL_KEYS = {
        'businessplanner-lti course banner',
        '"about this course" section',
        'course description',
        'course duration',
        'course language',
        'number of lessons',
        'number of assessments',
        '"overview" tab',
    }

    def open_overview_modal(self):
        """Show the course's About panel (the (i) beside the title)."""
        self._wait_for_page_ready()
        if self._is_visible(BP.ABOUT_COURSE_PANEL, timeout=4000):
            return True
        if not self._click_if_present(BP.COURSE_OVERVIEW_INFO_TRIGGER,
                                      "the course Overview (i) button", timeout=15000):
            print("No Overview (i) trigger on this screen")
            return False
        self.page.wait_for_timeout(2000)
        return self._is_visible(BP.ABOUT_COURSE_PANEL, timeout=10000)

    def close_overview_modal(self):
        if not self._is_visible(BP.COURSE_OVERVIEW_MODAL, timeout=2000):
            return False
        self._click_if_present(BP.COURSE_OVERVIEW_MODAL_CLOSE,
                               "the Overview modal's close button", timeout=8000)
        self.page.wait_for_timeout(1500)
        return True

    def _wait_for_page_ready(self, timeout=60000):
        """Wait out the course page's skeleton placeholders.

        The redesigned course page draws ant-skeleton blocks for tens of
        seconds before any content, so an early check reads a slow render as a
        missing element.
        """
        for selector in (".wf_spinner", ".ant-skeleton"):
            try:
                self.page.wait_for_selector(selector, state="detached", timeout=timeout)
            except Exception:
                print(f"The page still shows '{selector}' - carrying on")
        self.page.wait_for_timeout(1500)

    def click_tab(self, name):
        """Open what the feature still calls a tab.

        Only Overview is clickable now - as the (i) modal. Course Content and
        Performance became sections of the one course page, so there is
        nothing to click: the page only has to be finished rendering.
        """
        if name not in self._TAB_LOCATORS:
            raise ValueError(f"No locator mapped for the '{name}' tab")
        if name == "Overview":
            if not self.open_overview_modal():
                raise AssertionError("The course Overview could not be opened")
            return
        self.close_overview_modal()
        self._wait_for_page_ready()
        if name == "Course Content":
            self._course_content_url = self.page.url

    def click_course(self, name):
        locator = self._COURSE_LOCATORS.get(name)
        if not locator:
            raise ValueError(f"No locator mapped for the '{name}' course")
        self.scroll_carousel_to_course(name)
        self._click(locator, f"the '{name}' course")
        self.page.wait_for_timeout(3000)
        self._course_content_url = self.page.url

    def scroll_carousel_to_course(self, name, max_clicks=8):
        """Page the "Courses offered by wadhwani foundation" carousel until the
        course card is on screen.

        The listing is a react-multi-carousel, so a course further along the
        strip is in the DOM but off-screen; clicking the right arrow until it
        becomes visible avoids depending on where the card happens to sit.
        """
        locator = self._COURSE_LOCATORS.get(name)
        if self._is_visible(locator, timeout=8000):
            return True
        for attempt in range(max_clicks):
            if not self._click_if_present(
                BP.CAROUSEL_RIGHT_ARROW_BUTTON, f"carousel next arrow ({attempt + 1})", timeout=4000
            ):
                break
            self.page.wait_for_timeout(1200)
            if self._is_visible(locator, timeout=3000):
                print(f"'{name}' card reached after {attempt + 1} carousel click(s)")
                return True
        print(f"'{name}' card not brought on screen by the carousel - continuing anyway")
        return False

    # ---------- enrollment / start ----------

    def click_ordinal_button(self, label, ordinal):
        if label == "Enroll Now":
            locator = BP.ENROLL_NOW_BUTTON_FIRST if ordinal == 1 else BP.ENROLL_NOW_BUTTON_SECOND
            self._click(locator, f"the {'first' if ordinal == 1 else 'second'} 'Enroll Now' button")
            self.page.wait_for_timeout(3000)
            if ordinal == 2:
                self._course_content_url = self.page.url
            return
        if label == "Start":
            self.click_start(ordinal)
            return
        raise ValueError(f"No ordinal locator mapped for the '{label}' button")

    def click_start(self, ordinal):
        """Open the nth activity and record whether the certificate modal came up.

        The second activity is started from the course content page the first
        one navigated away from, so return there first. A finished activity's
        Start turns into "Result" and drops out of the Start query entirely, so
        when only one Start is left it is the one to click regardless of the
        ordinal the feature file names.
        """
        if ordinal > 1:
            self._return_to_course_content()
        self._activity_index = ordinal

        starts = self.page.locator(BP.START_BUTTON_ELEMENT)
        try:
            starts.first.wait_for(state="visible", timeout=15000)
        except Exception:
            # Fall back to the captured <span> locator if the button wrapper
            # does not match (e.g. the label is not a direct span child).
            starts = self.page.locator(BP.START_BUTTON)
            starts.first.wait_for(state="visible", timeout=15000)
        count = starts.count()
        index = 0 if count == 1 else min(ordinal - 1, count - 1)
        button = starts.nth(index)
        try:
            highlight_element(self.page, button)
        except Exception:
            pass
        button.click(force=True)
        print(f"Clicked the '{'first' if ordinal == 1 else 'second'}' 'Start' button "
              f"(index {index} of {count})")
        self.page.wait_for_timeout(3000)

        # The certificate-name modal is a one-time prompt raised by the FIRST
        # activity start; BusinessPlanner2 goes straight into its content.
        self._certificate_popup_shown = self._is_visible(BP.CONFIRM_AND_CONTINUE_BUTTON, timeout=8000)
        if self._certificate_popup_shown:
            print("Certificate name confirmation popup displayed")
            attach_screenshot(self.page, "Certificate name confirmation popup")
        else:
            print("Certificate name confirmation popup not shown - this activity "
                  "goes straight into its content")
            self._capture_activity_frame()

    def click_confirm_and_continue(self):
        """Dismiss the certificate-name modal and land inside the activity.

        Confirmed in the Try Activity flow: dismissing this modal does not
        always enter the lesson - "Start" sometimes has to be clicked again
        afterwards, so the Start click is retried if no activity frame loads.
        No-ops when the modal never appeared (the BusinessPlanner2 case).
        """
        if not self._certificate_popup_shown:
            print("Certificate name popup was not shown - nothing to confirm")
            if self._activity_frame is None:
                self._capture_activity_frame()
            return

        self._click(BP.CONFIRM_AND_CONTINUE_BUTTON, "the 'Confirm & Continue' button")
        self.page.wait_for_timeout(3000)

        if self._capture_activity_frame(poll_steps=8) is None:
            if self._click_if_present(BP.START_BUTTON, "'Start' again after Confirm & Continue", timeout=8000):
                self.page.wait_for_timeout(3000)
                self._capture_activity_frame()
        attach_screenshot(self.page, "Activity opened")

    # ---------- activity questions ----------

    def _plan_answers(self, fields):
        """Swap in the current activity's business for a (locator, answer) list.

        The first activity uses the answers declared alongside the section
        layout; every later one uses _PLAN2_ANSWERS, so BusinessPlanner2 fills
        the same fields with a different business instead of re-submitting the
        plan it inherited.
        """
        if self._activity_index <= 1:
            return fields
        return [(loc, self._PLAN2_ANSWERS.get(loc, answer)) for loc, answer in fields]

    def _idea_alternatives(self):
        """The Business Idea wordings for the activity currently running."""
        if self._activity_index <= 1:
            return self._BUSINESS_IDEA_ALTERNATIVES
        return self._PLAN2_IDEA_ALTERNATIVES

    def _replacing_inherited_plan(self):
        """True while an activity is overwriting a plan it inherited."""
        return self._activity_index > 1

    def _begin_editing_business_idea(self, target):
        """Unlock the Business Idea on a plan that was already reviewed.

        Confirmed against the live DOM: the reviewed plan carries exactly one
        "Edit" button (the Business Idea's), and clicking it only raises an
        "Are you sure you want to edit?" confirmation. The field stays
        read-only - and the Edit button stays on screen - until "Yes, Edit" is
        accepted, so clicking Edit on its own accomplishes nothing.
        """
        if self._is_visible(BP.WRITE_SIMPLE_SENTENCE_TEXTAREA, timeout=2500, target=target):
            return True
        if not self._is_visible(BP.ANSWER_EDIT_BUTTON, timeout=6000, target=target):
            print("  No 'Edit' button on this screen - the answer is not locked")
            return False
        try:
            target.locator(BP.ANSWER_EDIT_BUTTON).first.click(force=True)
            print("  Clicked 'Edit' on the Business Idea")
            self.page.wait_for_timeout(1200)
        except Exception:
            print("  'Edit' could not be clicked")
            return False

        if self._is_visible(BP.EDIT_CONFIRM_YES_BUTTON, timeout=8000, target=target):
            try:
                target.locator(BP.EDIT_CONFIRM_YES_BUTTON).first.click(force=True)
                print("  Confirmed the edit with 'Yes, Edit'")
                self.page.wait_for_timeout(2000)
            except Exception:
                print("  'Yes, Edit' could not be clicked")
                return False
        else:
            print("  No edit confirmation appeared - continuing")

        if self._is_visible(BP.WRITE_SIMPLE_SENTENCE_TEXTAREA,
                            timeout=LTI_CONTENT_LOAD_TIMEOUT_MS, target=target):
            print("  The Business Idea field is editable")
            return True
        print("  The Business Idea field did not become editable")
        return False

    def _reviewed_plan_edit_available(self, target=None):
        """True when this screen offers the Business Idea edit flow at all.

        An activity that opens on a blank question has nothing locked behind
        "Edit", so the feature file's edit-flow checks are reported as skipped
        there instead of failing.
        """
        target = target or self._activity_target()
        if self._is_visible(BP.ANSWER_EDIT_BUTTON, timeout=6000, target=target):
            return True
        # Once the confirmation has been accepted the answer is a live textarea
        # and the footer carries "Save & Re-evaluate" - the flow is open, not
        # absent.
        return self._is_visible(BP.SAVE_AND_RE_EVALUATE_BUTTON, timeout=2000, target=target)

    def _ensure_edit_confirmation_open(self, target=None):
        """Raise the "Are you sure you want to edit?" confirmation.

        The feature file opens it with its own "clicks on the edit button" step,
        but the confirmation's own checks call this too so they stay correct
        whichever order they run in - it no-ops once the confirmation is up.
        Returns False when this screen has no locked answer to edit.
        """
        target = target or self._activity_target()
        if self._is_visible(BP.EDIT_CONFIRM_YES_BUTTON, timeout=2500, target=target):
            return True
        if not self._is_visible(BP.ANSWER_EDIT_BUTTON, timeout=6000, target=target):
            return False
        try:
            target.locator(BP.ANSWER_EDIT_BUTTON).first.click(force=True)
            print("  Clicked 'Edit' to raise the edit confirmation")
            self.page.wait_for_timeout(1200)
        except Exception:
            print("  'Edit' could not be clicked")
            return False
        return self._is_visible(BP.EDIT_CONFIRM_YES_BUTTON, timeout=8000, target=target)

    def click_edit_button(self):
        """Click "Edit" beside a locked answer to raise the confirmation.

        Reports a skip instead of failing on an activity that opens on a blank
        question - there is nothing locked behind "Edit" there (see
        _reviewed_plan_edit_available).
        """
        if not self._ensure_edit_confirmation_open():
            print("This activity's screen has no locked answer to edit - "
                  "skipping the edit flow")
            return False
        attach_screenshot(self.page, "Raised the Business Idea edit confirmation")
        return True

    def verify_edit_popup_message(self):
        """Assert the edit confirmation's own message is displayed.

        Opens the confirmation first (see _ensure_edit_confirmation_open) and
        accepts the "Yes, Edit" button as proof it is up if the message wording
        ever changes, so a copy edit cannot fail an otherwise-passing run.
        """
        target = self._activity_target()
        if not self._ensure_edit_confirmation_open(target):
            print("This activity's screen has no locked answer to edit - skipping "
                  "the edit confirmation message check")
            return
        for locator in (BP.EDIT_CONFIRM_POPUP_MESSAGE, BP.EDIT_CONFIRM_YES_BUTTON):
            if self._is_visible(locator, timeout=8000, target=target):
                attach_screenshot(self.page, "Edit confirmation popup")
                print("Validated: the popup message for the edit button")
                return
        raise AssertionError("The edit confirmation popup message is not displayed")

    def click_yes_edit(self):
        """Accept the edit confirmation so the Business Idea becomes editable.

        No-ops when the answer is already a live textarea, and skips rather than
        failing on a screen that never locked it - the following steps
        (entering the answer, "Save & Re-evaluate") then run against whatever
        the screen does render.
        """
        target = self._activity_target()
        confirmation_open = self._is_visible(BP.EDIT_CONFIRM_YES_BUTTON, timeout=2500, target=target)
        if not confirmation_open:
            if self._is_visible(BP.WRITE_SIMPLE_SENTENCE_TEXTAREA, timeout=2500, target=target):
                print("The Business Idea answer is already editable - nothing to confirm")
                return
            if not self._ensure_edit_confirmation_open(target):
                print("This activity's screen has no edit confirmation - skipping 'Yes, Edit'")
                return
        try:
            target.locator(BP.EDIT_CONFIRM_YES_BUTTON).first.click(force=True)
        except Exception:
            raise AssertionError("The 'Yes, Edit' button could not be clicked")
        print("Clicked the 'Yes, Edit' button")
        self.page.wait_for_timeout(2000)
        if self._is_visible(BP.WRITE_SIMPLE_SENTENCE_TEXTAREA,
                            timeout=LTI_CONTENT_LOAD_TIMEOUT_MS, target=target):
            print("The Business Idea answer is now editable")
        else:
            print("The Business Idea field did not become editable after 'Yes, Edit'")
        attach_screenshot(self.page, "Confirmed the Business Idea edit")

    def _wait_for_plan_review(self, target):
        """Block until the "Reviewing your plan" overlay clears.

        The overlay covers the form, so touching the next field while it is up
        would silently do nothing.
        """
        # The overlay takes a moment to mount after the click, so give it a
        # real window to appear - a short one silently skips the wait and lets
        # the next field be typed into while the overlay still covers the form.
        if not self._is_visible(BP.REVIEWING_YOUR_PLAN_OVERLAY, timeout=10000, target=target):
            return
        print("  Plan re-evaluation running - waiting for it to finish")
        try:
            target.locator(BP.REVIEWING_YOUR_PLAN_OVERLAY).first.wait_for(
                state="hidden", timeout=PLAN_REVIEW_TIMEOUT_MS
            )
            print("  Plan re-evaluation finished")
        except Exception:
            print("  Plan re-evaluation overlay is still up - continuing anyway")

    def _save_and_re_evaluate(self, target):
        """Commit answers edited on an already-reviewed plan.

        An edit made through "Edit" is only applied by "Save & Re-evaluate",
        which re-runs the activity's review of the whole plan - without this
        the new answers are typed in and then thrown away.
        """
        if not self._is_visible(BP.SAVE_AND_RE_EVALUATE_BUTTON, timeout=8000, target=target):
            return False
        button = target.locator(BP.SAVE_AND_RE_EVALUATE_BUTTON).first
        # It ships disabled and only enables once the answer text has actually
        # changed, so a click landing too early would be swallowed.
        for _ in range(10):
            try:
                if not button.is_disabled():
                    break
            except Exception:
                break
            self.page.wait_for_timeout(500)
        try:
            button.click(force=True)
        except Exception:
            print("  'Save & Re-evaluate' could not be clicked")
            return False
        print("  Clicked 'Save & Re-evaluate'")
        self.page.wait_for_timeout(1500)
        self._wait_for_plan_review(target)
        return True

    def _fill_fields(self, target, fields, overwrite=False):
        """Fill the given (locator, answer) pairs that are visible.

        Empty fields are filled; already-answered ones are left alone unless
        `overwrite` is set, which is what lets a later activity replace the
        plan it inherited with its own business.
        """
        filled = 0
        for locator, value in fields:
            try:
                field = target.locator(locator).first
                if field.count() == 0 or not field.is_visible():
                    continue
                existing = (field.input_value() or "").strip()
                if existing and (not overwrite or existing == value):
                    continue
                if existing:
                    field.fill("")
                field.fill(value)
                filled += 1
                self._answers_entered += 1
                print(f"  Answered: {value[:70]}{'...' if len(value) > 70 else ''}")
            except Exception:
                continue
        return filled

    def _select_marketing_channel(self, target):
        """The marketing channel is a native <select>, not a textarea."""
        try:
            channel = target.locator(BP.MAIN_CHANNEL_WHATSAPP_SELECT).first
            if channel.count() and channel.is_visible() and not channel.input_value():
                channel.select_option("WhatsApp")
                self._answers_entered += 1
                print("  Selected main channel: WhatsApp")
                return 1
        except Exception:
            pass
        return 0

    def _fill_visible_answers(self, target):
        """Fill every mapped field that is currently visible.

        A later activity first clicks the inherited plan's "Edit" buttons so
        there is something to fill, then overwrites those answers with its own
        business.
        """
        overwrite = self._replacing_inherited_plan()
        return (
            self._fill_fields(target, self._plan_answers(self._ANSWER_SEQUENCE), overwrite=overwrite)
            + self._select_marketing_channel(target)
        )

    def _reveal_and_fill_answer(self, target, answer):
        """Put an answer into a screen whose fields render read-only.

        A later activity opens on the plan the earlier one submitted, where each
        answer sits behind an "Edit" button rather than in a live textarea.
        Clicking Edit is what turns one back into a fillable field. Returns
        False when the screen offers nothing to fill at all, which is a valid
        state - the plan is simply already complete.
        """
        if not self._is_visible(BP.ANY_ANSWER_TEXTAREA, timeout=5000, target=target):
            try:
                edit = target.locator(BP.ANSWER_EDIT_BUTTON).first
                if edit.count() == 0:
                    return False
                edit.click(force=True)
                self.page.wait_for_timeout(1500)
                print("  Clicked 'Edit' to make the answer field editable")
            except Exception:
                return False
            if not self._is_visible(BP.ANY_ANSWER_TEXTAREA, timeout=10000, target=target):
                return False
        try:
            field = target.locator(BP.ANY_ANSWER_TEXTAREA).first
            field.fill("")
            field.fill(answer)
        except Exception:
            return False
        self._answers_entered += 1
        print(f"  Answered: {answer[:70]}{'...' if len(answer) > 70 else ''}")
        self._save_and_re_evaluate(target)
        return True

    def _fill_all_sections(self, target):
        """Expand each business-plan section in turn and fill its fields.

        The sections are collapsible and only the open one's textareas are
        visible, so a fill pass restricted to what is on screen leaves the rest
        of the plan blank - which is how an almost-empty plan used to reach
        "Submit for review". Clicking each heading first is what makes the
        activity's questions actually all get answered.
        """
        filled = 0
        overwrite = self._replacing_inherited_plan()
        for name, heading, section_fields in self._SECTIONS:
            fields = self._plan_answers(section_fields)
            # Two attempts: a section whose fields had not rendered yet when the
            # heading was clicked would otherwise be skipped silently, and there
            # is no guaranteed second sweep (the "Fill More Fields" fallback is
            # only offered once). Re-clicking also recovers the case where the
            # first click collapsed a section that was already open.
            for attempt in (1, 2):
                try:
                    header = target.locator(heading).first
                    if header.count() and header.is_visible():
                        header.click(force=True)
                        self.page.wait_for_timeout(1200)
                        print(f"  Opened section '{name}'")
                except Exception:
                    print(f"  Section '{name}' could not be expanded - filling whatever is visible")

                # A section's own textareas are directly writable once it is
                # expanded - only the Business Idea sits behind "Edit".
                section_filled = self._fill_fields(target, fields, overwrite=overwrite)
                if name == "Marketing":
                    section_filled += self._select_marketing_channel(target)
                if section_filled:
                    print(f"  Filled {section_filled} field(s) in '{name}'")
                filled += section_filled

                if section_filled or not self._section_has_empty_field(target, fields):
                    break
                if attempt == 1:
                    print(f"  '{name}' still has empty fields - reopening it")
        return filled

    def _section_has_empty_field(self, target, fields):
        """True while any of the section's fields is missing or still blank."""
        for locator, _ in fields:
            try:
                field = target.locator(locator).first
                if field.count() == 0:
                    return True
                if not (field.input_value() or "").strip():
                    return True
            except Exception:
                return True
        return False

    def _handle_rejected_business_idea(self, target):
        """Reword the Business Idea answer when the activity rejects it.

        The activity validates that the answer really describes a business and
        blocks with "OK, I'll change it" when it does not - resubmitting the
        same text would just loop, so each rejection moves to the next wording.
        """
        if not self._is_visible(BP.OK_ILL_CHANGE_IT_BUTTON, timeout=2500, target=target):
            return False
        target.locator(BP.OK_ILL_CHANGE_IT_BUTTON).first.click(force=True)
        print("  Business Idea answer was rejected - rewording it")
        self.page.wait_for_timeout(1000)

        self._business_idea_attempt += 1
        alternatives = self._idea_alternatives()
        alternative = alternatives[self._business_idea_attempt % len(alternatives)]
        try:
            field = target.locator(BP.WRITE_SIMPLE_SENTENCE_TEXTAREA).first
            field.fill("")
            field.fill(alternative)
            print(f"  Reworded Business Idea: {alternative[:70]}...")
        except Exception:
            print("  Business Idea field not editable after rejection")
        return True

    def _handle_submit_dialog(self, target):
        """Answer the "Submit for review" confirmation.

        It offers "Fill More Fields" (back to the form) and "Submit Now ->".
        The first time it appears the form is sent back for another filling
        pass so nothing optional is left blank; the second time it is submitted.
        """
        if not self._is_visible(BP.SUBMIT_NOW_BUTTON, timeout=3000, target=target):
            return False
        if not self._fill_more_fields_used and self._is_visible(
            BP.FILL_MORE_FIELDS_BUTTON, timeout=2000, target=target
        ):
            target.locator(BP.FILL_MORE_FIELDS_BUTTON).first.click(force=True)
            self._fill_more_fields_used = True
            print("  Clicked 'Fill More Fields' to complete the remaining fields")
            self.page.wait_for_timeout(2000)
            return True
        target.locator(BP.SUBMIT_NOW_BUTTON).first.click(force=True)
        self._submitted_for_review = True
        print("  Clicked 'Submit Now'")
        self.page.wait_for_timeout(3000)
        return True

    def answer_current_question(self):
        """One fill-and-advance cycle: answer what is on screen, then continue.

        Returns True while the activity is still progressing and False once
        there is nothing left to fill or click, which is what
        complete_all_required_questions loops on.
        """
        target = self._activity_target()
        try:
            target.locator(BP.ANY_ANSWER_TEXTAREA).first.wait_for(
                state="visible", timeout=LTI_CONTENT_LOAD_TIMEOUT_MS
            )
        except Exception:
            print("  No answer field rendered on this screen")

        acted = bool(self._fill_visible_answers(target))

        if self._handle_submit_dialog(target):
            return True

        # A visible Continue means this is still a question screen - advance and
        # come back rather than treating it as the final plan form.
        if self._click_advance(target, "Continue", BP.CONTINUE_BUTTON):
            if self._handle_rejected_business_idea(target):
                return True
            return True

        # No Continue: this is the collapsible business-plan form. Every section
        # has to be expanded and filled BEFORE submitting, otherwise only the
        # one open section gets answered and a near-empty plan is submitted.
        if self._fill_all_sections(target):
            acted = True

        if self._click_advance(target, "Submit for review", BP.SUBMIT_FOR_REVIEW_BUTTON):
            acted = True
            self._handle_submit_dialog(target)

        if self._handle_rejected_business_idea(target):
            return True
        return acted

    def _click_advance(self, target, name, locator):
        try:
            button = target.locator(locator).first
            if button.count() == 0 or not button.is_visible() or button.is_disabled():
                return False
            button.click(force=True)
            print(f"  Advanced with '{name}'")
            self.page.wait_for_timeout(2500)
            return True
        except Exception:
            return False

    def enter_business_idea_answer(self):
        """Answer the Business Idea question without advancing the screen.

        The feature file validates the answer and the Continue button between
        entering the text and clicking Continue, so filling and advancing are
        deliberately kept as two separate steps here.
        """
        target = self._activity_target()
        answer = self._idea_alternatives()[0]
        # An inherited plan shows the earlier activity's idea as read-only text.
        # Edit + "Yes, Edit" is what unlocks it so this activity can replace it
        # with its own business.
        if self._replacing_inherited_plan():
            self._begin_editing_business_idea(target)

        field = target.locator(BP.WRITE_SIMPLE_SENTENCE_TEXTAREA).first
        try:
            field.wait_for(state="visible", timeout=LTI_CONTENT_LOAD_TIMEOUT_MS)
        except Exception:
            # The step is replayed for BusinessPlanner2, which may open on a
            # different question - answer the one it does show instead.
            if self._activity_index <= 1:
                raise
            print("The Business Idea field is not on this activity's opening screen - "
                  "answering the question it does show")
            if not self._fill_visible_answers(target):
                if not self._reveal_and_fill_answer(target, answer):
                    print("  Every answer on this screen was already filled in by the "
                          "earlier activity - there is nothing left to enter")
            attach_screenshot(self.page, "First question answered")
            return
        field.fill("")
        field.fill(answer)
        self._answers_entered += 1
        print(f"Entered the Business Idea answer: {answer}")
        # Replacing the inherited idea only takes effect once it is saved and
        # the activity has re-reviewed the plan against it.
        if self._replacing_inherited_plan():
            self._save_and_re_evaluate(target)
        attach_screenshot(self.page, "Business Idea answer entered")

    def click_continue(self):
        target = self._activity_target()
        button = target.locator(BP.CONTINUE_BUTTON).first
        try:
            button.wait_for(state="visible", timeout=20000)
        except Exception:
            # Same replayed step on a screen that advances through its own
            # "Submit for review" control instead of a Continue button.
            if self._activity_index <= 1:
                raise
            print("No 'Continue' button on this activity's screen - it advances "
                  "through its own submit control")
            return
        button.click(force=True)
        print("Clicked the 'Continue' button")
        self.page.wait_for_timeout(2500)
        self._handle_rejected_business_idea(target)

    def complete_all_required_questions(self, activity_name, max_cycles=40):
        """Drive the activity to completion, then return to Course Content.

        The number of screens differs per activity and per run, so this keeps
        answering whatever is on screen until the form is submitted or two
        consecutive cycles find nothing to do.
        """
        print(f"Completing all required questions in the {activity_name} activity")
        idle = 0
        for cycle in range(max_cycles):
            if self._submitted_for_review:
                break
            print(f" [cycle {cycle + 1}]")
            if self.answer_current_question():
                idle = 0
            else:
                idle += 1
                if idle >= 2:
                    print("  Nothing left to answer - activity appears finished")
                    break
        print(f"Answered {self._answers_entered} field(s) in the {activity_name} activity")
        attach_screenshot(self.page, f"{activity_name} activity completed")
        self._return_to_course_content()
        # The next activity starts from a clean modal/frame/answer state.
        self._certificate_popup_shown = False
        self._submitted_for_review = False
        self._fill_more_fields_used = False
        self._answers_entered = 0
        print(f"{activity_name} activity completed and returned to Course Content")

    # ---------- validations ----------

    def verify_logged_in(self, base_url):
        """Make the scenario runnable on its own.

        The shared pre-login in environment.py is skipped for newuser-only runs
        (that feature registers its own account), and this scenario can also be
        run by name. So: use the session if one is already open, and log in with
        the configured student credentials when there is not.
        """
        BusinessPlannerPage.activate()
        page = self.page
        if page.url in ("about:blank", ""):
            page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)

        for locator in (BP.HOME_BUTTON, "//button[@aria-label='Accounts menu']", BP.COURSES_AND_PROGRAMS_HEADING):
            if self._is_visible(locator, timeout=8000):
                print("User is already logged into the WSN application")
                attach_screenshot(page, "Logged into the WSN application")
                return

        from utils.config import Config
        from pages.login_page import LoginPage

        username, password = Config.get_credentials(Config.get_persona())
        login_page = LoginPage(page)
        login_page.open(base_url)
        login_page.dismiss_popup_if_present()
        login_page.click_get_started()
        login_page.click_continue_with_email()
        login_page.login(username, password)
        login_page.wait_for_home_page()
        attach_screenshot(page, "Logged into the WSN application")
        print("Logged into the WSN application")

    def verify_visible(self, description):
        """Assert one "the user should be able to see the ..." element."""
        key = " ".join(description.strip().lower().split())
        entry = self._VIEW_TARGETS.get(key)
        if entry is None:
            raise ValueError(
                f"No locator mapped for 'the user should be able to see the {description}' - "
                "add it to BusinessPlannerPage._VIEW_TARGETS"
            )
        locator, scope, soft = entry
        if key in self._ABOUT_PANEL_KEYS:
            self.open_overview_modal()
        candidates = locator if isinstance(locator, (list, tuple)) else [locator]
        # Opening-screen checks are only guaranteed on the first activity - see
        # _FIRST_ACTIVITY_SCREEN_TARGETS.
        first_screen_only = (
            key in self._FIRST_ACTIVITY_SCREEN_TARGETS and self._activity_index > 1
        )

        if scope == "certificate" and not self._certificate_popup_shown:
            print(f"Certificate popup not shown for this activity - skipping '{description}'")
            return
        target = self.page if scope in ("page", "certificate") else self._activity_target()

        # The Business Idea edit flow only exists on a plan an earlier activity
        # already submitted; "edit_popup" additionally needs the confirmation to
        # be up, which is what the check itself raises.
        if scope in ("edit", "edit_popup"):
            available = (
                self._ensure_edit_confirmation_open(target) if scope == "edit_popup"
                else self._reviewed_plan_edit_available(target)
            )
            if not available:
                print(f"This activity's screen has no locked answer to edit - "
                      f"skipping '{description}'")
                return

        # A shorter per-candidate wait keeps a multi-candidate check from adding
        # up to a minute of dead time when the first XPath is the wrong guess.
        timeout = 15000 if len(candidates) == 1 else 8000
        for candidate in candidates:
            if self._is_visible(candidate, timeout=timeout, target=target):
                print(f"Validated: {description}")
                return
        if first_screen_only:
            print(f"'{description}' is not on the BusinessPlanner{self._activity_index} "
                  "activity's opening screen - skipping this check for the current activity")
            return
        if soft:
            print(f"'{description}' not found with its best-guess locator - "
                  "verify the XPath in business_planner_locators.py")
            return
        raise AssertionError(f"'{description}' is not visible")

    def verify_navigated_to(self, destination):
        """Assert a page/tab actually rendered after a navigation click."""
        checks = {
            "home": [BP.EXPLORE_THINGS_TO_DO_HEADING, BP.HOME_BUTTON],
            "courses": [BP.COURSES_OFFERED_BY_WADHWANI_FOUNDATION_HEADING, BP.BUSINESSPLANNER_LTI_HEADING],
            "businessplanner-lti course": [BP.COURSE_TITLE_HEADING, BP.COURSE_OVERVIEW_HEADING],
            "course overview": [BP.COURSE_OVERVIEW_HEADING, BP.COURSE_OVERVIEW_IMAGE_SECTION],
            "course content": [BP.COURSE_CONTENT_HEADING, BP.VALIDATE_BUSINESSPLANNER1_HEADING],
        }
        key = " ".join(destination.strip().lower().split())
        locators = checks.get(key)
        if locators is None:
            raise ValueError(f"No navigation check mapped for the '{destination}' page")
        for locator in locators:
            if self._is_visible(locator, timeout=15000):
                attach_screenshot(self.page, f"Navigated to the {destination} page")
                print(f"Navigated to the {destination} page")
                return
        raise AssertionError(f"The {destination} page did not render")

    def verify_navigated_to_activity(self, activity_name):
        target = self._activity_target()
        if target is self.page and self._activity_frame is None:
            self._capture_activity_frame(poll_steps=8)
            target = self._activity_target()
        # A textarea only proves the activity opened when it opens on a blank
        # question. BusinessPlanner2 carries over the plan BusinessPlanner1
        # submitted and lands on the reviewed form instead - read-only answers,
        # Edit buttons, Save / Submit for review, and no textarea at all - so
        # that form counts as the activity having rendered too.
        for locator in (BP.ANY_ANSWER_TEXTAREA, BP.PLAN_FORM_LANDED):
            if self._is_visible(locator, timeout=LTI_CONTENT_LOAD_TIMEOUT_MS // 2, target=target):
                attach_screenshot(self.page, f"{activity_name} activity opened")
                print(f"Navigated to the {activity_name} activity")
                return
        raise AssertionError(f"The {activity_name} activity content did not render")

    def verify_tab_selected(self, name):
        """Confirm the tab is the active one.

        Confirmed on the live DOM: the selected tab's <p> carries an extra
        "active-tab" class alongside "tab-heading-text-active" (which every tab
        has, selected or not), so the selected state is that one class.
        """
        locator = self._TAB_LOCATORS.get(name)
        if not locator:
            raise ValueError(f"No locator mapped for the '{name}' tab")
        if not self._is_visible(locator, timeout=15000):
            raise AssertionError(f"The '{name}' tab is not visible")

        active = f"//p[contains(@class,'active-tab') and normalize-space(text())='{name}']"
        if self._is_visible(active, timeout=8000):
            print(f"The '{name}' tab is selected")
            return
        raise AssertionError(f"The '{name}' tab is visible but not the selected one")

    def verify_enrollment_popup(self):
        for locator in (BP.NOT_NOW_BUTTON, BP.ENROLL_NOW_BUTTON_SECOND, BP.START_LEARNING_WITH_YOUR_COURSE_TEXT):
            if self._is_visible(locator, timeout=15000):
                attach_screenshot(self.page, "Enrollment confirmation popup")
                print("Enrollment confirmation popup displayed")
                return
        raise AssertionError("The enrollment confirmation popup did not appear")

    def verify_enrolled(self):
        for locator in (BP.SUCCESSFULLY_ENROLLED_TEXT, BP.COURSE_PROGRESS_BAR_CONTAINER, BP.OVERALL_SCORE_GAUGE):
            if self._is_visible(locator, timeout=25000):
                attach_screenshot(self.page, "Enrolled in the BusinessPlanner-LTI course")
                print("Successfully enrolled in the BusinessPlanner-LTI course")
                return
        raise AssertionError("Enrollment could not be confirmed - no success message or progress section")

    def verify_certificate_popup(self):
        if not self._certificate_popup_shown:
            print("Certificate name confirmation popup is only raised by the first "
                  "activity - skipping this check for the current activity")
            return
        if not self._is_visible(BP.CONFIRM_AND_CONTINUE_BUTTON, timeout=10000):
            raise AssertionError("The certificate name confirmation popup is no longer displayed")
        print("Certificate name confirmation popup displayed")

    def verify_profile_updated(self):
        """The certificate-name confirmation is what updates the profile name.

        Nothing is asserted when the modal never appeared, because then no
        profile update was triggered for this activity in the first place.
        """
        if not self._certificate_popup_shown:
            print("No certificate name confirmation for this activity - no profile update to verify")
            return
        if self._is_visible(BP.CONFIRM_AND_CONTINUE_BUTTON, timeout=5000):
            raise AssertionError("The certificate name popup is still open - the profile was not updated")
        print("Profile updated successfully")

    def verify_answer_entered(self):
        """Confirm an answer was actually entered.

        Checked against the running count rather than "some visible field holds
        text": by the time this step runs the answering step may have expanded
        the next (empty) plan section or submitted the form, so a field-content
        check would fail on a screen where every answer was in fact entered.
        """
        target = self._activity_target()
        try:
            fields = target.locator(BP.ANY_ANSWER_TEXTAREA)
            for i in range(fields.count()):
                field = fields.nth(i)
                if field.is_visible() and (field.input_value() or "").strip():
                    print("Answer entered successfully")
                    return
        except Exception:
            pass
        if self._answers_entered:
            print(f"Answer entered successfully ({self._answers_entered} so far in this activity)")
            return
        # A later activity can open on a plan whose answers were all entered by
        # the earlier one; they render read-only behind "Edit" buttons, so an
        # Edit button IS an answer that has been entered.
        if self._activity_index > 1 and self._is_visible(
            BP.ANSWER_EDIT_BUTTON, timeout=5000, target=target
        ):
            print("The answers on this screen were already entered in the earlier activity")
            return
        raise AssertionError("No answer has been entered in this activity")

    def verify_continue_enabled(self):
        target = self._activity_target()
        button = target.locator(BP.CONTINUE_BUTTON).first
        try:
            button.wait_for(state="visible", timeout=15000)
        except Exception:
            if self._activity_index <= 1:
                raise AssertionError("The 'Continue' button did not appear")
            print("This activity's screen has no 'Continue' button - skipping the "
                  "enabled check")
            return
        if button.is_disabled():
            raise AssertionError("The 'Continue' button is disabled")
        print("The 'Continue' button is enabled")

    def verify_next_question_displayed(self):
        target = self._activity_target()
        if self._is_visible(BP.ANY_ANSWER_TEXTAREA, timeout=LTI_CONTENT_LOAD_TIMEOUT_MS, target=target):
            print("The next question is displayed")
            return
        # The last Continue of a screen submits it, so a submit control showing
        # instead of another answer field is also a valid "moved on" state.
        for locator in (BP.SUBMIT_FOR_REVIEW_BUTTON, BP.SUBMIT_NOW_BUTTON):
            if self._is_visible(locator, timeout=5000, target=target):
                print("The activity moved on to its submit step")
                return
        raise AssertionError("The activity did not move on to the next question")

    def verify_activity_completed(self, activity_name):
        for locator in (BP.RESULT_BUTTON, BP.COMPLETED_STATUS, BP.COURSE_PROGRESS_BAR_CONTAINER):
            if self._is_visible(locator, timeout=15000):
                attach_screenshot(self.page, f"{activity_name} marked as completed")
                print(f"The {activity_name} activity is marked as completed")
                return
        print(f"Could not confirm the {activity_name} activity's completed state on the "
              "Course Content page - verify the Result/Completed locators")

    def verify_progress_updated(self):
        for locator in (BP.COURSE_PROGRESS_BAR_CONTAINER, BP.OVERALL_SCORE_GAUGE):
            if self._is_visible(locator, timeout=15000):
                print("Progress is displayed and updated")
                return
        print("Progress section not found - verify the progress locators")

    def verify_back_on_course_content(self):
        for locator in (BP.COURSE_CONTENT_HEADING, BP.VALIDATE_BUSINESSPLANNER1_HEADING,
                        BP.VALIDATE_ASSESMENTS_HEADING_ACTUAL):
            if self._is_visible(locator, timeout=20000):
                attach_screenshot(self.page, "Back on the Course Content page")
                print("Navigated back to the Course Content page")
                return
        raise AssertionError("The Course Content page was not restored after the activity")
