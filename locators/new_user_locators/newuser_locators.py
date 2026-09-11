class NewUserLocators:
    GET_STARTED_BUTTON = "//button[text()='Get Started']"
    CONTINUE_WITH_EMAIL = "//p[text()='Continue with Email']"
    EMAIL_INPUT = "//input[@placeholder='Enter your Email ID']"
    NEXT_BUTTON = "//button[text()='Next']"
    VERIFY_BUTTON = "//button[text()='Verify']"
    NEW_PASSWORD_INPUT = "//input[@placeholder='Add New Password']"
    CONFIRM_PASSWORD_INPUT = "//input[@placeholder='Confirm Password']"
    SUBMIT_BUTTON = "//button[text()='Submit']"
    FIRST_NAME_INPUT = "//input[@id='firstName']"
    LAST_NAME_INPUT = "//input[@id='lastName']"
    TERMS_AND_CONDITIONS_CHECKBOX = "(//span[@class='ant-checkbox-inner'])[1]"
    SEARCH_CITY_LABEL = "//label[text()='Search City']"
    # Search City is an ant-design searchable select: the label above only opens it -
    # the actual typeable input is this following <input>, confirmed via live DOM inspection.
    SEARCH_CITY_INPUT = "//label[text()='Search City']/following::input[1]"
    # Options render as two <p> lines (city name + "district, state, country"), not a
    # single comma-joined string - match the first rendered option instead of exact text
    # (whichever city ends up first depends on what was typed into SEARCH_CITY_INPUT).
    MUMBAI_OPTION = "(//div[contains(@class,'ant-select-item-option-content')])[1]"
    PRIVACY_POLICY_CHECKBOX = "(//span[@class='ant-checkbox-inner'])[3]"
    SUBMIT_BUTTON = "//button[text()='Submit']"
    # The dashboard card was relabelled "Programs & Courses" when the app
    # merged the separate Courses and Programs screens; PROD still renders the
    # older "Courses" wording, so both are accepted and one locator serves
    # newuser.feature and newuser_prod.feature.
    COURSES_HEADER = (
        "//h6[text()='Courses']"
        "|//h6[text()='Programs & Courses']"
    )
    # Not present in the original locator list - confirmed via live DOM inspection that
    # "Course Content" is a tab (not an h6), tag-agnostic match used since the exact
    # element type wasn't captured.
    COURSE_CONTENT_TAB = "//*[normalize-space(text())='Course Content']"
    VALIDATE_IN_PROGRESS_HEADER = "//h5[contains(text(),'In Progress')]"
    VALIDATE_COMPLETED_HEADER = "//h5[contains(text(),'Completed')]"
    VALIDATE_COURSES_OFFERED_BY_WADHWANI_FOUNDATION_HEADER = "//h6[text()='Programs & Courses recommended by your institute']"
    DEV_TRY_ACTIVITY_SELF_SERVE = "//h4[text()='Dev-Try activity-Self serve']"
    # PROD equivalent of the dev course above ("QA Try Test"). The dev card's
    # rendered text ("Dev-Try activity-Self serve") already differs in case and
    # separators from the name used in the feature file, so this matches the
    # three words case-insensitively instead of pinning exact punctuation -
    # tighten to an exact text() match once the live PROD DOM is confirmed.
    _LOWER = "translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
    QA_TRY_TEST = (
        f"//h4[contains({_LOWER},'qa') and contains({_LOWER},'try') and contains({_LOWER},'test')]"
    )
    ENROLL_NOW_BUTTON = "(//button[text()='Enroll Now'])[1]"
    ENROLL_NOW_BUTTON_SECOND = "(//button[text()='Enroll Now'])[2]"
    START_COURSE_BUTTON = "//button[text()='Start Course']"
    # The lesson names differ between environments - confirmed via live DOM
    # inspection of the PROD "QA-Try Test" course, whose Course Content lists
    # "Try" / "Try Self Serve" where the dev course lists "Try Activity" /
    # "Try Self Serve Activity". Both spellings are accepted so one locator
    # serves newuser.feature and newuser_prod.feature.
    TRY_ACTIVITY = "//p[normalize-space(text())='Try Activity' or normalize-space(text())='Try']"
    TRY_SELF_SERVE_ACTIVITY = (
        "//p[normalize-space(text())='Try Self Serve Activity'"
        " or normalize-space(text())='Try Self Serve']"
    )
    START_BUTTON = "//span[text()='Start']"
    CONFIRM_AND_CONTINUE_BUTTON = "//button[text()='Confirm & Continue']"
    FACTORY_AND_PRODUCTION_WORK = "//span[text()='Factory & Production Work']"
    CHOOSE_JOB_ROLE_SELECTED_RADIO_BUTTON = "//span[@class='ant-radio ant-radio-checked']"
    NEXT_BUTTON = "//button[text()='Next']"
    WRITE_YOUR_PROMPT_HERE_TEXTAREA = "//textarea[@placeholder='Write your prompt here']"
    SUBMIT_BUTTON_SECOND = "//button[text()='Submit']"
    ORANGE_RIGHT_ARROW_BUTTON = "//img[@class='wf_image  no-js-Orange_rightArrow']"
    SECOND_RADIO_INPUT = "(//input[@class='ant-radio-input'])[2]"
    CONTINUE_BUTTON = "//button[text()='Continue']"
    FOURTH_RADIO_INPUT = "(//input[@class='ant-radio-input'])[4]"
    SUBMIT_BUTTON_THIRD = "//button[text()='Submit']"
    GENERATE_AUDIO_BUTTON = "//button[text()='Generate Audio']"
    AUDIO_PLAY_BUTTON = "//img[@class='wf_image restart-button visible no-js-try-play-icon']"
    THUMBSUP_SUITABLE_OPTION_IMAGE = "//img[@class='wf_image suitable-option-image no-js-try-like-icon']"
    TRY_OTHER_VOICES_BUTTON = "//button[text()='Try other voices']"
    #if it ask for other play audio thenbelow locators are used
    FIFTH_RADIO_INPUT = "(//input[@class='ant-radio-input'])[5]"
    SUBMIT_BUTTON_FOURTH = "//button[text()='Submit']"
    FINISH_BUTTON = "//button[text()='Finish']"
    WRITE_YOUR_PROMPT_HERE_TO_GENERATE_IMAGE_USING_AI_TEXTAREA = "//textarea[@placeholder='Write your prompt here to generate image using AI']"
    EVALUATE_MY_PROMPT_BUTTON = "//button[text()='Evaluate my prompt']"
    NEXT_LESSON = "//p[text()='Next Lesson']"
    SELECT_RANDOM_JOB_ROLE_FOR_ME_BUTTON = "//button[text()='Select a random job role for me']"
    BEGIN_CONVERSATION_BUTTON = "//button[text()='Begin Conversation →']"
    TYPE_OR_SPEAK_YOUR_RESPONSE_TEXTAREA = "//textarea[@placeholder='Type or speak your response…']"
    SEND_BUTTON = "//button[text()='Send']"
    TRY_NEW_SCENARIO_BUTTON = "//button[text()='Try New Scenario']"
    SECOND_ARROW_BUTTON = "(//button[@class='ant-btn ant-btn-default default_button arrow-btns'])[2]"
    # Best-guess text-match XPaths, not yet confirmed via live DOM inspection - verify
    # against the app. The "No scenarios found" message shows up transiently right
    # after clicking a job category (e.g. FACTORY_AND_PRODUCTION_WORK) before the
    # scenario actually loads.
    NO_SCENARIOS_FOUND_TEXT = "//*[contains(text(),'No scenarios')]"
    # Confirmed via a live screenshot of the score screen ("Your Highest Score: 4").
    YOUR_HIGHEST_SCORE_TEXT = "//*[contains(text(),'Your Highest Score')]"

    # ---------- Join a batch with a job/batch key ----------
    # (features/newuser_prod.feature > "PROD - New user enrolls with the job key")

    # The header avatar that opens the account dropdown. The %3e in the class is
    # a URL-encoded ">" and is part of the real class string, not a typo - it is
    # kept verbatim. ACCOUNTS_MENU_TRIGGER_FALLBACK is the same control addressed
    # by its aria-label (what the faculty/settings flows use), tried second so a
    # restyled icon cannot break this step.
    ACCOUNTS_MENU_TRIGGER = "//img[@class='wf_image header_profile_menu_trigger__icon no-js-svg%3e']"
    ACCOUNTS_MENU_TRIGGER_FALLBACK = "//button[@aria-label='Accounts menu']"
    # Confirmed via live DOM inspection: "Join a batch" is NOT a menu entry that
    # opens a modal - it is a card rendered inside the dropdown itself
    # (div.header-join-batch-card > h6.header-join-batch-card__title + the code
    # input and Enroll button), so the header IS the clickable entry.
    JOIN_A_BATCH_CARD = "//div[contains(@class,'header-join-batch-card')]"
    VALIDATE_JOIN_BATCH_HEADER = "//h6[text()='Join a batch']"
    JOIN_A_BATCH_MENU_ITEM = VALIDATE_JOIN_BATCH_HEADER
    # input.ant-input.normal_input.header-join-batch-card__input.code-input
    JOIN_A_BATCH_CODE_INPUT = "//input[@placeholder='Enter code here']"
    # The label is a <span class="text">Enroll</span> INSIDE the submit button,
    # and that button ships disabled until a code has been typed - so the click
    # has to target the button (and wait for it to enable), not the span.
    ENROLL_BUTTON = (
        "//button[contains(@class,'header-join-batch-card__submit')]"
        "|//span[text()='Enroll']/ancestor::button[1]"
    )
    # Best-guess success/error text. Verified on dev that a REJECTED code
    # renders no message at all - the code simply stays in the field - so the
    # enrollment check does not rely on either of these: it treats "the card
    # closed or cleared the code" as enrolled and "the code is still sitting in
    # the field" as rejected. These only shortcut that check when the app does
    # render a message.
    BATCH_ENROLLED_SUCCESS_TEXT = (
        "//*[contains(text(),'Enrolled')]"
        "|//*[contains(text(),'enrolled')]"
        "|//*[contains(text(),'Successfully')]"
    )
    BATCH_ENROLL_ERROR_TEXT = (
        "//*[contains(text(),'Invalid')]"
        "|//*[contains(text(),'invalid')]"
        "|//*[contains(text(),'expired')]"
    )


    # ---------- negative paths ----------
    # (features/newuser.feature > the "@negative" block)
    #
    # Best-guess containers for inline field errors: the app is ant-design based
    # (ant-form-item-explain-error) but also renders its own error <p>/<span>
    # elsewhere, so both shapes are matched. NOT yet confirmed against a live
    # invalid-input screen - which is why no negative check *requires* one of
    # these to be present. Each one asserts the flow did not advance (the next
    # screen never rendered / the button stayed disabled) and treats a matching
    # message only as extra evidence to log and screenshot.
    VALIDATION_ERROR_MESSAGE = (
        "//*[contains(@class,'ant-form-item-explain-error')]"
        "|//*[contains(@class,'error-message')]"
        "|//*[contains(@class,'errorMessage')]"
        "|//*[contains(@class,'error_message')]"
        "|//*[contains(@class,'input-error')]"
        "|//*[contains(@class,'wf_error')]"
        "|//*[contains(text(),'valid email')]"
        "|//*[contains(text(),'do not match')]"
        "|//*[contains(text(),'does not match')]"
        "|//*[contains(text(),'required')]"
    )
    # The OTP screen has only ever been driven manually (enter_otp_manually just
    # waits for the password screen to appear), so no OTP field was needed until
    # the "invalid OTP" scenario. Best guess covering both shapes this widget
    # takes - one field, or a row of single-character boxes; enter_otp() focuses
    # the first match and types, which auto-advances the box-style variant.
    OTP_INPUT = (
        "//input[contains(@placeholder,'OTP') or contains(@placeholder,'otp')]"
        "|//input[contains(@id,'otp')]"
        "|//input[contains(@class,'otp')]"
    )
