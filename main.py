"""
FUNCIONES PARA ALIMENTAR LA API
"""

#librerías
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pyarrow as pa
import pandas as pd
import numpy as np
#import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity


#instanciar la aplicación

app = FastAPI()

#Dataset a utilizar

gasto_por_usuario= pd.read_parquet("Data/df_gasto_por_usuario.parquet")
item_por_usuario = pd.read_parquet("Data/df_item_por_usuario.parquet")

recommend = pd.read_parquet("Data/recommend.parquet")
user_reviews = pd.read_parquet("Data/reviews.parquet")

usuario_mas_horas = pd.read_parquet("Data/df_funcion2_A.parquet")
tiempo_por_anio = pd.read_parquet("Data/df_funcion2_B.parquet")

df_funcion3 = pd.read_parquet("Data/df_funcion3.parquet")
df_funcion4 = pd.read_parquet("Data/df_funcion4.parquet")
df_funcion5 = pd.read_parquet("Data/df_funcion5.parquet")

modelo_item = pd.read_parquet("Data/modelo_item.parquet")

@app.get("/", response_class=HTMLResponse)
async def incio ():
    principal= """
    <!DOCTYPE html>
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Proyecto Henry: API de consultas sobre la plataforma de juegos Steam</h1>
            <p>Bienvenido a la API de Steam donde se pueden hacer diferentes consultas sobre la plataforma de videojuegos.</p>
            <p>INSTRUCCIONES:</p>
            <p>Escriba <span style="background-color: lightgray;">/docs</span> a continuación de la URL actual de esta página para interactuar con la API</p>
            <p> El desarrollo de este proyecto esta en <a href="https://github.com/sebastianr92/PI_MLOps_SteamGames.git"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
            <p>Sebastián Risi - 2023 -</p>
        </body>
    </html>

        """    
    return principal
    
#Función #1
@app.get( "/userdata/{user_id}", name = "userdata")
async def userdata(user_id : str):
  
    """
    Parametro: 
        user_id(str) : ID del Usuario a consultar.
    Retorna:
        user (dict): Información de un usuario ,
        -cantidad de dinero gastado (int): Dinero gastado por usuario
        -Porcentaje de recomendación usuario (float): Reviews realizadas por el usuario con respecto a la cantidad de 
        reviews poe usuario
        -cantidad de items (int):cantidad de juegos consumidos por usuario 
    """
        #Gasto por Usuario
    gasto = gasto_por_usuario[gasto_por_usuario["user_id"] == user_id]["Gasto total"]
    
    #Cantidad de recomendaciones del usuario ingresado
    rec_user= recommend[recommend["user_id"]== user_id]["recommend"].sum()
    #Cantidad de recomendaciones totales por usuario
    total_recomendaciones= len(user_reviews["user_id"].unique())
    porcentaje=(rec_user/total_recomendaciones)*100
    
    #Cantidad de juegos que utilizo el usuario 
    count= item_por_usuario[item_por_usuario["user_id"] == user_id]["items_count"]
    return{
        "Cantidad de dinero gastado": float(gasto.iloc[0]),
        "Porcentaje de recomendación usuario": round(float(porcentaje), 3),
        "Cantidad de items": int(count.iloc[0])
    }
    
#Función #2: USerForGenre

@app.get("/USerForGenre/{}/{genero}", name = "USerForGenre")
async def USerForGenre(genero: str):
    """
    Parametro: 
        genero: (str) : Género a consultar.
    Retorna:
        usuario que acumula más horas jugadas para el género dado 
        lista de la acumulación de horas jugadas por año de lanzamiento.
    """

    df_genero_deseado = usuario_mas_horas[usuario_mas_horas["genres"] == genero]
    
    if df_genero_deseado.empty:
        return {"Mensaje": f"No hay datos para el género '{genero}'"}


    # Encuentra el usuario que más jugó ese género.
    usuario_mas_jugo = df_genero_deseado.groupby('user_id')["playtime_forever"].sum().idxmax()
    
    horas_jugadas_por_anio = tiempo_por_anio[(tiempo_por_anio["genres"] == genero) & 
                            (tiempo_por_anio["user_id"] == usuario_mas_jugo)].drop(["user_id", "genres"], axis=1)


    retorno = {"Usuario con más horas jugadas para " + genero: usuario_mas_jugo , 
                "Horas jugadas": [{"Año": anio, "Horas": horas} for anio, horas in 
                horas_jugadas_por_anio.reset_index(drop=True).values]}

    return retorno


#Función #3: developer
@app.get("/developer/{}/{desarrolladora}", name = "developer")
async def developer(desarrollador):
    """
    Parametros:
        -desarrollador (str): El desarrollador del juego Steam que se ingresa 
    Retorna: dataframe:
        -Año
        -Cantidad de items por año: cantidad de juegos publicados por el desarrollador en el año 
        -Porcentaje de juegos free: porcentaje de juegos gratis con respecto a los publicados en ese año
    """
    
    # Filtra el DataFrame df_funcion3 para igualarlo al valor que se ingresa
    data = df_funcion3[df_funcion3["developer"] == desarrollador]
    
    if data.empty:
        return {"message": "Desarrollador no encontrado"}
    
    # Convierte la columna "item_id" a tipo de dato entero
    data["item_id"] = data["item_id"].astype(int)
    data['Año_estreno'] = data['Año_estreno'].astype(int)

    
    # Realiza las operaciones de conteo y cálculo
    cantidad = data.groupby("Año_estreno")["item_id"].count()
    free_anio = data[data["price"] == 0.0].groupby("Año_estreno")["item_id"].count()
    porcentaje_gratis = (free_anio / cantidad * 100).fillna(0).astype(int)
    
    # Crea una salida como DataFrame
    tabla = pd.DataFrame({
        "Año": cantidad.index,
        "Cantidad de items por año": cantidad.values,
        "Porcentaje de juegos free": porcentaje_gratis.apply(lambda x: str(x) + "%").tolist() #valor
    })
    
    tabla = tabla.to_dict(orient="records")
    return tabla



# Función #4: best_developer_year
@app.get("/best_developer_year/{anio}", name = "best_developer_year")
async def best_developer_year(anio):
    """
    Parametros:
        -Anio (int): Se ingresa un año
    Retorna: 
        Devuelve el top 3 de desarrolladores 
        con juegos MÁS recomendados por usuarios para el año dado.
        (reviews.recommend = True y comentarios positivos)
    """

    # Filtrar el DataFrame combinado para obtener los juegos del año especificado
    juegos_del_anio = df_funcion4[df_funcion4['Año_estreno'] == str(anio)]

    # Filtrar los juegos recomendados (recommend = True y comentarios positivos)
    juegos_recomendados = juegos_del_anio[(juegos_del_anio['recommend'] == True) & (juegos_del_anio['sentiment_analisis'] == 2)]

    if juegos_recomendados.empty:
        return {"Mensaje": f"No hay juegos recomendados para el año {anio}"}

    # Calcular el número de juegos recomendados por desarrollador
    juegos_por_desarrollador = juegos_recomendados.groupby('developer')['app_name'].count().reset_index()

    # Ordenar por número de juegos recomendados en orden descendente
    juegos_por_desarrollador = juegos_por_desarrollador.sort_values(by='app_name', ascending=False).reset_index()

    # Tomar los 3 primeros desarrolladores
    top_desarrolladores = juegos_por_desarrollador.head(3)

    # Construir el resultado en el formato deseado
    resultado = [{"Puesto " + str(i + 1): row['developer']} for i, row in top_desarrolladores.iterrows()]

    return resultado


#Función #5: developer_reviews_analysis

@app.get("/developer_reviews_analysis/{desarrolladora}", name = "developer_reviews_analysis")
async def developer_reviews_analysis(desarrolladora):
    """
    Parametros:
        -desarrolladora (str): Se ingresa una desarrolladora 
    Retorna: Diccionario
        Devuelve un diccionario con el nombre del desarrollador como llave 
        y una lista con la cantidad total de registros de reseñas de usuarios que se 
        encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
    """

    # Filtrar el DataFrame df_funcion5 por el desarrollador y por análisis de sentimiento positivo o negativo
    desarrolladora_reviews = df_funcion5[(df_funcion5['developer'] == desarrolladora) & ((df_funcion5['sentiment_analisis'] == 0) | (df_funcion5['sentiment_analisis'] == 2))]

    if desarrolladora_reviews.empty:
        return {desarrolladora: {'Positive': 0, 'Negative': 0}}

    # Contar la cantidad de reseñas positivas y negativas
    count_positive = (desarrolladora_reviews['sentiment_analisis'] == 2).sum()
    count_negative = (desarrolladora_reviews['sentiment_analisis'] == 0).sum()

    # Crear el diccionario de retorno
    resultado = {desarrolladora: ["Negative = " + str(count_negative), "Positive = " + str(count_positive)]}

    return resultado

#Modelo de recomendacion item_item

@app.get("/recommend_games/{id}", name= "recommend_games")
async def recommend_games(id: int):
    
    '''
    Esta función recomienda 5 juegos a partir del juego ingresado.

    Args:
        game_id (int): ID único del videojuego al cual se le harán las recomendaciones.
    '''

    # Verifica si el juego con game_id existe en df_games
    game = modelo_item[modelo_item['item_id'] == id]

    if game.empty:
        return(f"El juego '{id}' no posee registros.")
    
    # Obtiene el índice del juego dado
    idx = game.index[0]

    # Calcula la similitud de contenido solo para el juego dado y la muestra
    sim_scores = cosine_similarity([modelo_item.iloc[idx, 3:]], modelo_item.iloc[:, 3:])

    # Obtiene las puntuaciones de similitud del juego dado con otros juegos
    sim_scores = sim_scores[0]

    # Ordena los juegos por similitud en orden descendente
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # Obtiene los 5 juegos más similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # Lista de juegos similares (solo nombres)
    similar_game_names = modelo_item['app_name'].iloc[similar_game_indices].tolist()

    return {f"Juegos similares a {modelo_item[modelo_item['item_id'] == id]['app_name'].values[0]}: {', '.join(similar_game_names)}"}
