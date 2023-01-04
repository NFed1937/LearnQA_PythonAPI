import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

i = 0 # Количество редиректов
while i >= 0:
    try:
        if 300 <= response.history[i].status_code <= 399:
            i += 1
    except IndexError:
        break

print(f"Количество редиректов: {i}")
print(f"Конечный URL: {response.url}")



