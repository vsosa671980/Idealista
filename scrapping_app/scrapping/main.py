import os
import sys
# get current directory
path = os.path.dirname(__file__)
# parent directory
parent = os.path.dirname(path)
grandParent = os.path.dirname(parent)
# appending a path
sys.path.append(grandParent)
#TODO: QUITAR LO DE ARRIBA EN PRODUCCION
#import django
#django.setup()
#TODO: quitar lo de arriba en produccion
from scrapping_app.scrapping.config import IDEALISTA_NAME,URL_GOOGLE,URL_MAIN_IDEALISTA,DATABASE_NAME
from scrapping_app.scrapping.all_zones_houses import get_and_save_houses_from_all_zones
from scrapping_app.scrapping.req_html import Httpx_Client
from scrapping_app.scrapping.get_zones import get_zones_from_aera
from db_app.data_base.dao import HouseDao
from scrapping_app.scrapping.single_zone_all_pages_houses import get_and_save_houses_from_single_zone

def configure(final_url):
    httpx_client = Httpx_Client(IDEALISTA_NAME)
    # comenzamos viniendo de google y abrimos sesión abriendo la página de idealista.
    previous_url = URL_GOOGLE
    next_url = URL_MAIN_IDEALISTA
    # Hacemos este primer request para que la página nos detecte que empezamos a navegar
    # desde google
    httpx_client.get_html_from_url(next_url,previous_url)
    # Ahora la página previa es idealista.com
    previous_url = next_url
    # Hariamos una primera busqueda de la zona y nos aparece el mapa viniendo de idealista.com.
    next_url = URL_MAIN_IDEALISTA + final_url
    # Aquí empieza todo y se guarda en la base de datos
    house_dao = HouseDao(DATABASE_NAME)
    return httpx_client,next_url,previous_url,house_dao

def get_zones(final_url,zones_from_db=False):
    """
    Function using django interface, for getting the url zones from gran canaria
   
    PARAMETERS
    ----------
    final_url: "/venta-viviendas/las-palmas/gran-canaria/mapa" 
    zones_from_db: Use the zone from db file or from idealista directly.
  
    """
    httpx_client,next_url,previous_url,house_dao = configure(final_url)
    if zones_from_db == '0' or zones_from_db is False:
        zones = get_zones_from_aera(httpx_client,next_url,previous_url)
    else:
        zones = house_dao.get_zones_from_data_base()
    return zones

def get_houses_from_zone_url(zone_url):
    """
    Main function using django interface, download the houses from a single zone_url
   
    PARAMETERS
    ----------
    zone_url: "/venta-viviendas/las-palmas/gran-canaria/mapa" The final part of area URL we want to scrap´
  
    """
    httpx_client,next_url,previous_url,house_dao = configure(zone_url)
    houses, status = get_and_save_houses_from_single_zone(httpx_client,next_url,previous_url,house_dao)
    print(houses)
    print(status)
    
def start_scrapping_from_url(final_url,zones_from_db=False):
    """
    Main function using console, not interface
   
    PARAMETERS
    ----------
    final_url: "/venta-viviendas/las-palmas/gran-canaria/mapa" The final part of area URL we want to scrap´
    zones_from_db: Use the zone from db file or from idealista directly.
    """
    httpx_client,next_url,previous_url,house_dao = configure(final_url)
    get_and_save_houses_from_all_zones(httpx_client,
                                       next_url,
                                       previous_url,
                                       house_dao,
                                       zones_from_db=zones_from_db)



if __name__== '__main__':

    # PARA HACER PRUEBAS SIN INTEFAZ GRAFICO

    #final_url = "/venta-viviendas/telde-las-palmas/"
    #final_url = "/venta-viviendas/las-palmas/gran-canaria/agaete-centro/"
    #final_url = "/venta-viviendas/las-palmas-de-gran-canaria-las-palmas/"
    #final_url  = "/venta-viviendas/las-palmas/gran-canaria/mapa"
    #start_scrapping_from_url(final_url)
    #get_zones(final_url)
    print("OK")

