import copy

from test.domains.test_data.dto.base_dto import BaseDTO
from test.utils.utilities import Utilities


class UserDTO(BaseDTO):
    def __init__(self, json_data):
        self.json_data: dict = json_data
        self.username: str = Utilities.generate_email()
        self.first_name: str = json_data.get("first_name") or Utilities.get_random_text("", 10)
        self.last_name: str = json_data.get("last_name") or Utilities.get_random_text("", 10)
        self.email: str = self.username
        self.org_name: str = json_data.get("org_name") or Utilities.get_random_text("", 10)
        self.phone_no: str = json_data.get("phone_no")
        self.roles: dict = json_data.get("roles", {})
        self.status: str = json_data.get("status")
        self.original_dto = copy.deepcopy(vars(self))
        super().__init__(update_dict=json_data.get("Update"))
