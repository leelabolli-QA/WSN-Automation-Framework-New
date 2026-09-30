Feature: New_user
    Scenario: New user completes registration and finishes the Dev Try Activity Self Serve course
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user completes the registration form
        And the user clicks on "Submit"
        Then the user should be registered successfully

        When the user clicks on "Courses"
        And the user selects the "Dev Try Activity - Self Serve" course
        And the user clicks on the first "Enroll Now" button
        And the user clicks on the second "Enroll Now" button
        Then the course should be enrolled successfully

        When the user clicks on "Course Content"
        And the user opens the "Try Activity"
        And the user completes all the required activities
        Then all Try Activity tasks should be completed successfully

        When the user opens the "Try Self Serve Activity"
        And the user clicks on the first "Start" button
        And the user clicks on the factory and production work
        And the user answers all the available questions
        And the user selects any job category or selects a random job role
        And the user answers all the available questions
        Then the first self-serve activity should be completed successfully

        When the user clicks on the second "Start" button
        And the user clicks on the factory and production work
        And the user answers all the available questions
        And the user selects any job category or selects a random job role
        And the user answers all the available questions
        Then the second self-serve activity should be completed successfully
        #And user should navigate back to courses page 


    Scenario: User validates Business Planner LTI course and completes all required activities

        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user completes the registration form
        And the user clicks on "Submit"
        Then the user should be registered successfully
        When the user clicks on the "Home" button
        Then the user should be navigated to the Home page
        And the user should be able to see the "Explore things to do" section
        # The dashboard card reads "Programs & Courses" since the redesign.
        And the user should be able to see the "Programs & Courses" option
        # And the user should be able to see the "Programs" option
        And the user should be able to see the "My Career Advisor" option
        And the user should be able to see the "Personal Pitch Trainer" option
        And the user should be able to see the "Interview Coach" option
        And the user should be able to see the "Forums" option

        When the user clicks on the "Programs & Courses" option
        Then the user should be navigated to the Courses page
        And the user should be able to see the "Courses offered by wadhwani foundation" section
        And the user should be able to see the available courses
        And the user should be able to see the "BusinessPlanner-LTI" course
        And the user should be able to see the BusinessPlanner-LTI course image
        And the user should be able to see the BusinessPlanner-LTI course duration
        And the user should be able to see the course navigation button

        When the user clicks on the "BusinessPlanner-LTI" course
        Then the user should be navigated to the BusinessPlanner-LTI course page
        And the user should be able to see the "BusinessPlanner-LTI" course title
        # REMOVED BY THE REDESIGN: the course page has no Overview / Course
        # Content / Performance tabs any more. Overview opens as a modal from
        # the (i) beside the title (the "clicks on the Overview tab" step
        # below still does that), and the curriculum and certificate blocks are
        # sections of the one page.
        # And the user should be able to see the "Overview" tab
        # And the user should be able to see the "Course Content" tab
        # And the user should be able to see the "Performance" tab
        And the user should be able to see the "Enroll Now" button

        When the user clicks on the first "Enroll Now" button
        Then the enrollment confirmation popup should be displayed
        And the user should be able to see the "Start learning with your course" message
        And the user should be able to see the "Not now" button
        And the user should be able to see the second "Enroll Now" button

        When the user clicks on the second "Enroll Now" button
        Then the user should be successfully enrolled in the BusinessPlanner-LTI course
        And the enrollment success message should be displayed
        And the user should be able to see the "Successfully Enrolled!" message
        And the user should be able to see the course progress section
        # REMOVED BY THE REDESIGN: the overall score gauge is gone - a score
        # only exists once the assessment has been attempted, and it renders as
        # the assessment score tile.
        # And the user should be able to see the overall score
        And the user should be able to see the overall progress

        # Opens the (i) Overview modal now; everything under it is read there.
        When the user clicks on the "Overview" tab
        Then the user should be navigated to the course overview page
        # REMOVED BY THE REDESIGN: no tab strip, so nothing to be "selected".
        # And the "Overview" tab should be selected
        And the user should be able to see the BusinessPlanner-LTI course banner
        And the user should be able to see the "About this course" section
        And the user should be able to see the course description
        And the user should be able to see the course duration
        And the user should be able to see the course language
        And the user should be able to see the number of lessons
        And the user should be able to see the number of assessments

        # No longer a tab - this closes the Overview modal and waits for the
        # curriculum section of the course page.
        When the user clicks on the "Course Content" tab
        Then the user should be navigated to the Course Content page
        # REMOVED BY THE REDESIGN: no tab strip, so nothing to be "selected".
        # And the "Course Content" tab should be selected
        And the user should be able to see the "BusinessPlanner1" section
        And the user should be able to see the lesson completion status
        And the user should be able to see the "BusinessPlanner1" activity
        And the user should be able to see the "BusinessPlanner2" activity
        And the user should be able to see the "Assessments" section
        And the user should be able to see the activity count
        And the user should be able to see the first "Start" button

        When the user clicks on the first "Start" button
        Then the certificate name confirmation popup should be displayed
        And the user should be able to see the "Review Your Certificate Name" message
        And the user should be able to see the certificate name
        And the user should be able to see the "Review Profile" button
        And the user should be able to see the "Confirm & Continue" button

        When the user clicks on the "Confirm & Continue" button
        Then the user should be navigated to the BusinessPlanner1 activity
        And the user should be able to see the BusinessPlanner1 activity page
        And the user should be able to see the activity progress
        And the user should be able to see the "Business Idea" question
        And the user should be able to see the instructions for the Business Idea question
        And the user should be able to see the answer field
        And the user should be able to see the "Continue" button

        When the user enters the required answer for the Business Idea question
        Then the answer should be entered successfully
        And the "Continue" button should be enabled

        When the user clicks on the "Continue" button
        Then the user should be able to proceed to the next required question
        And the next question should be displayed
        And the user should be able to see the required answer field
        And the user should be able to enter the required answer
        And the user should be able to continue to the next question

        When the user completes all the required questions in the BusinessPlanner1 activity
        Then all the required questions should be completed
        And all the required answers should be submitted successfully
        And the activity progress should be updated
        And the BusinessPlanner1 activity should be marked as completed
        And the user should be navigated back to the course content page

        Then the user should be able to see the completed status for the BusinessPlanner1 activity
        And the user should be able to see the "Result" button for the completed activity
        And the user should be able to see the "Start" button for the BusinessPlanner2 activity

        When the user clicks on the second "Start" button
        # Then the certificate name confirmation popup should be displayed
        # And the user should be able to see the "Review Your Certificate Name" message
        # And the user should be able to see the certificate name
        # And the user should be able to see the "Review Profile" button
        # And the user should be able to see the "Confirm & Continue" button

        # When the user clicks on the "Confirm & Continue" button
        # Then the profile should be updated successfully
        Then the user should be navigated to the BusinessPlanner2 activity
        And the user should be able to see the BusinessPlanner2 activity page
        And the user should be able to see the activity progress
        And the user should be able to see the "Business Idea" question
        And the user should be able to see the instructions for the Business Idea question
        And the user should be able to see the answer field
        And the user should be able to see the "Continue" button
        And the user should be able to see the edit button
        And the user should able to see the popup message for the edit button
        And the user should be able to see the "cancel" button
        And the user should be able to see the "Yes, Edit" button
        And the user should be able to click on the "Yes, Edit" button
        And the user should be able to see the answer field for the Business Idea question
        And the user should be able to see the "save and re evaluate" button for the Business Idea question
        When the user enters the required answer for the Business Idea question
        Then the answer should be entered successfully
        And the "Continue" button should be enabled

        When the user clicks on the "Continue" button
        Then the user should be able to proceed to the next required question
        And the next question should be displayed
        And the user should be able to see the required answer field
        And the user should be able to enter the required answer
        And the user should be able to continue to the next question

        When the user completes all the required questions in the BusinessPlanner2 activity
        Then all the required questions should be completed
        And all the required answers should be submitted successfully
        And the activity progress should be updated
        And the BusinessPlanner2 activity should be marked as completed
        And the user should be navigated back to the course content page

        Then the user should be able to see the completed status for the BusinessPlanner2 activity
        And the user should be able to see the "Result" button for the completed activity
        And the user should be able to see the updated lesson completion status
        And the overall course progress should be updated


    #THINK LTI COURSE
    @think_lti
    Scenario: Register a new user for the Dev-Think LTI course
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user completes the registration form
        And the user clicks on "Submit"
        Then the user should be registered successfully

    @think_lti
    Scenario: User validates Dev-Think LTI course,completes Think activities and assessment

        Given the user is successfully logged into the WSN application
        Then the user should be navigated to the Home page
        # The dashboard redesign added a Jobs Connect card - seven now, not six.
        And the user should be able to see all 7 cards under "Explore things to do"
    @think_lti
    Scenario: Homepage Validation
        # The first card is labelled "Programs & Courses" now (was "Courses and Programs").
        Then the user should be able to see the "Programs & Courses" card
        # And the user should be able to see the "Programs" card
        And the user should be able to see the "Jobs Connect" card
        And the user should be able to see the "My Career Advisor" card
        And the user should be able to see the "Personal Pitch Trainer" card
        And the user should be able to see the "Interview Coach" card
        And the user should be able to see the "Career Buddy" card
        And the user should be able to see the "Forums" card

        When the user clicks on the "Programs & Courses" card
        Then the user should be able to see the courses offered by Wadhwani Foundation

        When the user clicks on the "Dev-Think LTI-Open" course
        Then the user should be able to see the course overview page

    # The course page lost its Overview / Course Content / Performance tabs.
    # Duration, language, the banner and "About this course" now open in an
    # Overview modal from the (i) beside the course title, which these steps
    # open for themselves.
    @think_lti
    Scenario: Course Overview Validation
        And the user should be able to validate the course duration as "2 hours"
        And the user should be able to validate the course language as "English"
        And the user should be able to validate the course image
        And the user should be able to validate the "About this course" heading
        And the user should be able to validate the course content

    @think_lti
    Scenario: User enrolls in Dev-Think LTI course
        When the user clicks on the "Enroll Now" button
        Then the user should be able to see the "Enroll Now" popup
        And the user should be able to see the "Not now" button
        And the user should be able to see the "Enroll Now" button

        When the user clicks on the "Enroll Now" button in the popup
        Then the user should be successfully enrolled in the course
        # REMOVED BY THE REDESIGN: there is no "Start Course" button on either
        # state of the course page. Enrollment is now proven by the Enroll Now
        # button disappearing and the curriculum rendering, which the step
        # above checks.
        # And the user should be able to see the "Start Course" button
        # REMOVED BY THE REDESIGN: the course page no longer shows an overall
        # score gauge or an overall progress badge, so there is no 0%/0% to read
        # on a freshly enrolled course. Progress is per section now
        # ("0/1 Lesson Completed") and a score only appears once the assessment
        # has been attempted.
        # And the user should be able to validate the overall score as "0%"
        # And the user should be able to validate the overall progress as "0%"

        # No longer a tab - the curriculum is a section of the course page, so
        # this step just waits for it to finish rendering.
        When the user clicks on the "Course Content" tab
        Then the user should be able to see the "Dev think LTI" section

        When the user clicks on the "Start" button for the Dev think LTI activity
        Then the user should be able to see the Think Activity question

    @think_lti
    Scenario: User completes Think activities and Orientation
        When the user selects the correct answer for Think 1
        And the user clicks on the "Submit" button
        Then the user should be able to see the successful completion message
        And the user should be able to see the "Finish" button

        When the user clicks on the "Finish" button
        Then the user should be able to see the completed tick symbol for "think 1"
        And the user should be able to access "think 2"

        When the user answers the Think 2 question
        And the user clicks on the "Submit" button
        Then the user should be able to see the "Finish" button

        When the user clicks on the "Finish" button
        Then the user should be able to see the "Orientation" section

        When the user completes the Orientation PDF
        Then the user should be able to proceed to the Assessment section

    @think_lti
    Scenario: User completes the Dev-Think assessment
        When the user clicks on the "Attempt quiz" button
        Then the user should be able to start the assessment
        And the user should be able to see 5 questions

        When the user answers all 5 questions
        And the user clicks on the "Next" button for each question
        Then the user should be navigated to the next question
        And the user's answer should be saved

        When the user completes all 5 questions
        And the user clicks on the "Finish attempt" button
        Then the user should be able to see the quiz summary page
        And the user should be able to see the "Back" button
        And the user should be able to see the "Submit all and finish" button

        When the user clicks on the "Submit all and finish" button
        Then the user should be able to see the "Submit all your answers and finish?" popup
        And the user should be able to see the "Cancel" button
        And the user should be able to see the "Submit all and finish" button

        When the user clicks on the "Submit all and finish" button in the popup
        Then the user should be able to see the quiz score page
        And the user should be able to validate the total number of questions
        And the user should be able to validate the number of answered questions
        And the user should be able to validate the number of correct answers
        And the user should be able to validate the number of partially correct answers
        And the user should be able to validate the number of incorrect answers
        And the user should be able to validate the overall score

        When the user clicks on the "Finish review" button
        Then the user should be navigated back to the Assessment page

    # There is no Performance tab any more: leaving the assessment lands back on
    # the course page, which is where the score tile and the certificate block
    # now live. (The score tile's "See Details in 'Performance' Tab" is a plain
    # label and navigates nowhere.)
    @think_lti
    Scenario: User validates Dev-Think performance details
        When the user clicks on the Assessment back arrow button
        Then the user should be navigated to the Performance page

        # REMOVED BY THE REDESIGN: the course-level Overall Score and Overall
        # Progress widgets are gone. What the page shows instead is the
        # assessment score tile (the Final Score step below) and each section's
        # "n/m Lesson Completed" status.
        # Then the user should be able to see the Overall Score
        # And the user should be able to see the Overall Progress
        Then the user should be able to see the Final Score
        # The earned-certificate block is headed "Congratulations !" now and its
        # action reads "Download Certificate".
        And the user should be able to see the "Congratulations" section
        And the user should be able to see the certificate eligibility message
        And the user should be able to see the "Download Certificate" option and click on the "Download certificate" button
        And the user should be able to see the "Share certificate" option and click on the "share certificate" button and paste the link in new tab 
        And the user should be able to see the "Assessments" section and click on the "Assessments progress arrow" and should see the data in assessments popup and then click on the ASSESSMENTS_PROGRESS_ARROW_POPUP_CLOSE_BUTTON
        And the user should be able to see the "Earned Micorcertificates" card and click on the earned microcertificate button
        And the user should be able to see the "Earned Microcertifacate" details with download & share certificate buttons
        And the user should be able to download the "Microcertificate" and click on the "share certificate" button and paste it in new tab
        # REMOVED BY THE REDESIGN: the Performance tab's assessments table
        # (name, score, attempt date, weightage) no longer exists - the page
        # keeps only an "Assessments" node on the CERTIFICATE PROGRESS strip.
        # And the user should be able to see the assessment name
        # And the user should be able to see the assessment score
        # And the user should be able to see the attempt date
        # And the user should be able to see the assessment weightage

    #DO-LTI course scenarios------------------------------------------------------------------------------------
    Scenario: New user enrolls in Do-LTI course using the job key and completes Do-LTI activities

        Given the user opens the WSN application
        When the user clicks on the Accounts menu
        And the user clicks on "Join a Batch"
        Then the user should be able to see the batch enrollment popup/page
        And the user should be able to see the Job Key/Job Code input field
        And the user should be able to see the "Enroll" button
        When the user enters a valid Job Key/Job Code
        And the user clicks on the "Enroll" button
        Then the user should be enrolled successfully
        And the user should be navigated to the Home page

    Scenario: Home Page Validation

        Then the user should be able to see the "Home" option in the header
        And the user should be able to see the Help icon
        And the user should be able to see the Notifications icon
        And the user should be able to see the user profile/menu icon
        And the user should be able to see the "Explore things to do" section
        And the user should be able to see the "Courses" card
        And the user should be able to see the "Programs" card
        And the user should be able to see the "My Career Advisor" card
        And the user should be able to see the "Personal Pitch Trainer" card
        And the user should be able to see the "Interview Coach" card
        And the user should be able to see the "Career Buddy" card
        And the user should be able to see the "Forums" card
        And the user should be able to see the active course count on the "Courses" card
        And the user should be able to verify that all homepage cards are displayed properly
        And the user should be able to verify that the card names and descriptions are displayed correctly

    Scenario: Navigate to Courses

        When the user clicks on the "Courses" card
        Then the user should be navigated to the Courses page
        And the user should be able to see the "In Progress" tab
        And the user should be able to see the "Completed" tab
        And the user should be able to see the Do-LTI course under the In Progress section
        And the user should be able to see the course name "Do-LTI_QA"
        And the user should be able to see the course type as "Batch Course"
        And the user should be able to see the course progress
        And the user should be able to see the certificate eligibility information
        And the user should be able to see the "View Details" option
        And the user should be able to see the "Resume" button
        And the user should be able to see the "Courses Recommended by Your Institute" section
        And the user should be able to see the recommended course cards
        And the user should be able to see the course name, duration and navigation option for the recommended courses

    Scenario: Do-LTI Course

        When the user clicks on the "Resume" button for the Do-LTI course
        Then the user should be navigated to the Do-LTI course page
        And the user should be able to see the course name "Do-LTI_QA"
        And the user should be able to see the "Start Course" button
        And the user should be able to see the Overall Score
        And the user should be able to see the Overall Progress
        And the user should be able to see the "Overview" tab
        And the user should be able to see the "Course Content" tab
        And the user should be able to see the "Performance" tab
        And the user should be able to verify that the Overview tab is selected by default
        And the user should be able to see the "About this course" section
        And the user should be able to see the course duration
        And the user should be able to see the language information
        And the user should be able to see the "View Batch" option

    Scenario: Course Content

        When the user clicks on the "Course Content" tab
        Then the user should be able to see the "Orientation" section
        And the user should be able to see the "Do-LTI" section
        And the user should be able to see the "Assessments" section
        And the user should be able to see the completion status for each section
        And the user should be able to expand and collapse the sections
        And the user should be able to see the Orientation activity
        And the user should be able to see the Do-LTI activities
        And the user should be able to see "Do-LTI-1"
        And the user should be able to see "Do-LTI-2"

    Scenario: Do-LTI Activity 1

        When the user clicks on "Do-LTI-1"
        Then the user should be navigated to the Do-LTI-1 activity page
        And the user should be able to see the activity content
        And the user should be able to see the Do-LTI activity navigation panel
        And the user should be able to see "Do-LTI-1" in the activity navigation panel
        And the user should be able to see "Do-LTI-2" in the activity navigation panel
        And the user should be able to see the activity video/session
        And the user should be able to see the video controls
        And the user should be able to see the Play button
        And the user should be able to play the session

        When the user clicks on the Play button
        Then the session/video should start playing
        And the user should be able to watch the session until completion
        And the user should be able to see the "Continue" button after completing the session

        When the user clicks on the "Continue" button
        Then the user should be navigated to the Do Activity questions
        And the user should be able to see the activity question
        And the user should be able to see the available answer options
        And the user should be able to select an answer
        And the user should be able to see the "Submit" button

        When the user selects the required answer
        And the user clicks on the "Submit" button
        Then the answer should be submitted successfully
        And the user should be able to see the answer result/feedback
        And the user should be able to see the "Continue" button

        When the user clicks on the "Continue" button
        Then the user should be navigated to the next activity question
        And the user should be able to select the required answer
        And the user should be able to click on the "Submit" button
        And the user should be able to click on the "Continue" button

        When the user completes the third activity question
        And the user selects the required answer
        And the user clicks on the "Submit" button
        Then the user should be able to see the result for the third question
        And the user should be able to see that all 3 questions are completed
        And the user should be able to see the activity result
        And the user should be able to see the score/result summary
        And the user should be able to see the "Next" button

        When the user clicks on the "Next" button
        Then the user should be navigated to the next step/activity
        And the user should be able to see the Do-LTI activity completion status

    Scenario: Do-LTI Activity 2

        When the user clicks on "Do-LTI-2"
        Then the user should be navigated to the Do-LTI-2 activity page
        And the user should be able to see the activity content
        And the user should be able to see the Do-LTI-2 activity in the navigation panel
        And the user should be able to see the activity video/session
        And the user should be able to see the Play button
        And the user should be able to see the video controls

        When the user clicks on the Play button
        Then the Do-LTI-2 session/video should start playing
        And the user should be able to watch the session until completion
        And the user should be able to see the "Continue" button

        When the user clicks on the "Continue" button
        Then the user should be navigated to the Do Activity questions
        And the user should be able to see the first question
        And the user should be able to see all available answer options
        And the user should be able to select the required answer
        And the user should be able to see the "Submit" button

        When the user selects the required answer
        And the user clicks on the "Submit" button
        Then the answer should be submitted successfully
        And the user should be able to see the result/feedback
        And the user should be able to see the "Continue" button

        When the user clicks on the "Continue" button
        Then the user should be navigated to the second question
        And the user should be able to select the required answer
        And the user should be able to click on the "Submit" button
        And the user should be able to click on the "Continue" button

        When the user completes the third question
        And the user selects the required answer
        And the user clicks on the "Submit" button
        Then the user should be able to see the result/feedback
        And the user should be able to see that all 3 questions are completed
        And the user should be able to see the final activity result
        And the user should be able to see the "Next" button

        When the user clicks on the "Next" button
        Then the user should be navigated to the next step
        And the user should be able to see that the Do-LTI-2 activity is completed
        And the user should be able to verify the updated completion status

    Scenario: Final Course Validation

        When the user navigates back to the Course Content page
        Then the user should be able to see the updated completion status for Do-LTI
        And the user should be able to see the completed status for Do-LTI-1
        And the user should be able to see the completed status for Do-LTI-2
        And the user should be able to verify that the completed activities are marked with the completed/tick indicator

    Scenario: Orientation Completion

        When the user completes the Orientation PDF
        Then the user should be able to proceed to the Assessment section
        And the user should be able to see the "Assessments" section
        And the user should be able to see the assessment activity

    Scenario: Start Assessment

        When the user clicks on the "Attempt quiz" button
        Then the user should be able to start the assessment
        And the user should be able to see the quiz navigation
        And the user should be able to see 5 questions
        And the user should be able to see the question and available answer options

    Scenario: Answer Assessment Questions

        When the user answers all 5 questions
        And the user clicks on the "Next" button for each question
        Then the user should be navigated to the next question
        And the user's answer should be saved
        And the user should be able to navigate between the questions using the quiz navigation

    Scenario: Finish Assessment

        When the user completes all 5 questions
        And the user clicks on the "Finish attempt" button
        Then the user should be able to see the quiz summary page
        And the user should be able to see the status of each question
        And the user should be able to see the "Back" button
        And the user should be able to see the "Submit all and finish" button

    Scenario: Submit Assessment Confirmation

        When the user clicks on the "Submit all and finish" button
        Then the user should be able to see the "Submit all your answers and finish?" popup
        And the user should be able to see the confirmation message
        And the user should be able to see the "Cancel" button
        And the user should be able to see the "Submit all and finish" button

        When the user clicks on the "Cancel" button
        Then the popup should be closed
        And the user should remain on the quiz summary page

        When the user clicks on the "Submit all and finish" button in the popup
        Then the user should be able to see the quiz score page

    Scenario: Quiz Score Validation

        Then the user should be able to validate the total number of questions
        And the user should be able to validate the number of answered questions
        And the user should be able to validate the number of correct answers
        And the user should be able to validate the number of partially correct answers
        And the user should be able to validate the number of incorrect answers
        And the user should be able to validate the overall score
        And the user should be able to see the quiz completion status

    Scenario: Finish Quiz Review

        When the user clicks on the "Finish review" button
        Then the user should be navigated back to the Assessment page
        And the user should be able to see the Assessment page
        And the user should be able to see the assessment completion status

    Scenario: Navigate to Performance

        When the user clicks on the Assessment back arrow button
        Then the user should be navigated to the Performance page

    Scenario: Performance Page Validation

        Then the user should be able to see the "Overall Score"
        And the user should be able to see the "Overall Progress"
        And the user should be able to see the "Final Score"
        And the user should be able to see the final score percentage
        And the user should be able to see the "Your Certificate Is Available" section
        And the user should be able to see the certificate eligibility message
        And the user should be able to see the "Download" option
        And the user should be able to see the "Share" option

    Scenario: Assessment Details Validation

        Then the user should be able to see the "Assessments" section
        And the user should be able to see the assessment name
        And the user should be able to see the assessment score
        And the user should be able to see the assessment attempt date
        And the user should be able to see the assessment weightage
        And the user should be able to verify that the displayed assessment score is correct
        And the user should be able to verify that the assessment attempt date is displayed
        And the user should be able to verify that the assessment weightage is displayed correctly



    # ==================================================================
    # Negative scenarios

    @negative
    Scenario: An invalid job key is rejected on "Join a batch"
        Given the user is signed in to the WSN application
        When the user clicks on accounts menu
        And the user clicks on "join a batch"
        And the user enters the job code "INVALID-0000-XXXX"
        And the user clicks on "Enroll"
        Then the batch enrollment should be rejected

    @negative
    Scenario: An expired/already-used job key is rejected on "Join a batch"
        Given the user is signed in to the WSN application
        When the user clicks on accounts menu
        And the user clicks on "join a batch"
        And the user enters the job code "TEST-0000-0000"
        And the user clicks on "Enroll"
        Then the batch enrollment should be rejected

    @negative
    Scenario: "Join a batch" cannot be submitted without a job key
        Given the user is signed in to the WSN application
        When the user clicks on accounts menu
        And the user clicks on "join a batch"
        And the user leaves the job code field empty
        Then the "Enroll" button should be disabled

    @negative
    Scenario Outline: A new user cannot continue with an invalid email address
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters the email address "<email>"
        And the user submits the email address
        Then the email address should be rejected
        And the user should not reach the OTP screen

        Examples: Invalid email addresses
            | email                 |
            | newuser               |
            | newuser@              |
            | newuser@domain        |
            | @domain.com           |
            | newuser@@domain.com   |

        #     behave features/newuser.feature --tags=@negative --tags=~@known_defect
        @known_defect
        Examples: Invalid email addresses the app currently accepts
            | email                 |
            | newuser@domain..com   |

    @negative
    Scenario: A new user cannot continue with an empty email address
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user leaves the email address field empty
        Then the "Next" button should be disabled
        And the user should not reach the OTP screen

    @negative @manual
    Scenario Outline: A new user cannot verify an incorrect OTP
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP "<otp>"
        And the user submits the OTP
        Then the OTP should be rejected

        Examples: Incorrect OTPs
            | otp    |
            | 000000 |
            | 123456 |

    @negative @manual
    Scenario: A new user cannot register when the passwords do not match
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user enters the password "Demo@999" and the confirm password "Demo@111"
        Then the password should be rejected
        And the user should remain on the password step

    @negative @manual
    Scenario Outline: A new user cannot register with a password that fails the policy
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user enters the password "<password>" and the confirm password "<password>"
        Then the password should be rejected
        And the user should remain on the password step

        Examples: Passwords that break the policy
            | password |
            | demo     |
            | demo999  |
            | Demo999  |
 

    @negative @manual
    Scenario: A new user cannot submit the registration form without accepting the terms
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user completes the registration form without accepting the terms and conditions
        Then the registration form should not be submitted

    @negative @manual
    Scenario: A new user cannot submit the registration form without the first name
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user completes the registration form without entering the first name
        Then the registration form should not be submitted

    @negative @manual
    Scenario: A new user cannot submit the registration form without selecting a city
        Given the user opens the WSN application
        When the user clicks on "Continue with Email"
        And the user enters a valid email address manually
        And the user enters the OTP manually
        And the user completes the registration form without selecting the city
        Then the registration form should not be submitted
