import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
import json

from sqlalchemy import create_engine
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from kneed import KneeLocator

os.makedirs("models", exist_ok=True)

usuarios = pd.read_csv("data/usuarios_streaming.csv")
perfiles = pd.read_csv("data/perfil_usuarios.csv")

data = pd.merge(usuarios, perfiles, on="id_cliente")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(data.drop(columns=["id_cliente"]))

inertias = []
silhouettes = []
for k in range(2,11):
    modelo = KMeans(n_clusters=k, random_state=29, n_init=10)
    modelo.fit(X_scaled)

    inertias.append(modelo.inertia_)
    silhouettes.append(silhouette_score(X_scaled, modelo.labels_))

kl = KneeLocator(
    range(2,11),
    inertias,
    curve='convex',
    direction='decreasing'
)

k_optimo = kl.elbow
kmeans = KMeans(n_clusters=k_optimo, random_state=29, n_init=10)

clusters = kmeans.fit_predict(X_scaled)
data["cluster"] = clusters

print("Modelo de segmentación creado con éxito. Número óptimo de clusters:", k_optimo)

pca = PCA(n_components=2)
componentes = pca.fit_transform(X_scaled)
data["pc1"] = componentes[:, 0]
data["pc2"] = componentes[:, 1]

data.to_csv("data/clientes_segmentados.csv", index=False)

metricas = {
    "k_optimo": int(k_optimo),
    "silhouette_score": silhouette_score(X_scaled, data["cluster"]),
    "n_clientes": int(len(data)),
    "n_clusters": int(k_optimo),
    "varianza_pca": float(
        pca.explained_variance_ratio_.sum()
    )
}

with open("models/metricas.json", "w") as f:
    json.dump(metricas, f, indent=4)

centroides_original = scaler.inverse_transform(kmeans.cluster_centers_)
centroides_df = pd.DataFrame(
    centroides_original,
    columns=data.columns.drop(["id_cliente", "cluster", "pc1", "pc2"])
)
centroides_df.to_csv("data/centroides.csv", index=False)

pickle.dump(kmeans, open("models/modelo_kmeans.pkl", "wb"))
pickle.dump(scaler, open("models/scaler.pkl", "wb"))
pickle.dump(pca, open("models/pca.pkl", "wb"))
print("Modelo guardado")