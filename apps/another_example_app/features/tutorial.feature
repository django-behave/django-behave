Feature: showing off nested app testing with behave


  Scenario: run a simple test in a nested app
    Given we have a nested app
      When behave tries to test it
      Then it succeeds
        And does not print 'skipping label with dot'

