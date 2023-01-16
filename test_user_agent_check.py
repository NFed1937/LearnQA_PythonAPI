import json
import pytest
import requests


class TestUserAgentCheck:
    cases = [
        (r"Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
         '{"platform": "Mobile", "browser": "No", "device": "Android"}'),
        (r"Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
         '{"platform": "Mobile", "browser": "Chrome", "device": "iOS"}'),
        (r"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         '{"platform": "Googlebot", "browser": "Unknown", "device": "Unknown"}'),
        (r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
         '{"platform": "Web", "browser": "Chrome", "device": "No"}'),
        (r"Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
         '{"platform": "Mobile", "browser": "No", "device": "iPhone"}'),
        ("", '{"platform": "Unknown", "browser": "Unknown", "device": "Unknown"}')
    ]

    @pytest.mark.parametrize("user_agent, expected_values", cases)
    def test_user_agent_check(self, user_agent, expected_values):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

        # headers={"User-Agent": "Some value here"}
        header = {"User-Agent": user_agent}

        response = requests.get(url, headers=header)
        # print(f"response.text - {response.text}")

        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()
        expected_values_dict = json.loads(expected_values)

        # print(f"expected_values - {expected_values}")

        assert "device" in response_dict, "There is no field 'device' in the response"
        assert "browser" in response_dict, "There is no field 'browser' in the response"
        assert "platform" in response_dict, "There is no field 'platform' in the response"

        assert response_dict["device"] == expected_values_dict["device"], \
            f"Field 'device' is not correct. Expected '{expected_values_dict['device']}' but actual value '{response_dict['device']}'"
        assert response_dict["browser"] == expected_values_dict["browser"], \
            f"Field 'browser' is not correct. Expected '{expected_values_dict['browser']}' but actual value '{response_dict['browser']}'"
        assert response_dict["platform"] == expected_values_dict["platform"], \
            f"Field 'platform' is not correct. Expected '{expected_values_dict['platform']}' but actual value '{response_dict['platform']}'"


# python -m pytest -s test_user_agent_check.py -k "test_user_agent_check"
# python -m pytest -s test_user_agent_check.py
