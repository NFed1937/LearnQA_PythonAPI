import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    exclude_fields = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

    # Создание пользователя с некорректным email - без символа @
    def test_create_user_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"Invalid email format")

    # Создание пользователя без указания одного из полей - с помощью @parametrize
    # необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
    @pytest.mark.parametrize('field_name', exclude_fields)
    def test_create_user_negative(self, field_name):
        data = self.prepare_registration_data()

        data[field_name] = None

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"The following required params are missed: {field_name}")

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_too_short_name(self):
        firstname = 'a'
        data = self.prepare_registration_data()
        data['firstName'] = firstname

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, r"The value of 'firstName' field is too short")

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_too_long_name(self):
        firstname = '1234567890'*30
        data = self.prepare_registration_data()
        data['firstName'] = firstname

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, r"The value of 'firstName' field is too long")

        # print(response.status_code)
        # print(response.content)

        # expected_error = "Too short value for field firstName"
        # expected_error = "Too long value for field firstName"

# python -m pytest -s tests/test_user_register.py
# python -m pytest -s tests/test_user_register.py -k test_create_user_successfully
# python -m pytest -s tests/test_user_register.py -k test_create_user_negative
# python -m pytest -s tests/test_user_register.py -k test_create_user_incorrect_email
# python -m pytest -s tests/test_user_register.py -k test_create_user_too_short_name
# python -m pytest -s tests/test_user_register.py -k test_create_user_too_long_name
