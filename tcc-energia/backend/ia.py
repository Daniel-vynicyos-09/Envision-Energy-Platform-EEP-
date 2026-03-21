import numpy as np
import os
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, LSTM


MODEL_PATH = "backend/modelo_lstm.keras"

SEQ_LEN = 5  # quantidade de dados usados na sequência


def criar_modelo():
    model = Sequential([
        LSTM(16, activation='relu', input_shape=(SEQ_LEN, 1)),
        Dense(8, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    return model


def carregar_ou_criar():
    if os.path.exists(MODEL_PATH):
        try:
            model = load_model(MODEL_PATH, compile=False)
            model.compile(optimizer='adam', loss='mse')  # 🔥 ESSENCIAL
            return model
        except:
            print("Modelo corrompido, recriando...")

    model = criar_modelo()
    return model


def preparar_dados(dados):
    X, y = [], []

    for i in range(len(dados) - SEQ_LEN):
        X.append(dados[i:i+SEQ_LEN])
        y.append(dados[i+SEQ_LEN])

    return np.array(X), np.array(y)


def treinar(dados):
    if len(dados) <= SEQ_LEN:
        return

    model = carregar_ou_criar()

    X, y = preparar_dados(dados)

    X = X.reshape((X.shape[0], X.shape[1], 1))

    # 🔥 CORREÇÃO AQUI
    model.compile(optimizer='adam', loss='mse')

    model.fit(X, y, epochs=20, verbose=0)

    model.save(MODEL_PATH)


def prever(dados):
    if len(dados) < SEQ_LEN:
        return None

    model = carregar_ou_criar()

    entrada = np.array(dados[-SEQ_LEN:])
    entrada = entrada.reshape((1, SEQ_LEN, 1))

    previsao = model.predict(entrada, verbose=0)
    return float(previsao[0][0])
#chat ia
def dica(valor, previsao):
    if previsao is None:
        return "Coletando dados ainda..."

    if previsao > valor:
        return "Consumo pode subir ⚠️"
    elif previsao < valor:
        return "Consumo pode diminuir ✅"
    else:
        return "Consumo está estável"

def responder(pergunta, historico, previsao):
        pergunta = pergunta.lower()

        if "consumo" in pergunta:
            return f"O consumo atual é {historico[-1]:.1f}"

        elif "previs" in pergunta:
            if previsao:
                return f"A previsão é {previsao:.1f}"
            else:
                return "Ainda estou aprendendo"

        elif "alto" in pergunta:
            return "Consumo alto pode indicar muitos aparelhos ligados"

        elif "dica" in pergunta:
            return dica(historico[-1], previsao)

        else:
            return "Não entendi bem, mas estou aprendendo 😄"
#chat ia
def analisar_consumo(historico):
            if len(historico) < 5:
                return "Poucos dados para análise"

            media = sum(historico) / len(historico)
            ultimo = historico[-1]

            if ultimo > media:
                return "O consumo atual está acima da média"
            elif ultimo < media:
                return "O consumo está abaixo da média"
            else:
                return "O consumo está na média"
