Feature: showing off behave


  @old
  Scenario: run a simple test
    Given we have behave installed
      When we implement a test
      Then behave will test it for us

  @new
  Scenario: run a different simple test
    Given we have behave installed
      When we implement another test
      Then behave will test it for us
