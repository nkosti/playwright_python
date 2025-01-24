class Locators:
    CLOSE_MESSAGE_POPUP_BUTTON = ".ant-notification-notice-close"
    CLOSE_NOTIFICATION_WITH_TEXT = '.ant-notification-notice-content:has-text("{}") + a.ant-notification-notice-close'
    SUCCESSFUL_NOTIFICATION = '[data-cy="toast-item-severity-success"]'
    SPINNER_ELEMENT = ".ant-spin >> nth=0"
    TOAST_MESSAGE = '[data-cy="toast-item-message"], [data-cy="toast-item-notification"]'
    TOAST_MESSAGE_WITH_TEXT = '[data-cy="toast-item-message"]:has-text("{0}"), [data-cy="toast-item-notification"]:has-text("{0}")'
