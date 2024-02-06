

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
from db_app.data_base.dao import HouseDao
import pandas as pd
matplotlib.use('Agg')

def generate_plot():
    # Código para generar el gráfico con Matplotlib
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 15, 25, 30]
    
    # Get all the houses
    
    # Create a dao house object
    dao = HouseDao('idealista_data_base')
    # Get the houses fron database
    houses = dao.get_all_houses()
    
    # Creating list of dictionaries
    list_houses = [house.serialize() for house in houses]
    
    # Creating dataFrame of houses
    df = pd.DataFrame(list_houses)
    

    
    # Get the mean price of each zone
    price_mean_for_zone = df.groupby("location_2")["last_price"].mean()
    price_mean_for_zone_calculated = df.groupby("location_2")["predicted_price"].mean()
    
    plt.rc('font', family='Montserrat')
    fig, ax = plt.subplots(figsize = (20,6))
    fig.set_facecolor('#BFF1FF')
    ax.plot(price_mean_for_zone.index,price_mean_for_zone.values,marker="o",label ="Mean Price")
    ax.plot(price_mean_for_zone_calculated.index,price_mean_for_zone_calculated.values,marker="o",label ="Mean Price Calculated")
    ax.set_xlabel('Prices',color = "#666666")
    ax.set_ylabel('Zones',color = "#666666")
    ax.set_title('Medias de precios por zonas',color = "#666666")
     # Configurar el color de fondo
    ax.set_facecolor('black')  # Puedes ajustar el color según tus preferencias
    ax.legend()
    # Rotate the  labels of x
    plt.xticks(rotation=45, ha='right')
    ax.tick_params(axis='x', colors='#666666')  # Cambia el color de los valores en el eje x 
    ax.tick_params(axis='y', colors='#666666') 
    plt.subplots_adjust( top=0.9, bottom=0.4)

    # Convertir la figura a formato base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    plt.close()

    return encoded_image