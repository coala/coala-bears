Feature: Test for no-files-without-scenarios rule - Only Scenario Outline

Scenario Outline: Scenario Outline only
  Given we use "<foo>"
  And the feature has only scenario outlines
  Then I should see no no-files-without-scenarios error

  Examples:
  | foo |
  | bar |
