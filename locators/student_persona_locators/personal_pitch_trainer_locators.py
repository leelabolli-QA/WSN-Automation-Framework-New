class PersonalPitchTrainerLocators:
    HOME = "//div[text()='Home']"
    PERSONAL_PITCH_TRAINER = "//h6[text()='Personal Pitch Trainer']"
    CREATE_YOUR_PITCH_BUTTON = "//button[text()='Create Your Pitch']"
    PITCH_TRAINER_BACK_ARROW_BUTTON = "//img[@class='wf_image redirection-image no-js-pitch-trainer-back-arrow']"
    # Page objects resolve locators with `.first`, so no positional index is needed.
    PITCH_SUMMARY_VIEW_BUTTON = "//p[text()='View']"
    VIEW_PITCH_BUTTON = "//p[text()='View Pitch']"
    VIDEO_PLAY_BUTTON = "//video[text()='Your browser does not support the video tag.']"
    VIDEO_CLOSE_BUTTON = "//span[@class='ant-modal-close-x']"
    SHARE_PITCH_BUTTON = ("//p[normalize-space()='View Pitch']/ancestor::button"
                          "/following-sibling::button[1]")
    COPY_SHARE_BUTTON = "//img[@class='wf_image  no-js-share-button-copy']"
    SHARE_PITCH_CLOSE_BUTTON = "//span[@class='ant-modal-close-x']"
    PERSONAL_PITCH_TRAINER_PASSED_TEXT = "//p[contains(text(), 'Passed')]"
    VALIDATE_CHECK_BUTTON = "(//div[@class='dot-line'])[5]"