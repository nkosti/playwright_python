class Locators:
    USERNAME_INPUT = "[data-cy='userName']"
    FIRST_NAME_INPUT = "[data-cy='firstName']"
    LAST_NAME_INPUT = "[data-cy='lastName']"
    EMAIL_INPUT = "[data-cy='email']"
    ORG_NAME_INPUT = "[data-cy='organizationName']"
    STATUS_DROPDOWN = "[data-cy='status']"
    STATUS_VALUE_OPTION = "[data-cy='status-{}']"
    RESET_BUTTON = "[data-cy='table-filter-reset-button']"
    CREATE_BUTTON = "[data-cy='user-create-user-modal-link']"
    NEW_USER_EMAIL_INPUT = "[data-cy='createUserModal-userName']"
    ADD_USER_BUTTON = "[data-cy='createUserModal-ok']"
    CELL_TEXT = 'tr:has-text("{}") [data-cy="{}"]:has-text("{}")'
    CELL_VALUE = 'tr:has-text("{}") [data-cy="{}"]'
    RESULTING_ROWS = ".ant-table-tbody tr"
    TOTAL_USER_COUNT = "li.ant-pagination-total-text"
