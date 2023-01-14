import requests


class TestHomeworkCookie:
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)

        # print(f"Текст ответа '{response.text}'")
        # print(f"Куки ответа '{response.cookies}'")

        expected_cookie = "HomeWork"
        expected_cookie_value = "hw_value"

        assert response.status_code == 200, "Wrong response code"

        assert expected_cookie in response.cookies, f"There is no cookie '{expected_cookie}' in the response"

        actual_cookie_value = response.cookies.get(expected_cookie)
        # print(f"actual_cookie_value = '{actual_cookie_value}'")

        assert actual_cookie_value == expected_cookie_value,\
            f"Actual value '{actual_cookie_value}' of cookie '{expected_cookie}' is not correct"

# python -m pytest -s test_homework_cookie.py -k "test_homework_cookie"
# Текст ответа ''
# Куки ответа  '<RequestsCookieJar[<Cookie HomeWork=hw_value for .playground.learnqa.ru/>]>'
