Feature: Test for the no-files-without-scenarios rule

Background:
  Given I have a Feature file with no scenarios
  Then I should see a no-files-without-scenarios error
