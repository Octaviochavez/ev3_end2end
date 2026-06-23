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
print(usuarios.head())