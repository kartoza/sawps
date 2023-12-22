Feature: user

    User Form
    Scenario: User is created
        Given There is no user
        When I navigate to admin panel
        Then status code is 200
        Then I create user
        Then user should be present
