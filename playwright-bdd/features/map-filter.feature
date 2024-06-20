Feature: Map filter

    Map filter
    Scenario: Map filter
        Given I am on the project landing page "http://localhost:61100/"
        When I click on "Explore" button
        Then I should be redirected to the "**/map" view
        Then I should see the map canvas on the page
        When I configure filters
        Then I should see data on the map and legend should be visible