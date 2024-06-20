Feature: SAWPS login page

    Scenario: Check title
        Given I open url "http://localhost:61100/"
        When I click link "LOGIN"
        Then I see in title "SAWPS - Login"
        Then I fill in login details: "admin@example.com" and "admin"
        Then I can proceed to "LOGIN"
        Then I assert if "Explore" and "Upload your data" is visible