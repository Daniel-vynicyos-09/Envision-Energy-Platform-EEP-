import requests
import random
import time

while True:

    dados = {
        "sensor": "sala",
        "consumo": random.randint(200,700)
    }

    r = requests.post(
        "http://127.0.0.1:8000/dados",
        json=dados
    )

    print("Enviado:", dados)

    time.sleep(5)