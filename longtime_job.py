import requests
import json
import time

#  Токены
URL = "https://playground.learnqa.ru/ajax/api/longtime_job"
#  1) создаем задачу
response = requests.get(URL)
#  разбираем ответ сервера
json_text = response.text
obj = json.loads(json_text)
if response.status_code == 200:
    s = obj['seconds']
    print(f"Ожидание {obj['seconds']} сек.")
    t = obj['token']
    print(f"Токен - {obj['token']}")

    #  2) делаем один запрос с token ДО того, как задача готова
    payload = {"token": t}
    response1 = requests.get(URL, params=payload)
    #  разбираем ответ сервера
    json_text1 = response1.text
    obj1 = json.loads(json_text1)
    #  убеждаемся в правильности поля status
    #  если задача еще не готова, будет надпись Job is NOT ready, если же готова - будет надпись Job is ready
    if obj1['status'] == "Job is NOT ready":
        print(obj1['status'])
        print("Ждите ... ")
        #  3) ждем нужное количество секунд
        time.sleep(s)
        #  4) делаем еще один запрос c token ПОСЛЕ того, как задача готова
        response2 = requests.get(URL, params=payload)
        #  разбираем ответ сервера
        json_text2 = response2.text
        obj2 = json.loads(json_text2)
        # убеждаемсяся в правильности поля status и наличии поля result
        if obj2['status'] == "Job is ready":
            print(f"status = {obj2['status']}")
            print(f"result = {obj2['result']}")
        else:
            print("Что-то пошло не так ...")
            print(f"response2.status_code = {response2.status_code}")
            print(f"Отверт сервера - {response2.text}")
    else:
        print("Что-то пошло не так ...")
        print(f"response1.status_code = {response1.status_code}")
        print(f"Отверт сервера - {response1.text}")
else:
    print("Что-то пошло не так ...")
    print(f"response.status_code = {response.status_code}")
    print(f"Отверт сервера - {response.text}")
