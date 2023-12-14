Feature: SAWPS

    Scenario: Check title
        Given I am at "http://localhost:61100/"
        Then The title is "SAWPS"
        Then I check if "Explore" and "Upload your data" are both visible
