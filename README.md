# 🎮 Modelo de Recomendación de Juegos en Steam

Proyecto MLOps - SteamGames

👨‍💻 Sebastián Risi - 2023

[🚀 Ingreso a la API](https://pi-mlops-steamgames-git.onrender.com/docs).

🎥 [Video Explicativo](https://www.loom.com/share/094ab96bbf8643b5986d67678e267d44?sid=2e93f1b1-2ee7-4027-87ba-2f9280c1095a).

## 📝 Descripción del Proyecto

Este proyecto simula el rol de un MLOps Engineer, que combina habilidades de Data Engineer y Data Scientist, en el contexto de la plataforma de juegos Steam. El desafío de negocio consiste en crear un Producto Mínimo Viable (MVP) que incluya una API desplegada y un modelo de Machine Learning. Este producto debe poder realizar algunas consultas útiles sobre la plataforma de Steam. Por otro lado, implemente un sistema de recomendación basado en la similitud de los juegos.

## 📊 Datos

El desarrollo del proyecto se basa en tres archivos JSON comprimidos (GZIP):

* **output_steam_games.json**: Contiene información sobre los juegos, como el nombre, el editor, el desarrollador, los precios y las etiquetas.
* **australian_users_items.json**: Proporciona información sobre cómo los usuarios interactúan con los juegos, incluido el tiempo que pasan jugando.
* **australian_users_reviews.json**: Contiene los comentarios y reseñas que los usuarios hacen sobre los juegos, junto con recomendaciones y otros datos como URLs y IDs de usuario.

## 🛠️ Tareas Realizadas

### ETL (Extracción, Transformación y Carga)

En esta fase del proyecto, se llevaron a cabo las siguientes actividades utilizando los Notebooks ETL_steam_games, ETL_user_reviews y ETL_user_items:

1. Extracción de datos desde los archivos JSON iniciales para familiarizarse con ellos y comenzar la limpieza de datos.
2. Limpieza de los datos para eliminar información innecesaria y asegurar una comprensión adecuada.
3. Conversión de los datos a formato Parquet para su uso posterior.

### Feature Engineering

En esta fase del proyecto se realiza el análisis de sentimientos, utilizando la librería TextBlob. La librería TextBlob es parte de una biblioteca de procesamiento de lenguaje natural (NLP); la que toma un comentario de un usuario, calcula la polaridad del sentimiento y luego lo clasifica como negativo, neutral o positivo.

Además de la utilización de esta metodología, se prepararon los datasets necesarios para el tratamiento de cada función específica, logrando la optimización y mejora de los tiempos del funcionamiento del servicio de la nube para deployar la API y resolver las consultas.

### Análisis Exploratorio de Datos (EDA)

Se llevó a cabo un análisis exploratorio de los tres conjuntos de datos después del proceso ETL. Esto permitió visualizar las variables categóricas y numéricas, identificando las que son esenciales para el modelo de recomendación final del Machine Learning.

### Modelado (Desarrollo de Modelos de Machine Learning)

Este proyecto se basó en el dataset `steam_games` y se desarrolló una función llamada `recommend_games`, que proporciona recomendaciones de juegos similares según el género utilizando una comparación de elementos. Esta función se ejecuta mediante el modelo de recomendación item-item. Se aplicó la *similitud del coseno*, una técnica comúnmente empleada para comparar la similitud entre documentos, palabras o cualquier cosa que pueda ser representada como vectores en un espacio multidimensional.

#### Desarrollo de API

Se creó una API utilizando el framework FastAPI, que ofrece las siguientes funciones:

* **userdata**: Proporciona información sobre el gasto de un usuario, su porcentaje de recomendaciones y la cantidad de elementos que consume.
* **userforgenre**: Identifica al usuario que acumula más horas jugadas para el género dado y otorga una lista de la acumulación de horas jugadas por año de lanzamiento.
* **developer**: Ofrece detalles sobre el contenido desarrollado por una empresa y su porcentaje de contenido gratuito por año.
* **best_developer_year**: Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
* **sentiment_analysis**: Según el desarrollador, devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
* **recommend_games**: Recomienda 5 juegos similares a uno ingresado.

### FastAPI

El código para la generación de la API se encuentra en el archivo `Main`. Para ejecutar la API localmente, siga estos pasos:

1. Clonar el proyecto con `git clone https://github.com/sebastianr92/PI_MLOps_SteamGames.git`
2. Levantar un entorno virtual con `python -m venv env`.
3. Activar el entorno virtual con `env\Scripts\activate`.
4. Instalar las dependencias con `pip install -r requirements.txt`.
5. Ejecutar el archivo `main.py` usando Uvicorn con `uvicorn main:app --reload`.
6. Acceder a la documentación de la API en su navegador usando la dirección `http://XXX.X.X.X:XXXX/docs`.
7. Utilizar las funciones proporcionadas.

### Deploy

El despliegue de la API se realizó en la plataforma Render, que es una solución en la nube para crear y ejecutar aplicaciones web. Se generó un servicio en Render conectado a este repositorio y se puede acceder a la API en el siguiente enlace: [Link de la API](https://pi-mlops-steamgames-git.onrender.com).

## 🎬 Video

Puede ver una explicación y demostración detallada del funcionamiento de la API en el siguiente [video](https://www.loom.com/share/094ab96bbf8643b5986d67678e267d44?sid=2e93f1b1-2ee7-4027-87ba-2f9280c1095a).

## 🌟 Conclusiones

Este proyecto se llevó a cabo utilizando los conocimientos adquiridos durante el programa de Data Science en Henry. Las tareas realizadas reflejan las responsabilidades típicas de un Data Engineer y un Data Scientist. El objetivo de un Producto Mínimo Viable (MVP) se logró con éxito, incluyendo una API y su despliegue en un servicio web. El modelo de recomendación puede ser mejorado y complejizado agreg...
