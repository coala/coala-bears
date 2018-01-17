Feature: Test for the no-homogenous-tags

Background:
  Given I have a Feature file with homogenous tags

@homogenousTag
Scenario: This is a Scenario with some tags
  Then this is a then step

@homogenousTag
Scenario Outline: This is a Scenario with the same tags
  Then this is a then step

  Examples:
  | Example |
  | Another Example |
