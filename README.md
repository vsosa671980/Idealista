# Análisis Inmobiliario mediante Web Scraping y Machine Learning

## Máster de Programación Avanzada en Python para Big Data, Hacking y Machine Learning .


![Portada](/imgproject\Portada.png)

Ante la variación de los precios de venta y alquiler de inmuebles, y gracias a la existencia de portales inmobiliarios, podemos observar tendencias o aproximaciones de los precios de dichos inmuebles, que no llegan a ser más que conjeturas basadas en la observación, desde el punto de vista de un particular. En el caso de profesionales, parten de grandes bases de datos, y costosos estudios de mercado, que llevan en su mayoría un laborioso trabajo que implican grandes cantidades de dinero y tiempo.

Debido a la abundancia de información disponible en diversas plataformas sobre propiedades, es factible utilizar estos datos para crear modelos de predicción que permitan estimar el valor de una propiedad en el mercado en función de sus características específicas.

En este trabajo se quiere presentar una solución al mercado inmobiliario, que se podrá aplicar tanto a profesionales como a particulares. Para acotar el problema, se ha elegido la Isla de Gran Canaria para elaborar la Base de Datos.

Se pretende elaborar un modelo para la predicción del precio de mercado de un inmueble en Las Islas Canarias empleando técnicas de Machine Learning aprendidas durante el Master. Los datos para su realización se extraerán de la web de la plataforma idealista, mediante técnicas de Web Scraping.  

Los datos se quieren incorporar en una Base de datos SQL para su posterior utilización en el algoritmo de aprendizaje, así como para explotar y analizar esos datos para realizar gráficas que ayuden a la hora de elegir una vivienda.

Por tanto, la aplicación no solo contará con el modelo de predicción, si no que podrá ser una herramienta de análisis inmobiliario, mostrando gráficas y datos de interés. Con opción a filtrado y elección de datos.

Al tratarse de un trabajo en grupo, utilizaremos una metodología Ágil para coordinar y repartir los trabajos, para que todos participemos de igual medida en la consecución de los objetivos marcados.

* **Vicente Sosa Alcolea**

### Pre-requisitos 📋

Se encuentrasn todos en el archivo _requirements.txt

```
pip install -r requirements.txt
```
## RUN SERVER

idealista_app/tfm/tfm/

python manage.py runserver

## Tecnologias usadas

### Parte Web

Python con Framwork Django en el servidor.

Uso de Templates en la parte de la vista combinadas con Javascript.

## Graficos

Matplotlib

## Machine Learning 

Scki-learn

## Scrapping 

BeautifulSoup

## Base de Datos 

Relacional Sql-lite

# Imagenes de la aplicacion
### Pantalla Inicio

![Portada](imgproject\Portada.png)

### Descarga de datos 

![Portada](imgproject\scrapping.png)

### Carga de datos

![Portada](imgproject\descarga.png)

### Listado de Casas

![Portada](imgproject\listado.png)

### Grafico de desviacion precios predichos y precio real

![Portada](imgproject\graficos.png)
