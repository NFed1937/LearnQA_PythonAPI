import requests


class TestHomeworkHeader:
    def test_homework_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        # print(f"Текст ответа '{response.text}'")
        # print(f"Куки ответа '{response.cookies}'")
        # print(f"Заголовки ответа '{response.headers}'")

        expected_header = "x-secret-homework-header"
        expected_header_value = "Some secret value"

        assert response.status_code == 200, "Wrong response code"

        assert expected_header in response.headers, f"There is no header '{expected_header}' in the response"

        actual_header_value = response.headers.get(expected_header)
        # print(f"actual_header_value = '{actual_header_value}'")

        assert actual_header_value == expected_header_value,\
            f"Actual value '{actual_header_value}' of header '{expected_header}' is not correct"

# python -m pytest -s test_homework_header.py -k "test_homework_header"

# Текст ответа '{"success":"!"}'
# Куки ответа '<RequestsCookieJar[]>'
# Заголовки ответа '{'Date': 'Sat, 14 Jan 2023 18:23:05 GMT', 'Content-Type': 'application/json',
# 'Content-Length': '15', 'Connection': 'keep-alive', 'Keep-Alive': 'timeout=10', 'Server': 'Apache',
# 'x-secret-homework-header': 'Some secret value', 'Cache-Control': 'max-age=0',
# 'Expires': 'Sat, 14 Jan 2023 18:23:05 GMT'}'

# 'x-secret-homework-header': 'Some secret value'

