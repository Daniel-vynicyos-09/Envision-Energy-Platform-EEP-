from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend import database
from backend import ia

app = FastAPI()
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")

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
    previsao = ia.prever(historico)
    dica = ia.dica(d.valor, previsao)

    return {
        "valor": d.valor,
        "previsao": previsao,
        "dica": dica
    }

@app.get("/historico")
def historico():
    return {"dados": database.listar()}
class Pergunta(BaseModel):
    texto: str

@app.post("/chat")
def chat(p: Pergunta):
    historico = database.listar()

    previsao = ia.prever(historico)

    resposta = ia.responder(p.texto, historico, previsao)

    return {"resposta": resposta}

@app.get("/analise")
def analise():
    historico = database.listar()
    texto = ia.analisar_consumo(historico)
    return {"analise": texto}