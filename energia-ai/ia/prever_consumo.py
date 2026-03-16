import pandas as pd
from sklearn.linear_model import LinearRegression
import os

caminho = os.path.join(os.path.dirname(__file__), "..", "dados", "consumo.csv")

df = pd.read_csv(caminho)

df["tempo"] = pd.to_datetime(df["tempo"])
df["tempo_num"] = df["tempo"].astype("int64") // 10**9

X = df[["tempo_num"]]
y = df["consumo"]

modelo = LinearRegression()
modelo.fit(X, y)

proximo_tempo = [[X.iloc[-1]["tempo_num"] + 60]]

previsao = modelo.predict(proximo_tempo)

print("Previsão de consumo:", previsao[0])