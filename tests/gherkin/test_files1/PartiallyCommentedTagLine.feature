Feature: Test for the no-partially-commented-tag-lines

Background:
  Given I have a Feature file with a line with tags that is half commented out

@tag #@commented-out-tag
Scenario: This is a Scenario for no-partially-commented-tag-lines
  Then I should see a no-partially-commented-tag-lines error
