Feature: Test for the no-dupe-feature-names rule

Scenario: This is Scenario 1 for no-dupe-feature-names
  Given I have 2 feature files with the same name
  Then I should see a no-dupe-feature-names error

Scenario: This is Scenario 2 for no-dupe-feature-names
  Given I have 2 feature files with the same name
  Then I should see a no-dupe-feature-names error
