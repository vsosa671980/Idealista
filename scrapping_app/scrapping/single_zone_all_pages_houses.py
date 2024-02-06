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
from scrapping_app.scrapping.config import URL_MAIN_HOUSE_IDEALISTA, URL_GOOGLE
from bs4 import BeautifulSoup as bs
import scrapping_app.scrapping.single_page as single_page
from time import sleep
from random import randint
from db_app.data_base.dao import Db_save_state  
from scrapping_app.scrapping.single_house import parser_and_save_house_id
from scrapping_app.scrapping.error_logger import log_error


def get_and_save_houses_from_single_zone(httpx_client,zone_url,previous_url,house_dao):
    """
    Function that goes page by page downloading ids and houses

    Parameters
    ----------
        httpx_client(req_html): httpx session
        zone_url: URL of the last subzone that has no further divisions
        previous_url: Previous URL to create the header and simulate human-like usage
        house_dao: Data Base Conection

    Return
    ------
        ([results], False): [{'id': , 'price': , 'date': ,'status': House.status_house.status_House_db}]
                                Ends due to an error, not due to completion of the download
        ([results], True): [{'id': , 'price': , 'date': ,'status': House.status_house.status_House_db}]
                                Ends due to completion of the download, not due to an error

    """

    results = []
    # In theory, URLs should come without /mapa..., but I've seen cases where, for some reason, it doesn't disappear
    # I haven't been able to figure out the logic behind it
    zone_url = zone_url.replace("/mapa",'')
    # To avoid infinite loops
    page_attemps = 0
    new_page_attemps = 0
    prev_url = previous_url
    page_number = 1
    print(f"Downloading Zone: {zone_url} ")
    # We go through all the pages of the zone
    while True:
        print(f"Downloading page: {page_number} ")
        next_url = zone_url + f'/pagina-{page_number}.htm'
        print(next_url)
        html = httpx_client.get_html_from_url(next_url,prev_url)
        previous_url = next_url
        if html:
            soup = bs(html, 'html.parser')
            # check if we have reached the last page
            if page_number == single_page.get_actual_page_number(soup):
                # First, download all the IDs from the page.
                articles = single_page.get_housesId_from_page(soup)
            else:
                # If there are no more pages, end the loop."
                break
            # Now that we have all the IDs, we download all the houses from that list.
            page_results = single_page.get_and_save_houses_from_page(httpx_client,articles,previous_url,zone_url,house_dao)
            # Each result {'id': , 'price': , 'date': ,'status':}
            if page_results:
                page_number += 1
                results = results + page_results
                prev_url = next_url
        if  not html or not page_results:
            sleep(randint(2,6))
            page_attemps +=  1
            if page_attemps == 2:
                # 3 Errors on the same page.
                print(f"Some Problems on page: {page_number}")
                page_number += 1
                prev_url = next_url
                page_attemps = 0
                new_page_attemps += 1
                if new_page_attemps == 3:
                    # 3  Errors on 3 consecutive pages
                    print("Problems downloading")
                    # Ends due to an error, not due to download completion
                    return (results, False)
        else:
            page_attemps = 0
            new_page_attemps = 0
    print(f"{zone_url} DOWNLOADED.")
    # After the download is complete,
    # Check what we have downloaded against what is in the database 
    # List of downloaded IDs from the area that are not errors."
    not_error_ids = [int(obj["id"]) for obj in results if obj["status"] != Db_save_state.error]
    # Check the houses in that area that we have in the database
    #TODO: Quiero solo las ACTIVAS ... CAMBIAR,... CREAR FUNCION EN db.py y COMPROBAR
    houses_id_in_zone = house_dao.houses_ids_from_zone(zone_url)
    # Check the houses that are supposedly not active.
    not_active_ids = []
    try:
        not_active_ids = list(set(houses_id_in_zone) - set(not_error_ids))
    except Exception as e:
        log_error(f'(single_zone_all_pages_houses.py) Error on not_active_ids{e}')
    for id in not_active_ids:
        #TODO: Primero checkear que hay conexion por ejemplo a google. por si es fallo de conexión
        # Attempt a final download of those that were active
        # to verify if they are still active 
        # and if not, I mark them as inactive: 
        # Just in case there was an error in the download as well.
        house = house_dao.find_houses_by_id(id)
        if house.active:
            house_url = URL_MAIN_HOUSE_IDEALISTA + f"/{id}/"
            previous_url = URL_GOOGLE
            print("Downloading to check: " + house_url)
            html = httpx_client.get_html_from_url(house_url,previous_url)
            if html is not None:
                single_house_soup = bs(html, 'html.parser')
                result = parser_and_save_house_id(single_house_soup,id,house.operation,house.zone_url,house_dao)
                if result['status'] == Db_save_state.error:
                    house_dao.update_ad_state(id,False) # Inactivo
    # It finishes due to the completion of the download, not due to an error.
    return (results, True)  
