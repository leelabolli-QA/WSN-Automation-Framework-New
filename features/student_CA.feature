Feature: Student CA Management
  @ca-card
  Scenario: Validate Career Advisor card and page
    Given the user opens the WSN application
    When the user clicks on "Continue with Email"
    And the user enters a valid email address manually
    And the user enters the OTP manually
    And the user completes the registration form
    And the user clicks on "Submit"
    Then the user should be registered successfully
    And the user should reach the application
    Given user is on homepage
    Then user validates the CA card in homepage and click on it
    Then user validates the CA card details in the subsequent page

  @sequential @passions @fresh-user
  Scenario: Fresh user selects Arts and Design
    Given user is on Career Advisor page
    Then user selects the Arts & Design option
    Then user click on submit button in passions section
  @sequential @questionnaires @interests
  Scenario: Complete interests questionnaire
    Given user is on Career Advisor page
    Then user clicks on questionnaires section
    Then user clicks on interests card in questionnaires section and clicks on reattempt button
    Then user clicks on questionnaries choose button and clicks on question cards and click on next button
    Then user attempts all the questions in interests section and clicks on next button
  @sequential @questionnaires @aptitudes
  Scenario: Complete aptitudes questionnaire
    Given user is on Career Advisor page
    Then user clicks start aptitudes and answer all the questions in aptitudes section and clicks on next button
  @sequential @questionnaires @values
  Scenario: Complete values questionnaire
    Given user is on Career Advisor page
    Then user clicks on start values and answer all the questions in values section and clicks on next button
  @sequential @reattempt @interests
  Scenario: Reattempt interests section
    Given user is on Career Advisor page
    Then user clicks on interests card and clicks on reattempt button
    Then user slides the slider to 7 or 8 or 8 or 7 and clicks on next button
    Then user clicks on submit button in interests section
    Then user clicks on backarrow button
  @sequential @reattempt @aptitudes
  Scenario: Reattempt aptitudes section
    Given user is on Career Advisor page
    Then user clicks on aptitudes card and clicks on reattempt button
    Then user slides the slider to 7 or 8 or 8 or 7 and clicks on next button
    Then user clicks on submit button in aptitudes section
    Then user clicks on backarrow button
  @sequential @reattempt @values
  Scenario: Reattempt values section
    Given user is on Career Advisor page
    Then user clicks on values card and clicks on reattempt button
    Then user slides the slider to 7 or 8 or 8 or 7 and clicks on next button
    Then user clicks on submit button in values section
    Then user clicks on backarrow button
  @sequential @roles @search
  Scenario: Search roles and save a job
    Given user is on Career Advisor page
    Then user clicks on search roles
    Then user enters jobrole and add the first job as add saved
    Then user clicks on save menu header and validates the saved job
    Then user clicks on compare roles
    Then user clicks on first and second checkbox in search results and clicks on compare button
  @sequential @roles @compare
  Scenario: Compare roles
    Given user is on Career Advisor page
    Then user clicks on compare roles
    Then user clicks on first and second checkbox in search results and clicks on compare button
  @sequential @share-report
  Scenario: Share report validation
    Given user is on Career Advisor page
    Then user clicks on share report and click and validates the share report options
    Then user validates self review, matched roles, and favourite roles tabs in share report section
    Then user clicks on Saved menu and removes the saved job from favourites
  @help
  Scenario: Help icon validation
    Given user is on Career Advisor page
    Then user clicks on help icon
  # ------------------------------------------------------------------
  # Added coverage: recommendation explanations, search edge cases,
  # the saved-roles page and About.
  #
  # These are deliberately NOT tagged @sequential - each one re-enters CA from
  # the dashboard, and none of them builds
  # state for the next, so they are safe to run individually or in any order.
  # ------------------------------------------------------------------
  @roles
  Scenario: Recommended roles explain why they were recommended
    Given user is on Career Advisor page
    Then user validates the why this recommendation option on recommended roles
  @search
  Scenario: Search returns matching job roles
    Given user is on Career Advisor page
    Then user clicks on search roles
    Then user searches for the job role "Developer"
    Then user validates the search results are returned
  @search @negative
  Scenario: Search shows no related jobs for an unmatched query
    Given user is on Career Advisor page
    Then user clicks on search roles
    Then user searches for the job role "zzzqqqxyz123notarole"
    Then user validates no related jobs are found
  @search
  Scenario: Search results can be cleared and searched again
    Given user is on Career Advisor page
    Then user clicks on search roles
    Then user searches for the job role "Developer"
    Then user validates the search results are returned
    Then user clears the search input
    Then user searches for the job role "Engineer"
    Then user validates the search results are returned
  @saved
  Scenario: Saved roles page lists saved roles with compare option
    Given user is on Career Advisor page
    Then user clicks on save menu header and validates the saved job
    Then user validates the saved roles page
  @about
  Scenario: About page describes the app and its key features
    Given user is on Career Advisor page
    Then user clicks on about icon
    Then user validates the about page details
