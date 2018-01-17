@watch
Feature: A feature with disallowed tag

@important @wip
Scenario: A scenario with disallowed tag
  Then I should see a no-watch tag error

@todo
Scenario: A scenario with allowed tags
  Then I should see a no-watch tag error
