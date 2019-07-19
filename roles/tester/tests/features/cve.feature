Feature: Perform exploit from <cve>
  Environment should not be affectable by <cve> exploit

  Scenario Outline: Victim node should pass all checks after performing exploit
    Given prepared <abuser> node
    And prepared <victim> node
    When exploit is finished
    Then all checks against <victim> are passed
