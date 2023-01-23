from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    # Первый - на попытку удалить пользователя по ID 2
    def test_delete_user_2(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_content(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    # Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить
    # его данные по ID и убедиться, что пользователь действительно удален.
    def test_delete_user_auth_as_same_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        new_email = register_data['email']
        new_password = register_data['password']
        new_user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': new_email,
            'password': new_password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{new_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
            )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_response_content(response3, "")

        # GET
        response4 = MyRequests.get(
            f"/user/{new_user_id}"
        )

        Assertions.assert_code_status(response4, 404)
        Assertions.assert_response_content(response4, "User not found")

    # Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_user_auth_as_another_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        new_email = register_data['email']
        new_password = register_data['password']
        new_user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{new_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
            )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_content(response3, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

        # GET
        response4 = MyRequests.get(
            f"/user/{new_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 200)
        Assertions.assert_response_content(response4, '{"username":"learnqa"}')

# python -m pytest -s tests/test_user_delete.py
# python -m pytest -s tests/test_user_delete.py -k test_delete_user_2
# python -m pytest -s tests/test_user_delete.py -k test_delete_user_auth_as_same_user
# python -m pytest -s tests/test_user_delete.py -k test_delete_user_auth_as_another_user
