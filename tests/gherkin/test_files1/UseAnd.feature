Feature: Test for the use-and rule

Background:
  Given first statement
  And second statement with and
  Given third statement that does not use and

Scenario: A scenario for use-and rule
  Given first given within scenario, which is fine
  When first step
  When second step without and
  And third step with and
  Then first assertion
  Then second assertion without and
