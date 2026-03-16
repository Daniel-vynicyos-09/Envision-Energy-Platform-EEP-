from fastapi import FastAPI
from datetime import datetime
import pandas as pd
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(BASE_DIR, "dados")
ARQUIVO_DADOS = os.path.join(PASTA_DADOS, "consumo.csv")

os.makedirs(PASTA_DADOS, exist_ok=True)


@app.get("/")
def home():
    return {"status": "Servidor Energia AI Online"}


@app.post("/dados")
def receber_dados(dados: dict):

    sensor = dados["sensor"]
    consumo = dados["consumo"]

    registro = {
        "sensor": sensor,
        "consumo": consumo,
        "tempo": datetime.now()
    }

    df = pd.DataFrame([registro])

    df.to_csv(
        ARQUIVO_DADOS,
        mode="a",
        header=not os.path.exists(ARQUIVO_DADOS),
        index=False
    )

    return {"status": "dados recebidos"}


@app.get("/dados")
def ler_dados():

    if not os.path.exists(ARQUIVO_DADOS):
        return {"dados": []}

    df = pd.read_csv(ARQUIVO_DADOS)

    return df.to_dict(orient="list")