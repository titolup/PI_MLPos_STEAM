"""
FUNCIONES CREADAS PARA EL PROYECTO FINAL INDIVIDUAL 1 DE DATA SCIENCE DE SOY HENRY
                            - STEAM GAMES - 

FUNCIONES PARA ALIMENTAR LA API
"""

#uvicorn main:app --reload

#librerías
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, List, Union, Tuple
import pandas as pd
from pandas.core.frame import DataFrame
import scipy as sp
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional
from pydantic import BaseModel

# Instanciamos la aplicación

app = FastAPI()

# Dentro del script
df_EP1 = pq.read_table("1_desarrollador.parquet").to_pandas()
df_EP2 = pq.read_table("2User_id.parquet").to_pandas()
df_EP3 = pq.read_table("3genero.parquet").to_pandas()
df_EP4 = pq.read_table("4año.parquet").to_pandas()
df_EP5 = pq.read_table("5desarrolladora.parquet").to_pandas()
modelo_games = pq.read_table("modelo_train.parquet").to_pandas()


@app.get("/", response_class=HTMLResponse)
async def inicio():
    template = """
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
            <h1>API de consultas sobre juegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=template)

    
    
# Definir el modelo de respuesta
class DeveloperInfo(BaseModel):
    data: List[dict]

# Función para manejar la solicitud GET
@app.get("/developer/{desarrollador}", response_model=DeveloperInfo)
async def developer(desarrollador: str) -> DeveloperInfo:

    """
    Obtiene la cantidad y porcentaje de juegos gratuitos por año para un desarrollador específico.

    Parámetros:
    - desarrollador (str): El nombre del desarrollador de juegos para el cual se desea obtener la información. Ejemplo: "Valve", "Re-Logic", etc.

    Retorna:
    - DeveloperInfo: Un objeto que contiene una lista de diccionarios, cada uno representando un año con la cantidad de juegos y el porcentaje de juegos gratuitos para ese año.
    """

    listaaños = sorted(df_EP1.release_year.unique(), reverse=True)
    listadeveloper = df_EP1.developer.unique() 
    
    data = []
    
    if desarrollador in listadeveloper: 
        for años in listaaños:
            df_desarrollador = df_EP1[(df_EP1.developer == desarrollador) & (df_EP1.release_year == años)]
            cantidad_total_items = len(df_desarrollador)
            cantidad_items_free = len(df_desarrollador[df_desarrollador.price == 0])
            
            porcentaje_free = 0
            if cantidad_total_items != 0:
                porcentaje_free = round((cantidad_items_free / cantidad_total_items) * 100, 2)
                
            data.append({
                "Año": int(años),
                "Cantidad de Items": int(cantidad_total_items),
                "Contenido Free": f"{porcentaje_free}%"
            })
    else:
        print('No cuento con los registros de esa empresa en mi base de datos')

    return DeveloperInfo(data=data)
    



# Definir un modelo de respuesta alternativo que puede manejar tanto el caso de éxito como el caso de error
class UserDataResponse(BaseModel):
    User: str
    Dinero_gastado: str
    Porcentaje_de_recomendacion: str
    Cantidad_de_items: int

# Definir una función de ayuda para construir el modelo de respuesta para el caso de éxito
def build_success_response(user: str, dinero_gastado: str, porcentaje_recomendacion: str, cantidad_de_items: int) -> UserDataResponse:
    return UserDataResponse(
        User=user,
        Dinero_gastado=dinero_gastado,
        Porcentaje_de_recomendacion=porcentaje_recomendacion,
        Cantidad_de_items=cantidad_de_items
    )

# Definir una función de ayuda para construir el modelo de respuesta para el caso de error
def build_error_response(user_id: str) -> Union[dict, UserDataResponse]:
    raise HTTPException(status_code=404, detail=f"El usuario {user_id} especificado no existe.")

# Función para manejar la solicitud GET
@app.get("/userdata/{usuario}", name="USERDATA", response_model=Union[UserDataResponse, dict])
async def userdata(usuario: str) -> Union[UserDataResponse, dict]:
    """
    Obtiene información sobre el usuario especificado.

    Parámetros:
    - usuario (str): El ID del usuario a consultar. Ejemplo: "armouredmarshmallow", "exiaez", etc.

    Retorna:
    - Union[UserDataResponse, dict]: Información del usuario, incluyendo cantidad de dinero gastado, porcentaje de recomendación y cantidad de items, o un mensaje de error si el usuario no existe.
    """
    # Convertimos el ID del usuario proporcionado a minúsculas para una comparación sin distinción de mayúsculas
    usuario = usuario.lower()

    # Verificamos si el usuario está en la lista de usuarios
    if usuario in df_EP2.user_id.unique():
        # Filtramos el DataFrame por el usuario especificado
        df_usuario = df_EP2[df_EP2.user_id == usuario]

        # Calculamos la cantidad de dinero gastado
        dinero_gastado = round(df_usuario.price.sum(), 2)

        # Calculamos el porcentaje de recomendación
        porcentaje_recomendacion = int((df_usuario.recommend.mean()) * 100)

        # Obtenemos la cantidad de items del usuario
        cantidad_items = len(df_usuario)

        # Construimos el modelo de respuesta para el caso de éxito
        response = build_success_response(usuario, f"{dinero_gastado} USD", f"{porcentaje_recomendacion}%", cantidad_items)
    else:
        # Construimos el modelo de respuesta para el caso de error
        response = build_error_response(usuario)

    return response
    
    
#Funcion 3
@app.get("/userforgenre/{genero}", name="USERFORGENRE")
async def UserForGenre(genero: str) -> Dict[str, Union[str, List[Dict[str, Union[int, str]]]]]:
    """
    Devuelve el usuario con más horas jugadas para un género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

    Parámetros:
    - genero (str): El género para el cual se desea obtener la información. Ejemplo: "Action", "Adventure", "Strategy", etc.

    Retorna:
    - Un diccionario con la información solicitada, incluyendo el usuario con más horas jugadas para el género especificado y una lista de la acumulación de horas jugadas por año de lanzamiento, ordenada de forma descendente por año.
    """

    # Filtramos el DataFrame por el género dado
    df_genero = df_EP3[df_EP3['genres'].str.lower() == genero.lower()]

    if df_genero.empty:
        return {"mensaje": "No se encontraron datos para el género especificado."}

    # Obtenemos el usuario con más horas jugadas para el género dado
    usuario_mas_horas = df_genero.groupby('user_id')['playtime_hours'].sum().idxmax()

    # Creamos una lista de la acumulación de horas jugadas por año de lanzamiento, ordenada de forma descendente por año
    horas_por_año = df_genero.groupby('release_year')['playtime_hours'].sum().reset_index()
    horas_por_año = horas_por_año.rename(columns={'release_year': 'Año', 'playtime_hours': 'Horas'})
    horas_por_año = horas_por_año.sort_values(by='Año', ascending=False)

    # Convertir los valores de horas a minutos
    horas_por_año['Horas'] = (horas_por_año['Horas'] / 60).astype(int)

    # Convertir la lista de horas por año a formato de lista de diccionarios
    lista_horas_por_año = horas_por_año.to_dict('records')

    # Devolver la respuesta con los valores corregidos
    return {
        "Usuario con más horas jugadas para {}".format(genero): usuario_mas_horas,
        "Horas jugadas": lista_horas_por_año
    }


#Funcion 4
@app.get("/bestdeveloperyear/{year}", name="BESTDEVELOPERYEAR")
async def best_developer_year(year):
    """
    La siguiente función devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
    
    Ejemplos de entrada: 2010, 2011, 2012, ..., 2015
    """

    # Convertir el año a entero
    year = int(year)
    
    # Filtrar los datos por el año dado y las condiciones requeridas
    recom = df_EP4[(df_EP4["recommend"] == True) & (df_EP4["sentiment_analysis"] > 0) & (df_EP4["release_year"] == year)]
    
    # Verificar si hay registros para el año dado
    if recom.empty:
        return {"message": f"No hay registros para el año {year}."}
    
    # Agrupar por desarrollador y sumar las recomendaciones
    developer_recommendations = recom.groupby("developer")["recommend"].sum()
    
    # Obtener el top 3 de desarrolladores
    top_3_developers = developer_recommendations.nlargest(3)
    
    # Crear la lista de desarrolladores en el formato requerido
    top_developers_list = [{"Puesto " + str(rank): developer} for rank, (developer, count) in enumerate(top_3_developers.items(), start=1)]

    return top_developers_list




#Funcion 5
@app.get("/developerreviewsanalysis/{desarrolladora}", name="DEVELOPERREVIEWSANALYSIS")
async def DeveloperReviewsAnalysis(desarrolladora: str) -> Union[Dict[str, Dict[str, int]], Dict[str, str]]:
    """
    La siguiente función devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentran categorizados con un análisis de sentimiento como valor positivo o negativo.
    ...

    Ejemplos de entrada:
                        Valve
    """                    
    
    # Convertimos el nombre del desarrollador proporcionado a minúsculas para una comparación sin distinción de mayúsculas
    desarrolladora = desarrolladora.lower()
    
    # Convertimos los nombres de desarrolladores en el DataFrame a minúsculas para una comparación sin distinción de mayúsculas
    df_EP5['developer'] = df_EP5['developer'].str.lower()
    
    # Verificamos si el desarrollador proporcionado está en el DataFrame
    if desarrolladora not in df_EP5['developer'].unique():
        return {"message": "Mi base de datos no tiene registros de ese desarrollador"}
    
    # Filtramos el DataFrame por la desarrolladora y los registros con sentimiento distinto de neutro (1)
    df_filt_developer = df_EP5[(df_EP5['developer'] == desarrolladora) & (df_EP5['sentiment_analysis'] != 1)]
    
    # Verificamos si hay registros para la desarrolladora y si hay registros con análisis de sentimiento
    if not df_filt_developer.empty:
        # Contamos los sentimientos y mapeamos el número del sentimiento a su etiqueta correspondiente
        sentiment_counts = df_filt_developer['sentiment_analysis'].replace({0: 'Negative', 1: 'Positive', 2: 'Positive'}).value_counts()
        
        result = {desarrolladora.capitalize(): sentiment_counts.to_dict()}  # Convertimos la primera letra del nombre a mayúscula
    else:
        result = {"message": "No hay registros de análisis de sentimiento para esa desarrolladora en mi base de datos"}

    return result

                                                #'Valve', 'Outerlight Ltd.', 'GlyphX Games',
                                                #'Introversion Software', 'Facepunch Studios',
                                                #'Bugbear Entertainment', 'Funcom',
                                                #'Firaxis Games,Feral Interactive (Mac)',
                                                #'Crystal Dynamics,Feral Interactive (Mac)', 'CAPCOM Co., Ltd.',
                                                #'id Software', 'Gray Matter Studios', '2K Boston,2K Australia',
                                                #'Relic Entertainment', 'The Creative Assembly'


#Modelo de recomendacion item_item
@app.get("/recomendacion_juego/{id}", name= "RECOMENDACION_JUEGO")
async def recomendacion_juego(id: int):
    
    """La siguiente funcion genera una lista de 5 juegos similares a un juego dado (id)
    
    Parametros:
    
        El id del juego para el que se desean encontrar juegos similares. Ej: 10

    Retorna:
    
         Un diccionario con 5 juegos similares 
    """
    
    # Verificamos si el juego con game_id existe en df_games
    game = modelo_games[modelo_games['item_id'] == id]

    if game.empty:
        return("El juego '{id}' no posee registros.")
    
    # Obtenemos el índice del juego dado
    idx = game.index[0]

    # Tomamos una muestra aleatoria del DataFrame df_games
    sample_size = 2000  # Definimos el tamaño de la muestra (ajusta según sea necesario)
    df_sample = modelo_games.sample(n=sample_size, random_state=42)  # Ajustamos la semilla aleatoria según sea necesario

    # Calculamos la similitud de contenido solo para el juego dado y la muestra
    sim_scores = cosine_similarity([modelo_games.iloc[idx, 3:]], df_sample.iloc[:, 3:])

    # Obtenemos las puntuaciones de similitud del juego dado con otros juegos
    sim_scores = sim_scores[0]

    # Ordenamos los juegos por similitud en orden descendente
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # Obtenemos los 5 juegos más similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # Listamos los juegos similares (solo nombres)
    similar_game_names = df_sample['app_name'].iloc[similar_game_indices].tolist()

    return {"similar_games": similar_game_names}



