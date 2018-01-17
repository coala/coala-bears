Feature: Test for the no-unnamed-scenarios rule

Scenario:
  Given I have an unnamed Scenario
  Then I should see a no-unnamed-scenarios error
