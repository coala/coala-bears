Feature: Test for the new-line-at-eof rule

Scenario: This is a Scenario for new-line-at-eof
  Given I don't have a new line at the end of this file
  Then I should see a new-line-at-eof error