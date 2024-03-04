![6CF774EC-A503-4B93-BF63-47A9CE38A14A](https://github.com/titolup/PI_MLPos_STEAM/assets/113148754/2a94ce95-c3d4-48df-9d24-d89ed57c3730)



# **Machine Learning MLOps Videojuegos STEAM**
El propósito fundamental de este proyecto es desarrollar un Producto Mínimo Viable (MVP) que incluya una API y un modelo de Machine Learning diseñado para realizar análisis de sentimientos en los comentarios de los usuarios. Este modelo fue creado con el propósito de ofrecer un sistema de recomendación de videojuegos personalizado en la popular plataforma Steam.

## *Explorando el análisis de tres archivos en formato JSON GZIP:*

'**output_steam_games.json**´: Este archivo contiene un dataframe que detalla información crucial sobre los juegos, incluyendo el nombre del juego, el editor, el desarrollador, los precios y etiquetas asociadas.

'**australian_users_items.json**': Aquí se encuentra un dataframe que proporciona información sobre los juegos utilizados por los usuarios australianos, junto con el tiempo dedicado por cada usuario a cada juego.

'**australian_users_reviews.json**´: Este archivo alberga un dataframe que recopila los comentarios realizados por los usuarios australianos sobre los juegos que han utilizado. Incluye recomendaciones o críticas, así como datos adicionales como URL y user_id asociados a cada comentario.

Estos archivos, comprimidos en formato JSON GZIP, ofrecen un amplio conjunto de datos para realizar un análisis exhaustivo sobre la experiencia de los usuarios con los juegos.

Puedes encontrar los detalles de los conjuntos de datos en los siguentes enlaces:

- [Steam_Games.json](https://github.com/titolup/PI_MLPos_STEAM/blob/main/Datasets_Steam_Games/steam_games.json.gz)

- [User_reviews.json](https://github.com/titolup/PI_MLPos_STEAM/blob/main/Datasets_User_Reviews/user_reviews.json.gz)
   
-[](enlace)


## **Actividades Desarrolladas:**

**ETL (Extracción, Transformación y Carga):**
Durante esta etapa crítica del proyecto, se ejecutaron tres Notebooks fundamentales: ETL_steam, ETL_reviews y ETL_items. El propósito principal fue extraer datos de los dataframes iniciales para adquirir familiaridad con ellos y, seguidamente, iniciar la crucial fase de limpieza de datos. Este proceso implicó la eliminación de cualquier elemento que pudiera obstruir la comprensión y la interpretación precisa del archivo, garantizando así la efectividad en el logro de los objetivos del proyecto. Una vez completada la limpieza, se procedió a generar los datasets necesarios para la fase subsiguiente, comprimiéndolos en formato Parquet para una gestión y almacenamiento optimizados.

**Feature Engineering:**
En esta etapa, se llevó a cabo un análisis de sentimientos utilizando la biblioteca TextBlob, aplicada específicamente a una columna que contenía los comentarios de los usuarios en el dataset user_reviews. Como resultado, se creó una nueva columna que clasifica los sentimientos en negativos, neutros o positivos. TextBlob, integrada dentro de una biblioteca de procesamiento de lenguaje natural (NLP), analiza los comentarios de los usuarios, calcula la polaridad del sentimiento y los clasifica en consecuencia.

Además de la implementación de esta metodología, se prepararon en esta fase los conjuntos de datos necesarios para el tratamiento de cada función específica. Esto permitió optimizar y mejorar los tiempos de ejecución del servicio en la nube, facilitando así el despliegue de la API y la resolución eficiente de consultas.


## **Funciones Endpoints:**

En esta etapa del proyecto, se seleccionaron cuidadosamente los conjuntos de datos necesarios para abordar cada función específica. Este enfoque se llevó a cabo con el objetivo de optimizar significativamente el rendimiento y mejorar los tiempos de procesamiento asociados a cada tarea.

Las funciones creadas incluyen:

- **developer(desarrollador: str)**: Esta función devuelve la cantidad de ítems y el porcentaje de contenido gratuito por año, según el desarrollador de la empresa.

- **userdata(user_id: str)**: Devuelve el monto total gastado por el usuario, el porcentaje de recomendaciones basado en las revisiones y la cantidad de elementos.

- **UserForGenre(genero: str)**: Esta función identifica el usuario que acumula más horas jugadas para un género específico, junto con una lista que muestra la acumulación de horas jugadas por año de lanzamiento.

- **best_developer_year(año: int)**: Proporciona el top 3 de desarrolladores con los juegos más recomendados por los usuarios para el año indicado.

- **developer_reviews_analysis(desarrolldora:str)**: Devuelve un diccionario con el nombre del desarrollador y cantidad de registros con reseñas de usuarios categorizadas con un analisis de sentimiento como positivo o negativo.


## **Exploracion y Análisis de Datos (EDA):**

Durante esta fase del proyecto, se llevó a cabo un análisis exhaustivo de los tres conjuntos de datos después de completar el proceso de ETL. El objetivo principal fue obtener una visualización detallada de cada variable, tanto categórica como numérica. Esto permitió identificar con precisión las variables críticas necesarias para el modelo de recomendación, que representa el objetivo final del proceso de aprendizaje automático (Machine Learning).



## **Modelado (Desarrollo del Modelo de Aprendizaje Automático):**

En esta fase del proyecto, se utilizan los conjuntos de datos obtenidos durante la etapa de Feature Engineering, especialmente el dataset "steam_games", que contiene información crucial como los géneros de videojuegos, los títulos y las identificaciones correspondientes.

Una función destacada en esta etapa es "recomendacion_juego", la cual toma como parámetro el "id" de un título de juego y devuelve una lista con 5 juegos recomendados similares. Esto se logra mediante una comparación item-item, basada en la similitud de géneros entre los juegos.


## **Desarrollo de Funciones API:**

En esta etapa del proyecto, se llevó a cabo el desarrollo de los endpoints requeridos mediante [Funciones](https://github.com/titolup/PI_MLPos_STEAM/blob/main/5_Funciones.ipynb), implementadas dentro del archivo Funciones.ipynb. Después de instalar FastAPI y uvicorn, se configuró un archivo [main.py](https://github.com/titolup/PI_MLPos_STEAM/blob/main/main.py) con la estructura necesaria para poner en funcionamiento los endpoints.

Estas funciones se alimentan con datos provenientes de los archivos PARQUET generados en ETL y luego tratados en el archivo [Tablas_Union_Funciones](https://github.com/titolup/PI_MLPos_STEAM/blob/main/main.py) para poder optimizar el almacenamiento para poder posteriormente realizar el deploy en Render.

Todo el proceso de desarrollo se realizó localmente en Visual Studio Code, haciendo uso de herramientas como Jupyter Notebook, Python, numpy, pandas, FastAPI y uvicorn. Esta combinación de tecnologías permitió dar vida a los endpoints de la API, proporcionando un acceso exitoso a las funcionalidades desarrolladas en el proyecto.

![A368FB0A-85EF-41BC-88B4-A694DF131B84](https://github.com/titolup/PI_MLPos_STEAM/blob/main/Imagenes/A368FB0A-85EF-41BC-88B4-A694DF131B84.PNG)



## **Despliegue de la API en Render:**

Para el despliegue de la API, se optó por la plataforma Render, una solución en la nube unificada que permite crear y ejecutar aplicaciones y sitios web de manera eficiente. Render ofrece la ventaja de desplegar automáticamente las aplicaciones directamente desde GitHub.

El proceso comenzó con la creación de un nuevo servicio en Render, el cual se conectó a este repositorio. Como resultado, la API ahora está completamente operativa y accesible a través del siguiente enlace: [URL del servicio Render](https://api-p1-70mr.onrender.com/docs#).


## **Video:**

Para obtener una explicación y demostración del funcionamiento de la API, puedes acceder al siguiente enlace de video:

[Enlace al video de explicación y demostración de la API](enlace_al_video)


## **Autor:**
Este proyecto fue realizado por : [**Natalia Paez Marin**](https://github.com/titolup) como proyecto individual para el bootcamp de Data Science de Henry.

















