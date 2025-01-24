@UOM
Feature: User Management

  @TEST-1
  Scenario: [TEST-1] Creation of a new User - User not found in CIAM
    Given "User Admin" navigated to Users page
    When  "User Admin" creates a new active User
    Then  confirmation message is displayed
    And   the new User is displayed on User list as "ACTIVE"
