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
from scrapping_app.scrapping.config import OperationType, URL_MAIN_HOUSE_IDEALISTA
import random
from scrapping_app.scrapping.req_html import Httpx_Client
from bs4 import BeautifulSoup as bs
from scrapping_app.scrapping.single_house import parser_and_save_house_id
from db_app.data_base.dao import Db_save_state  
from scrapping_app.scrapping.error_logger import log_error

def get_housesId_from_page(houses_list_soup):
    """
    Returns all the IDs and prices of houses appearing on a single page.

    Parameters
    ----------
    houses_list_soup (BeautifulSoup): Soup of the page containing the list of houses.

    Returns
    -------
    {id: price}: All the IDs and prices of the houses on the page, randomly unordered.
    {}: If there are no houses or if there's an error.
    """
    try:
        articles = houses_list_soup.find("section",{"class":"items-container"}).find_all("article")
        ids_prices = {}
        for article in articles:
            id = article.get("data-adid")
            if id:
                price = int(article.find("div",{"class":"item-info-container"}).find("div",{"class":"price-row"}).find("span",{"class":"item-price h2-simulated"}).text.replace(".","").replace("€",""))
                ids_prices[id] = price
        return ids_prices
    except Exception as e:
        log_error(f'(single_page.py) Error getting houses ID from page {e}')
        return {}
    
def get_actual_page_number(houses_list_soup):
    """
    Parameters
    ----------
    houses_list_soup (BeautifulSoup): Soup of the page containing the list of houses.

    Returns
    -------
    page_number (int): The page number.
    1: If there's an error.
    """
    try:
        items = houses_list_soup.find("main",{"class":"listing-items"})
        items = items.find("div",{"class":"pagination"})
        numero_pagina = int(items.find("li",{"class":"selected"}).text)
        return numero_pagina
    except:
        return 1

def get_and_save_houses_from_page(httpx_client:Httpx_Client,ids_price:dict,houses_list_url,zone_URL,dao):
    """
    Parameters
    ----------
    httpx_client: Scraping session.

    ids_price (Dict): Dictionary of IDs using get_housesId_from_page from the page we are going to download.

    houses_list_url (str): The URL of the page where houses are located.

    url_zone (str): The URL of the zone.

    dao: House Dao DB Manager

    Returns
    -------
    [{'id': house.id, 'price': price, 'date': date, 'status': Db_save_state}]
    []: If no house has been added.
    None: If there are errors.
    """
    house_attempts = 0
    results = []
    ids = list(ids_price.keys()) 
    random.shuffle(ids)
    for id in ids:
        if id is None:
            continue
        price =  dao.find_house_last_price_by_id(id)
        house = dao.find_houses_by_id(id)
        if house is not None and price.price == ids_price[id]:
            # The ID is in the database, and the price is the same.
            dao.update_ad_state(id,True)  
            results.append({'id': id, 'price': price.price, 'date': price.date,'status':Db_save_state.house_and_price_duplicated})
            continue
        house_url = URL_MAIN_HOUSE_IDEALISTA + f"/{id}/"
        print("Downloading: " + house_url)
        html = httpx_client.get_html_from_url(house_url,houses_list_url)
        if html is None:
            print("Error downloading house")
            results.append({'id': id, 'price': None, 'date': None,'status':Db_save_state.error})
            house_attempts +=1
            if house_attempts == 3:
                print("Possible connection loss")
                return None
            continue
        single_house_soup = bs(html, 'html.parser')
        if "alquiler" in houses_list_url:
            operation =  OperationType.rent
        else:
            operation =  OperationType.sale
        result = parser_and_save_house_id(single_house_soup,id,operation,zone_URL,dao)
        print(f"Result:  {result}")
        results.append(result)
        if result['status'] == Db_save_state.error:
            house_attempts +=1
        else:
            house_attempts = 0 
    return results

