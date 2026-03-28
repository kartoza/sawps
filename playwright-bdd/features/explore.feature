Feature: Explore

    Explore page
    Scenario: Explore
        Given I am on the landing page "http://localhost:61100/"
        When I click on "Explore"
        Then I should be redirected to "http://localhost:61100/map" view
        Then I should see the map canvas