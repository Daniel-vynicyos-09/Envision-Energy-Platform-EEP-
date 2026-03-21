from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend import database
from backend import ia

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.criar_tabela()

class Dados(BaseModel):
    valor: float

@app.post("/dados")
def dados(d: Dados):
    database.inserir(d.valor)

    historico = database.listar()

    ia.treinar(historico)
    previsao = ia.prever(d.valor)
    dica = ia.dica(d.valor, previsao)

    return {
        "valor": d.valor,
        "previsao": previsao,
        "dica": dica
    }

@app.get("/historico")
def historico():
    return {"dados": database.listar()}