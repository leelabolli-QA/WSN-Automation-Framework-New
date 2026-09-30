Feature: Student Persona
  Scenario: Validate Home Dashboard
    Given user is on the home page
  #   # Then user validates the home icon
    # Then user validates the welcome header and wadhwani skilling header
    Then user clicks on Programs and Courses card
    Then user clicks on personal pitch trainer card
    Then user clicks on Interview coach card
    Then user clicks on forums card
    Then user clicks on My carrer advisory card
    Then user clicks on Carrer Buddy card
    Then user clicks on Jobs Connect card
    Then user clicks on menu help icon
    Then user clicks on notification icon
    Then user clicks on profile icon
    Then user clicks on header profile menu icon 
    Then user clicks on Calender
    Then user clicks on messages and discussions
    # Then user clicks on learning progress
    Then user clicks on settings

  Scenario: Validate Genie
    Given user is on the home page
    Then user validates genie
  Scenario: Validate Jobs Connect
    Given user is on the home page
    Then user navigates to home page
    Then user clicks on jobsconnect card
    Then user clicks on jobtype and selects full time option
    Then user clicks on workmode filter and selects office option
    Then user clicks on industry sector filter and selects automotive option
    Then user clicks on education level filter and selects graduate option
    Then user clicks on search by role title and fills product manager and clicks on find jobs
    Then user clicks on first job card
    Then user validates about the job and about the company sections
    Then user validates apply button and closes the current tab and navigate to jobs connect page
    Then user clicks on reset button
    Then user clicks on jobs connect applied status card
    Then user clicks on applied jobs button and validates the applied job card

  Scenario: Validate Forums
    Given user is on the home page
    Then user navigates to home page
    Then user clicks on forums card
    Then user validates the my forums header
    Then user clicks on view forum button
  Scenario: Validate Courses and Programs
    Given user is on the home page
    Then user navigates to Programs & Courses page
    # Validate In Progress and Completed tabs
    Then user validates the In Progress and Completed tabs
    # Validate In Progress Course
    When user clicks on the In Progress tab
    Then user validates the enrolled course cards
    When user opens the "QA-Emp skill Test-V2" course

    # Validate Course Detail Page
    Then user validates the course detail page
    Then user validates the Pre Video icon
    Then user clicks on the Pre Video icon
    Then user validates the Pre Video popup
    Then user clicks on the right arrow button if the pre video not started
    Then user click on the back navigation arrow button and again clicks on the pre video icon
    Then user closes the Pre Video popup

    Then user validates the Collaborate icon
    Then user clicks on the Collaborate icon
    Then user validates the Collaborate popup
    Then user closes the Collaborate popup

    Then user validates the Assessments icon
    Then user clicks on the Assessments icon
    Then user validates the Assessments popup
    Then user closes the Assessments popup

    Then user validates the Post Video icon
    Then user clicks on the Post Video icon
    Then user validates the Post Video popup
    Then user closes the Post Video popup

    # Navigate back to Courses & Programs
    Then user navigates back to the Programs & Courses list

    # Validate Completed Courses
    When user clicks on the Completed tab
    Then user validates the completed course cards

    # Validate Resume Course type
    Then user validates the Dev-Try activity-Self serve course
    Then user validates the completed course and clicks on Resume Course option
    Then user should see the "complete all citeria message" screen and if it's available then user clicks on the "COURSE_CONTENT_BACK_ARROW" and should land on the "complete all citeria message" screen
    Then user validates the complete all citeria message
    Then user clicks on the "COURSE_BACK_BUTTON" from the "complete all citeria message" screen
    When user clicks on the Completed tab
    Then user validates the completed course cards

    # Validate Certificate type
    Then user validates Dev-Think-Lti-open course
    Then user validates certificate button
    Then user clicks on "Dev-Think-Lti-open" course completed button
    Then user validates certificate image, download certificate button and share button
    Then user clicks on the download certificate button
    Then user clicks on the share button
    Then user clicks on the scorecard download link if it's available or else skip this
    Then user navigates back to the Programs & Courses list

    # Validate Scorecard and Certificate type
    Then user validates HPS Test-QA2 course
    Then user validates certificate button and scorecard button
    Then user clicks on "HPS Test-QA2"course completed button
    Then user validates certificate image, download certificate button, share button and download score card button
    Then user clicks on the download certificate button
    Then user clicks on the share button
    Then user clicks on the scorecard download link if it's available or else skip this
    Then user navigates back to the Programs & Courses list
    
    # Validate Institute Recommendations
    Then user validates Courses & Programs recommended by institute
    Then user validates the recommended course and program cards

    # Validate Wadhwani Foundation Recommendations
    Then user validates Courses & Programs recommended by Wadhwani Foundation
    Then user validates the recommended course and program cards

    # Validate Join a Batch
    Then user validates the Join a batch section

  # Scenario: Validate Courses & programs
  #   Given user is on the home page
  #   Then user navigates to home page
  #   Then user validates the courses In Progress and Completed tabs
  #   Then user clicks on the courses In Progress tab
  #   Then user validates enrolled course card
  #   Then user opens the first course
  #   Then user validates the course detail sections
  #   Then user expands the first lesson section
  #   Then user navigates back to the courses list
  #   Then user clicks on the courses Completed tab
  #   Then user opens the first course
  #   Then user validates the assessment score
  #   Then user navigates back to the courses list
  #   Then user validates courses recommended by institute
  #   Then user validates recommended course card
  #   Then user validates courses offered by wadhwani foundation
  Scenario: Validate Career Buddy
    Given user is on the home page
    Then user navigates to home page
    Then user clicks on Career Buddy card
    Then user clicks on language dropdown and selects the language and click on apply button
    Then user clicks on language close button
    Then user clicks on sector dropdown and selects the sector and click on apply button
    Then user clicks on sector close button
    Then user clicks on location dropdown and selects the location and click on apply button
    Then user clicks on location close button
    Then user clicks on job role dropdown and selects the job role and click on apply button
    Then user clicks on job role close button
    Then user clicks on search mentor and fill the details
    Then user clicks on the recommended mentor card
    Then user validates the sector jobrole and language details
    Then user clicks on the Book a Session button
    Then user selects the available date and clicks on the slot button
    Then user clicks on session purpose label and selects the Job Search Strategy option
    Then user clicks on specific outcome label and fills in the specific outcome fields, selects the checkbox option and clicks on the Book button
    Then user clicks on the Copy Link option and validates the copied link
  Scenario: Validate Interview Coach
    Given user is on the home page
    Then user navigates to home page
    Then user navigates to interview coach card
    Then user clicks on audio button image
    Then user validates textbox and mic button in Interview Coach page
    Then user fills the textbox and clicks on send icon
    Then user clicks on Practise Interviewing for the role
    Then user validates start button
    Then user clicks on pitch trainer back icon
    Then user validates your recent roles header
    Then user validates ongoing header and completed header
    Then user clicks on threedots icon
    Then user clicks on delete this role icon and confirms delete action
    Then user clicks on home icon and navigates to home page
  Scenario: Validate My Career Advisor
    Given user is on the home page
    Then user navigates to home page
    Then user clicks on My Career Advisor card
    Then user validates the Passion header and clicks on the Review button
    Then user selects the passion items and clicks on the Submit button
    Then user validates the Questionnaire header
    Then user clicks on the Review button in the Aptitudes section
    Then user clicks on the Reattempt button
    Then user clicks on the slider choose button
    Then user selects the 1st question option. If the slider sequence is on 9, the user clicks on 10. If the slider sequence is on 10, the user clicks back on 9
    Then user clicks on the Update button
    Then user clicks on the Go to Matched Roles button
    Then user clicks on Without College Degree
    Then user validates the header count
    Then user clicks on the searched role
    Then user fills in the job role input field
    Then user validates the Result header and clicks on Favourite
    Then user clicks on the Favourites header
    Then user clicks on Share Report and clicks on the Share button
    Then user clicks on the Favourite button and removes the favourite
    Then user clicks on the home icon and navigates to home page
    Then user clicks on roles saved card and click on favourites header and validate the favourite role header
  Scenario: Validate Personal Pitch Trainer
    Given user is on the home page
    Then user navigates to home page
    Then user clicks on personal pitch trainer card
    Then user clicks on create pitch button
    Then user clicks on create your pitch back button
    Then user clicks on pitch summary view button
    Then user clicks on view pitch button
    Then user clicks on video play button
    Then user clicks on video close button
    Then user clicks on share pitch button
    Then user clicks on copy pitch button
    Then user clicks on share pitch close button
    Then user clicks on home icon and navigates to home page
    Then user clicks on passed text on personal pitch trainer card 
    Then user validates check button 
  # Programs now live on the same merged "Programs & Courses" screen as courses;
  # the old Enroll -> Confirm/Cancel modal no longer exists.
  # Scenario: Validate Programs
  #   Given user is on the home page
  #   Then user navigates to home page
  #   Then user validates the programs In Progress and Completed tabs
  #   Then user clicks on the programs In Progress tab
  #   Then user validates program card
  #   Then user validates recommended by institue header
  #   Then user validates recommended program card
  #   Then user validates offered by wadhwani foundation header
  #   Then user validates join a batch section
  Scenario: Messages and discussions validation
    Then user clicks on Accounts menu
    Then user clicks on Messages & Discussions
    Then user clicks on first chat in the list
    Then user sends a message
    Then user validates the latest message sent
    Then user clicks on file upload button
    Then user uploads document in to the chat and validates
    Then user clicks on file upload button
    Then user uploads photo in to chat and validates
    Then user navigates to home page
# Scenario: Learning progress validation
#     Then user clicks on Accounts menu
#     Then user clicks on learning progress
#     Then user validates the learning progress
#     Then user navigates to learning progress page and clicks on completed courses
#     Then user clicks on a completed course and validates overview, content, performance sections, score value and overall progress
#     Then user clicks on share certificate button and validates download certificate option
#     Then user clicks on ongoing courses and validates overview section
#     Then user clicks on content section and clicks on resume
#     Then user clicks on performance section and validates final score
  Scenario: Settings ZoomConnect validation
      Then user clicks on Account menu
      Then user clicks on settings menu
      Then user validates the settings sections
      Then user clicks on zoom accounts menu and validates accounts_meetings section
      Then user clicks on sign in with zoom right arrow button
      Then user validates the zoom account delinked popup and closed the popup
      Then user validates the sign in with zoom section and turn on the toggle button
      Then user navigates to meetings section and click on signin button
      Then user navigates to zoom.us signin screen and validates the email address, password, signin buttons
      Then user clicks on email input field and enter the email id
      Then user clicks on password input field and enter the password
      Then user clicks on sigin button
      Then user navigates back to to signin with zoom screen and validates the toggle button status
      Then user click on the toggle button and validates the disconnect section
      Then user clicks on the disconnect button
      Then user click on back arrow and navigates to settings screen
  Scenario: Settings DeleteAccount validation
      Then user clicks on Account menu
      Then user clicks on settings menu
      Then user validates the settings sections
      Then user clicks on accounts menu and validates delete account section
      Then user clicks on delete account right arrow button
      Then user validates the delete account popup and clicks on the get otp button
      Then user validates the otp input field and clicks on the delete account otp section back arrow
      Then user navigates to delete account section and click on close icon
      Then user navigates to settings screen
  Scenario: Settings WhatsappNotifications validation
      Then user clicks on Account menu
      Then user clicks on settings menu
      Then user validates the settings sections
      Then user clicks on notifications menu and validates whatsapp container section
      Then user clicks on whatsapp container section right arrow button
      Then user validates the whatsapp section and clicks on the toggle button
      Then user clicks on the whatsapp section back arrow and validates the settings section
  Scenario: Notifications validation
      Then user clicks on notification icon
      Then user validates the notifications
      Then user clicks on first notification  
      Then user navigates to home page
 