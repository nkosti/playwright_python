from playwright.sync_api import expect
from pytest_bdd import step, parsers
from test.domains.test_data.dto.users.users_dto import UserDTO

from test.conftest import Context
from test.domains.enum.users.users import UserFiltersCell
from test.features.conftest import navigate_to_users_page


@step(parsers.parse('"{User}" creates a new active User'))
def create_new_active_user(poms: Context, user_dto: UserDTO):
    poms.users.create_user.create_new_user(user_dto.email)
    user = poms.users.create_user
    user.fill_user_info(
        first_name=user_dto.first_name,
        last_name=user_dto.last_name,
        email=user_dto.email,
        phone=user_dto.phone_no,
        notam_office=user_dto.notam_office,
    )
    user.set_organization(user_dto.org_name)
    user.set_user_roles(user_dto.roles)
    user.save_user_settings()


@step(parsers.parse("the new User is displayed on User list as {status_value}"))
def user_displayed_with_status(poms, user_dto: UserDTO, json_data):
    navigate_to_users_page(poms)
    user = poms.users.find_user
    user.search_user_by(username=user_dto.email)
    expect(
        poms.users.find_user.get_cell_element(
            user_dto.email,
            UserFiltersCell.STATUS,
            json_data.get("Expected").get("expected_status"),
        )
    ).to_be_visible()
