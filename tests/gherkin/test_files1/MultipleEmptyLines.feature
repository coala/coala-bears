Feature: Test for the no-multiple-empty-lines rule


Scenario: This is a Scenario for no-multiple-empty-lines
  Given I have a feature file with multiple empty lines
  Then I should see a no-multiple-empty-lines error
