Feature: Test for the no-tags-on-backgrounds

@tag
Background:
  Given I have a Feature file with a tag on a background

Scenario: This is a Scenario for no-tags-on-backgrounds
  Then I should see a no-tags-on-backgrounds
