import requests

#  1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"1. При запросе без параметра выводится текст: '{response.text}'")  # Wrong method provided
print()

#  2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print(f"2. При запросе не из списка (для HEAD) выводится текст: '{response.text}'")  # Пустая строка
print()

#  3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
# Запрашивать его можно четырьмя разными HTTP-методами: POST, GET, PUT, DELETE
payload = {"method": "POST"}
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
print(f"3.1 Для метода POST выводится текст: '{response.text}'")

payload = {"method": "GET"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
print(f"3.2 Для метода GET выводится текст: '{response.text}'")

payload = {"method": "PUT"}
response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
print(f"3.3 Для метода PUT выводится текст: '{response.text}'")

payload = {"method": "DELETE"}
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
print(f"3.4 Для метода DELETE выводится текст: '{response.text}'")
print()

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса.
# Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, но сервер отвечает так,
# словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

reqParams = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE', 'CONNECT', 'OPTIONS']
print(f"4 Для всех теоретически возможных типов запроса: {reqParams}")

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"
s = '{"method": "METHOD"}'


def checkresponse(a, b, c, d):
    print(f"  4.{d}.{i + 1} Для сочетания {reqType}-{reqParams[i]} выводится текст: '{response.text}'")
    if a == b:
        if 'Wrong' in c:
            print("----------------------------------------------------------------------------ERROR1")
        else:
            print("  OK")
    else:
        if 'success' in c:
            print("----------------------------------------------------------------------------ERROR2")
        else:
            print("  OK")


reqType = "GET"
j = 1
print(f"{reqType}")
for i in range(9):
    payload = s.replace("METHOD", reqParams[i])
    # print(payload)
    response = requests.get(URL, params=payload)
    checkresponse(reqType, reqParams[i], response.text, j)
print()

reqType = "POST"
j = 2
print(f"{reqType}")
for i in range(9):
    payload = s.replace("METHOD", reqParams[i])
    response = requests.post(URL, data=payload)
    checkresponse(reqType, reqParams[i], response.text, j)
print()

reqType = "PUT"
j = 3
print(f"{reqType}")
for i in range(9):
    payload = s.replace("METHOD", reqParams[i])
    response = requests.put(URL, data=payload)
    checkresponse(reqType, reqParams[i], response.text, j)
print()

reqType = "DELETE"
j = 4
print(f"{reqType}")
for i in range(9):
    payload = s.replace("METHOD", reqParams[i])
    response = requests.delete(URL, data=payload)
    checkresponse(reqType, reqParams[i], response.text, j)
print()

reqType = "HEAD"
j = 5
print(f"{reqType}")
for i in range(9):
    payload = s.replace("METHOD", reqParams[i])
    response = requests.head(URL, data=payload)
    checkresponse(reqType, reqParams[i], response.text, j)
print()

reqType = "PATCH"
j = 6
print(f"{reqType}")
for i in range(9):
    payload = s.replace("METHOD", reqParams[i])
    response = requests.patch(URL, data=payload)
    checkresponse(reqType, reqParams[i], response.text, j)
print()

# AttributeError: module 'requests' has no attribute 'trace'
# reqType = "TRACE"
# j = 7
# print(f"{reqType}")
# for i in range(9):
#     payload = s.replace("METHOD", reqParams[i])
#     response = requests.trace(URL, data=payload)
#     checkresponse(reqType, reqParams[i], response.text, j)
# print()

# AttributeError: module 'requests' has no attribute 'connect'
# reqType = "CONNECT"
# j = 8
# print(f"{reqType}")
# for i in range(9):
#     payload = s.replace("METHOD", reqParams[i])
#     response = requests.connect(URL, data=payload)
#     checkresponse(reqType, reqParams[i], response.text, j)
# print()

reqType = "OPTIONS"
j = 9
print(f"{reqType}")
for i in range(9):
    payload = s.replace("METHOD", reqParams[i])
    response = requests.options(URL, data=payload)
    checkresponse(reqType, reqParams[i], response.text, j)
print()
