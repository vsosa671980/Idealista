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
from bs4 import BeautifulSoup as bs
from scrapping_app.scrapping.config import URL_MAIN_IDEALISTA
from scrapping_app.scrapping.error_logger import log_error
import pandas as pd

def get_zones_from_aera(httpx_client,next_url,previous_url):
    """
    Function that searches for all the subzones of the area we want, in the form of URLs

    Parameters
    ----------
        httpx_client(req_html.Httpx_client): httpx session
        next_url: URL of the entire area or zone we want to search for houses
        previous_url: Previous URL to create the header and simulate human-like usage

    Return
    ------
        [zone_urls]: List with all the URLs of the subzones in the entire area we want to download,
                that can no longer be further divided into subzones
        [next_url]: List with only the URL we want to download the subzones from, as there has been an error
    """
    print(f"Downloading Zones URLs from: {next_url}")
    try:
        html = httpx_client.get_html_from_url(next_url,previous_url)
        # TODO: CHEQUEAR RESPONSE PARA COMPROBAR QUE SE HA DESCARGADO BIEN, O QUE HA HECHO REDIRECT, O SI ENTRÓ EL CATCH
        # TODO: En casos como agaete hay una particularidad de municipio, que hace que o se busque bien y se conforme con el anterior
        if html:
            # We obtain with BeautifulSoup the soup of the HTML page
            area_soup = bs(html, 'html.parser')
            # We look for the dropdown menu of the zone, which indicates more subzones
            zones_soup = area_soup.find("ul",{"class":"breadcrumb-dropdown-subitem-list"})
            zones_urls = []
            if zones_soup:
                # Now we search for the list of subzones
                dropdown_soup = zones_soup.find_all("li",{"class":"breadcrumb-dropdown-subitem-element-list"})
                # We will save the number of houses for each URL
                for zone_soup in dropdown_soup:
                    # For each option in the dropdown
                    zone_URL = zone_soup.find("a").get("href")
                    url = URL_MAIN_IDEALISTA + zone_URL
                    print(f"Downloading subzones from: {url}")
                    try:
                        # Since thousands are indicated with a dot, we replace it with nothing
                        number_houses = int(zone_soup.find("span").text.replace('.',''))
                    except:
                        number_houses = 0
                    if number_houses > 0:
                        try:
                            # If this zone has houses, we will check if it has more subzones within it,
                            # Using recursion with this same function
                            # It's like traversing the branches of a tree.
                            # In this case, we are coming from the page of the previous zone 
                            # and moving on to the next subzone
                            zones_urls = zones_urls + list(dict.fromkeys(get_zones_from_aera(httpx_client,url,next_url)))
                        except:
                            print(f"Added: {url} houses:{number_houses}")
                            zones_urls.append((url,number_houses))
                    else:
                        print(f"Added: {url}")
                        zones_urls.append((url,number_houses))
            else:
                number_houses = int(area_soup.find("h1",{"id":"h1-container"}).text.split()[0])
                zones_urls.append((next_url,number_houses))
            return zones_urls
        return []
    except Exception as e:
        log_error(f'(get_zones.py) Error Getting Zones from area {next_url}: {e}')
    return []
    

