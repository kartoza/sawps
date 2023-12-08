Feature: testing website navigation

        Scenario: landingpage
            Given the user is on the landingpage
             Then page is landingpage

        Scenario: logging into the application
            Given user is on 'landingpage'
             When user clicks on 'Log in'
             Then page is 'landingpage with explore and upload data button visible'

        Scenario: accessing map page
            Given user is on the landingpage
             When user clicks on 'Explore' link
             Then the page is the'map' page