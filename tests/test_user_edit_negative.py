from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEditNegative(BaseCase):
    def setup_method(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.new_email = register_data['email']
        self.new_first_name = register_data['firstName']
        self.new_password = register_data['password']
        self.new_user_id = self.get_json_value(response1, "id")

    # - Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_not_auth(self):
        # EDIT
        new_name = "Changed Name"

        response1 = MyRequests.put(
            f"/user/{self.new_user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response1, 400)
        Assertions.assert_response_content(response1, "Auth token not supplied")

    # - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_auth_as_another_user(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        # print(f"new_user_id - '{self.new_user_id}'")

        response2 = MyRequests.put(
            f"/user/{self.new_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_content(response2, "Please, do not edit test users with ID 1, 2, 3, 4 or 5.")

    # - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем,
    # на новый email без символа @
    def test_edit_user_auth_bad_email(self):
        # LOGIN
        login_data = {
            'email': self.new_email,
            'password': self.new_password
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        bad_email = "Changed_Email___example.com"

        response2 = MyRequests.put(
            f"/user/{self.new_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": bad_email}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_content(response2, "Invalid email format")

    # - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    def test_edit_user_auth_too_short_name(self):
        # LOGIN
        login_data = {
            'email': self.new_email,
            'password': self.new_password
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        new_name = "a"
        # new_name = "0123456789"*30

        response2 = MyRequests.put(
            f"/user/{self.new_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 400)

        expected_error = "Too short value for field firstName"
        # expected_error = "Too long value for field firstName"

        Assertions.assert_json_value_by_name(
            response2,
            "error",
            expected_error,
            "Unexpected error text!"
        )

# python -m pytest -s tests/test_user_edit_negative.py
# python -m pytest -s tests/test_user_edit_negative.py -k test_edit_user_not_auth
# python -m pytest -s tests/test_user_edit_negative.py -k test_edit_user_auth_as_another_user
# python -m pytest -s tests/test_user_edit_negative.py -k test_edit_user_auth_bad_email
# python -m pytest -s tests/test_user_edit_negative.py -k test_edit_user_auth_too_short_name