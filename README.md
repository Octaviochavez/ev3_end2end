# Segmentación de clientes con Machine Learning

## Evaluación N°3 Programación para la Ciencia de Datos: Construir una solución End-to-end.

**Integrantes:**

- Octavio Chávez
- David Ramirez
- Felipe Huincaman

**Asignatura:**

- Programación para la Ciencia de Datos

**Docente:**

- Jazna Meza Hidalgo

**Fecha:**

- 30-06-2026

### Descripción del proyecto:

Este proyecto implementa una solución completa de segmentación de clientes utilizando técnicas de aprendizaje no supervisado

**Objetivo** : Integrar dos fuentes de datos, construir un conjunto analítico consolidado y desarrollar un modelo de segmentación utilizando el algoritmo KMeans que permita identificar perfiles diferenciados de usuarios.

La solución incorpora:

- Una fuente de datos en formato CSV.
- Una segunda fuente de datos almacenada en una base de datos PostgreSQL.
- Un pipeline de integración de datos.
- Entrenamiento de un modelo de clustering.
- Exposición del modelo mediante un API REST.
- Dashboard interactivo para análisis de resultados.
- Contenerización completa utilizando Docker.

## Arquitectura de la solución:

                  CSV Clientes
                        |
                        |
                        v

                +----------------+
                |  Integración   |
                |   de datos     |
                +----------------+
                        |
                        |
            +---------------------------+
            |                           |
            v                           v

    +-------------------+    +-----------------+
    |PostgreSQL CRM     |    |Dataset integrado|
    |perfil_usuarios.csv|    |data_usuarios.csv|
    +-------------------|    +-----------------+
                           |
                           |
                           v

                    +----------------+
                    |    KMeans      |
                    |  Segmentación  |
                    +----------------+

                            |
                +-----------+-----------+
                |                       |
                v                       v
            FastAPI                Streamlit
            Servicio               ML Dashboard

## Tecnologías utilizadas:

### Lenguaje

- Python 3.12.10

### Machine Learning:

- Scikit-Learn
- KMeans
- StandardScaler
- Silhouette Score
- Método del codo mediante KneeLocator

### Datos

- Pandas
- PostgreSQL
- SQLAlchemy

### Backend

- FastAPI
- Uvicorn

### Visualización

- Streamlit

### Infraestructura

- Docker
- Docker Compose

## Estructura del proyecto:

    ev3_programacion
    |
    |-docker/
    |
    |-docs/
    |
    |-etl/
    |
    |--data/
    |   |
    |   |-usuarios_streaming.csv
    |   |-data_usuarios.csv
    |   |-usuarios_segmentados.csv
    |   |-centroides.csv
    |
    |--database/
    |   |
    |   |-perfil_usuarios.csv
    |   |-init.sql
    |
    |
    |--dashboards/
    |   |
    |   |-Dockerfile
    |   |-app.py
    |   |-requirements.txt
    |
    |--api/
    |   |
    |   |-train.py
    |   |-Dockerfile
    |   |-requirements.txt
    |   |-app.py
    |
    |--tests/
    |
    |--repo/
    |    |
    |    |-git_branches.png
    |    |-commits.png
    |    |-git_summary.png
    |
    |-.env
    |-docker-compose.yml
    |-analisis_exploratorio.ipynb
    |-README.MD

## Fuentes de datos

## Fuente 1: Información de consumo dentro de la plataforma

Archivo:

`usuarios_streaming.csv`

Esta fuente contiene información relacionada con los hábitos de consumo de los usuarios dentro de la plataforma.

Incluye variables como:

- horas de consumo mensual
- gasto mensual asociado al servicio
- cantidad de contenidos vistos
- cantidad de sesiones semanales
- porcentaje de contenidos finalizados
- duración promedio de sesión
- cantidad de géneros consumidos
- porcentaje de uso de promociones
- antigüedad del usuario

## Fuente 2: Información complementaria del usuario

Archivo:

`perfil_usuarios.csv`

Esta fuente contiene información obtenida desde el sistema de perfiles y atención al usuario.

El contenido de este archivo debe ser cargado en una tabla en una base de datos en Postgres.

Base de datos:
`analisis streaming`

Tabla:
`perfil_usuarios`

Incluye variables como:

- edad del usuario
- cantidad de dispositivos registrados
- porcentaje de uso desde aplicación móvil
- cantidad de perfiles creados
- cantidad de interacciones con soporte
- distancia promedio asociada a la red de conexión

## Pipeline de Machine Learning

El proceso ejecutado por train.py realiza:

1. Lectura del archivo CSV.

2. Conexión a PostgreSQL.

3. Extracción de información desde la tabla:

   `perfil_usuarios`

4. Integración mediante:

   `id_cliente`

5. Generación del dataset analítico:

   `data_usuarios.csv`

6. Normalización de variables utilizando:

   `StandardScaler`

7. Evaluación de diferentes cantidades de clusters.

8. Selección del número óptimo de segmentos.

9. Entrenamiento del modelo KMeans.

10. Persistencia del modelo:

    `modelo_kmeans.pkl`

11. y del escalador:

    `scaler.pkl`

## Ejecución del proyecto

### Requisitos

Tener instalado:

- Docker
- Docker Compose

## Levantar la solución

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Este comando levantará tres servicios:

| Servicio      |    Tecnología    | Puerto | Descripción                           |
| :------------ | :--------------: | :----: | :------------------------------------ |
| Base de datos |  PostgreSQL 16   | `5432` | Almacenamiento relacional de perfiles |
| API Backend   | FastAPI / Python | `8000` | Procesamiento ETL y modelo KMeans     |
| Frontend      |    Streamlit     | `8501` | Dashboard interactivo para el negocio |

## Acceso a los servicios

### API Machine Learning:

Abrir:
`http://localhost:8000`

Respuesta esperada:
`{
    "mensaje": "Servicio ML funcionando"
`}

### Dashboard

Abrir:
`http://localhost:8501`

El dashboard permite:

- Métricas del modelo.
- Visualizar los clientes segmentados.
- Visualizar distribución de segmentos.
- Analizar el perfil de cada grupo.

## Endpoint de predicción

Servicio:

`POST /predict`

Ejemplo de entrada:

```json
{
  "horas_consumo_mensual": 49,
  "gasto_mensual": 76,
  "cantidad_contenidos_vistos": 3,
  "sesiones_semana": 6,
  "porcentaje_finalizacion": 49,
  "tiempo_promedio_sesion_min": 56,
  "cantidad_generos_consumidos": 4,
  "porcentaje_uso_promociones": 0.7855,
  "antiguedad_cliente_meses": 28,
  "edad": 52,
  "dispositivos_registrados": 2,
  "porcentaje_uso_app_movil": 0.29,
  "cantidad_perfiles_creados": 5,
  "interacciones_mensuales_soporte": 3,
  "distancia_promedio_red_km": 34.1
}
```

Respuesta:

```json
{
  "cluster": 1
}
```

## Perfilamiento de segmentos

Luego de la predicción se genera un resumen con características promedio:

Ejemplo:

| Segmento |                                                    Descripción                                                    | Perfil                           |
| :------- | :---------------------------------------------------------------------------------------------------------------: | -------------------------------- |
| 0        | Usuarios con un bajo promedio de horas de consumo mensual y con un alta cantidad de promedio de contenidos vistos | Usuario explorador               |
| 1        |                  Usuarios sensibles a promociones y baja cantidad promedio de contenidos vistos                   | Usuarios sensibles a promociones |
| 2        |                 Usuarios intensivos con un alto consumo mensual y baja sensibilidad a promociones                 | Usuario Premium                  |

El perfil se obtiene analizando:

- promedio de horas de consumo mensual,
- gasto mensual promedio,
- cantidad promedio de contenidos vistos,
- antigüedad promedio,
- porcentaje de uso de promociones,
- promedio de dispositivos utilizados.

## Detener servicios

Para detener los contenedores:

```bash
docker compose down
```

Para eliminar también los volúmenes:

```bash
docker compose down -v
```

## Para cambios de código:

Para detener los contenedores:

```bash
docker compose down
```

Para eliminar también los volúmenes:

```bash
docker compose build --no-cache
```

Luego, levantamos:

```bash
docker compose up
```

Para verificar el contenido de la tabla:

```bash
docker exec -it crm_database psql -U admin -d analisis_streaming
```

Luego, para ver las tablas, ejecutar:

```bash
\dt
```
