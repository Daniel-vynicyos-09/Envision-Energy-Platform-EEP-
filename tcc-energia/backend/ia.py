import numpy as np
import os
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense

MODEL_PATH = "backend/modelo.h5"

def criar_modelo():
    model = Sequential([
        Dense(8, activation='relu', input_shape=(1,)),
        Dense(8, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def carregar_ou_criar():
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH, compile=False)

        # 🔥 recompila o modelo
        model.compile(optimizer='adam', loss='mean_squared_error')

        return model

    return criar_modelo()

def treinar(dados):
    if len(dados) < 5:
        return None

    X, y = [], []

    for i in range(len(dados)-1):
        X.append([dados[i]])
        y.append(dados[i+1])

    X = np.array(X)
    y = np.array(y)

    model = carregar_ou_criar()
    model.fit(X, y, epochs=50, verbose=0)

    model.save(MODEL_PATH)
    return model

def prever(valor):
    if not os.path.exists(MODEL_PATH):
        return None

    model = load_model(MODEL_PATH)
    pred = model.predict(np.array([[valor]]), verbose=0)

    return float(pred[0][0])

def dica(valor, previsao):
    if previsao is None:
        return "Coletando dados ainda..."

    if previsao > valor * 1.2:
        return "⚠️ Pico de consumo previsto! Evite usar vários aparelhos juntos."
    elif previsao > valor:
        return "Consumo pode subir um pouco."
    else:
        return "Consumo está controlado 👍"