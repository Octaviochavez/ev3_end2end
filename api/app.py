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
    """
    inicio(): Es un endpoint GET en / que responde con un JSON simple
    {"mensaje": "Servicio ML funcionando"}. Es una comprobación de que el servicio está activo
    Returns:
        mensaje: Comprobación del funcionamiento del servicio.
    """    
    return {
        "mensaje":
        "Servicio ML funcionando"
    }

@app.get("/dashboard-data")
def dashboard_data():
    """
    dashboard_data(): Es un endpoint GET en /dashboard-data que carga: 
    - usuarios_segmentados.csv como usuarios
    - carga centroides.csv como centroides
    * Es la funcion que expone los datos necesarios para el dashboard
    Returns:
        - usuarios como lista de registros.
        - Centroides como lista de registros.
        - metricas ya cargadas en memoria.
    """    
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
    """
    predict(): Es un endpoint POST en /predict que recibe un JSON con los datos del usuario, convierte
    esa entrada en DataFrame, normaliza las caracteristicas con scaler.transform() y luego usa modelo.predict()
    para asignar un cluster
    - Args:
        datos (dict):
        Un diccionario con las características del usuario que se usan para crear el dataframe
        de entrada antes de escalar y predecir el cluster.

    Returns:
        {"cluster": int(cluster[0])}: Devuelve el resultado como JSON.
    """    
    data = pd.DataFrame([datos])
    X = scaler.transform(data)
    # Realiza la predicción (determinar el cluster)
    cluster = modelo.predict(X)

    return {"cluster": int(cluster[0])}