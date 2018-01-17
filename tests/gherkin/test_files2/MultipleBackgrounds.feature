Feature: Test for the up-to-one-background-per-file rule

Background:
  Given I have a Feature file with 2 backgrounds

Scenario: This is Scenario 1 for up-to-one-background-per-file
  Then I should see a up-to-one-background-per-file error

Background:
  Given my second Background existsSync

Scenario: This is Scenario 2 for up-to-one-background-per-file
  Then I should see a up-to-one-background-per-file error
