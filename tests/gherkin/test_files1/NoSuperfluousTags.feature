@superfluousTag
Feature: Test for the no-superfluous-tags

Background:
  Given I have a Feature file with superfluous tags

@superfluousTag
Scenario: This is a Scenario with the same tag as a feature
  Then I should see a no-superfluous-tags
