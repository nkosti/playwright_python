from enum import Enum

from test.domains.enum.base.base_enum import BaseEnum


class UserFiltersCell(Enum):
    USERNAME = 'cell-userName'
    FIRST_NAME = 'cell-firstName'
    LAST_NAME = 'cell-lastName'
    EMAIL = 'cell-email'
    ORGANIZATION_NAME = 'cell-organizationName'
    STATUS = 'cell-status'


class UsersCSVFilters(BaseEnum):
    USERNAME = ('Username', 'username')
    FIRST_NAME = ('First name', 'first_name')
    LAST_NAME = ('Last name', 'last_name')
    EMAIL = ('E-mail', 'email')
    ORGANIZATION_NAME = ('Organization name', 'organization_name')
    STATUS = ('Status', 'status')

    @property
    def csv_name(self):
        return self.value[0]

    @property
    def filter_name(self):
        return self.value[1]
