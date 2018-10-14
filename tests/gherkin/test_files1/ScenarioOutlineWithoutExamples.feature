Feature: Test for no-scenario-outlines-without-examples rule

Scenario Outline: Scenario Outline without examples
  Given we use foo
  And the scenario outline has no examples
  Then I should see a no-scenario-outlines-without-examples error

Scenario: Scenario without examples
  Given we use bar
  And the scenario has no examples
  Then I should see no no-scenario-outlines-without-examples error
