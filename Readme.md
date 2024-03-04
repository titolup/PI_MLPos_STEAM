![6CF774EC-A503-4B93-BF63-47A9CE38A14A](https://github.com/titolup/PI_MLPos_STEAM/assets/113148754/2a94ce95-c3d4-48df-9d24-d89ed57c3730)



# *Proyecto Individual 1 - Machine Learning MLOps*
El propósito fundamental de este proyecto es simular el rol de un MLOps Engineer, que amalgama las competencias de un Data Engineer y un Data Scientist, dentro del contexto dinámico de la plataforma de juegos Steam. El desafío empresarial que se plantea es la creación de un Producto Mínimo Viable (MVP) que integre una API desplegada conjuntamente con un modelo de Machine Learning. Este modelo debe ser capaz de efectuar un análisis de sentimientos basado en los comentarios de los usuarios, al tiempo que provee un sistema de recomendación de videojuegos personalizado para la plataforma.

## *El proyecto se fundamenta en el análisis de tres archivos en formato JSON GZIP:*

'**output_steam_games.json**´: Este archivo contiene un dataframe que detalla información crucial sobre los juegos, incluyendo el nombre del juego, el editor, el desarrollador, los precios y etiquetas asociadas.

'**australian_users_items.json**': Aquí se encuentra un dataframe que proporciona información sobre los juegos utilizados por los usuarios australianos, junto con el tiempo dedicado por cada usuario a cada juego.

'**australian_users_reviews.json**´: Este archivo alberga un dataframe que recopila los comentarios realizados por los usuarios australianos sobre los juegos que han utilizado. Incluye recomendaciones o críticas, así como datos adicionales como URL y user_id asociados a cada comentario.

Estos archivos, comprimidos en formato JSON GZIP, ofrecen un amplio conjunto de datos para realizar un análisis exhaustivo sobre la experiencia de los usuarios con los juegos.

Puedes encontrar los detalles de los conjuntos de datos en los siguientes enlaces:
- [Dataset_steam_games.json](enlace)
- [Datasets_users_items.json](enlace)
- [Datasets_users_reviews.json](enlace)



## **Tareas Realizadas:**

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



## **Análisis Exploratorio de los Datos:**

Durante esta fase del proyecto, se llevó a cabo un análisis exhaustivo de los tres conjuntos de datos después de completar el proceso de ETL. El objetivo principal fue obtener una visualización detallada de cada variable, tanto categórica como numérica. Esto permitió identificar con precisión las variables críticas necesarias para el modelo de recomendación, que representa el objetivo final del proceso de aprendizaje automático (Machine Learning).




## **Desarrollo de la API:**

Para el desarrollo de la API, se seleccionó el framework FastAPI, implementando las siguientes funciones:

1. `developer`: Esta función recibe como entrada 'desarrollador' devuelve cantidad de items y porcentaje de contenido free por año según empresa desarrolladora.

2. `userdata`: Esta función tiene por parámentro 'user_id' y devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendaciones que realizó sobre la cantidad de reviews que se analizan y la cantidad de items que consume el mismo.

3. `userforgenre`: Se proporciona el género de un videojuego como parámetro y devuelve el usuario que acumula más horas jugadas para el genero dado y una lista de acumulacion de horas jugadas por año de lanzamiento.

4. `best_developer_year`: Esta función recibe como parametro el año y devuelve el top 3 de desarrolladores con más juegos recomendados por usuarios para el año dado.

5. `developer_reviews_analysis`: Esta funcion recibe como entrada el nombre de la empresa desarrolladora y devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un analisis de sentimiento como valor positivo o negativo.

6. `recomendacion_juego`: Se ingresa el nombre de un juego (id) y se obtiene una lista con 5 juegos recomendados similares al ingresado.

Es importante destacar que la función "recomendacion_juego" se añadió a la API, sin embargo, solo "recomendacion_juego" en el notebook de modelado es la correcta, ya que la implementación en Render no fue posible debido a restricciones de capacidad de almacenamiento. Por lo tanto, para utilizar esta función, se debe ejecutar la API localmente.

## **Modelado (Desarrollo del Modelo de Aprendizaje Automático):**

En esta fase del proyecto, se utilizan los conjuntos de datos obtenidos durante la etapa de Feature Engineering, especialmente el dataset "steam_games", que contiene información crucial como los géneros de videojuegos, los títulos y las identificaciones correspondientes.

Una función destacada en esta etapa es "recomendacion_juego", la cual toma como parámetro el "id" de un título de juego y devuelve una lista con 5 juegos recomendados similares. Esto se logra mediante una comparación item-item, basada en la similitud de géneros entre los juegos.

## **FastAPI:**

El código para generar la API se encuentra en el archivo Main. Para ejecutar la API desde localhost, sigue estos pasos:


1. Clona el proyecto utilizando el comando: `git clone https://github.com/titolup/PI_MLPos_STEAM.

2. Prepara el entorno de trabajo en Visual Studio Code:

    - Crea un entorno virtual con el comando: `python -m venv env`.
    - Activa el entorno virtual con: `env\Scripts\activate`.
    - Instala las dependencias ejecutando: `pip install -r requirements.txt`.

3. Ejecuta el archivo `main.py` desde la consola activando `uvicorn`. Utiliza el siguiente comando: `uvicorn main:app --reload`.

4. Haz clic en la dirección que aparece en la consola (http://XXX.X.X.X:XXXX) o cópiala en tu navegador.

5. Una vez en el navegador, agrega "/docs" al final de la URL para acceder a ReDoc.

6. Dentro de cada función, haz clic en "Try it out", luego introduce los datos necesarios o utiliza los ejemplos por defecto. Finalmente, haz clic en "Execute" para ver la respuesta.

¡Con estos pasos podrás ejecutar y probar la API localmente en tu máquina!


## **Despliegue de la API en Render:**

Para el despliegue de la API, se optó por la plataforma Render, una solución en la nube unificada que permite crear y ejecutar aplicaciones y sitios web de manera eficiente. Render ofrece la ventaja de desplegar automáticamente las aplicaciones directamente desde GitHub.

El proceso comenzó con la creación de un nuevo servicio en Render, el cual se conectó a este repositorio. Como resultado, la API ahora está completamente operativa y accesible a través del siguiente enlace: [URL del servicio Render](https://api-p1-70mr.onrender.com/docs#).


## **Video:**

Para obtener una explicación y demostración del funcionamiento de la API, puedes acceder al siguiente enlace de video:

[Enlace al video de explicación y demostración de la API](enlace_al_video)


## **Conclusiones:**

Este proyecto representa una valiosa aplicación de los conocimientos adquiridos durante el programa de Data Science en HENRY. Ha abordado con éxito tareas típicas tanto de un Data Engineer como de un Data Scientist. Logramos cumplir con el objetivo de desarrollar un Producto Mínimo Viable (MPV), consistente en la creación de una API y su posterior despliegue en un servicio web.

A pesar de haber alcanzado el objetivo principal, es crucial reconocer que existen áreas para mejorar. Las funciones implementadas podrían optimizarse aún más para obtener resultados más eficientes y precisos, especialmente considerando las limitaciones de almacenamiento que se presentaron durante el proyecto. Esto subraya la importancia de la iteración continua y la búsqueda constante de la excelencia en el desarrollo de proyectos de este tipo.

En definitiva, este proyecto ha sido una oportunidad invaluable para aplicar de manera práctica los conceptos teóricos aprendidos en un entorno real. Ha proporcionado una experiencia significativa que nos ha permitido crecer como profesionales en el campo de la ciencia de datos.
















