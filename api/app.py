import pandas as pd
import json
import pickle
from fastapi import FastAPI

app = FastAPI(title="Servicio Segmentación de Usuarios")
data = pd.read_csv("data/usuarios_segmentados.csv")
modelo = pickle.load(open("models/modelo_kmeans.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

with open("models/metricas.json") as f:
    metricas = json.load(f)

@app.get("/")
def inicio():
    return {
        "mensaje":
        "Servicio ML funcionando"
    }

@app.get("/dashboard-data")
def dashboard_data():
    usuarios = pd.read_csv(
        "data/usuarios_segmentados.csv"
    )

    centroides = pd.read_csv("data/centroides.csv")

    return {
        "usuarios": usuarios.to_dict(orient="records"),
        "centroides": centroides.to_dict(orient="records"),
        "metricas": metricas
    }

@app.post("/predict")
def predict(datos:dict):
    data = pd.DataFrame([datos])
    X = scaler.transform(data)
    # Realiza la predicción (determinar el cluster)
    cluster = modelo.predict(X)

    return {"cluster": int(cluster[0])}