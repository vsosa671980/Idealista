import os
import sys
# get current directory
path = os.path.dirname(__file__)
# parent directory
parent = os.path.dirname(path)
grandParent = os.path.dirname(parent)
# appending a path
sys.path.append(grandParent)
#TODO: quitar lo de arriba en produccion
from scrapping_app.scrapping.get_zones import get_zones_from_aera
from scrapping_app.scrapping.single_zone_all_pages_houses import get_and_save_houses_from_single_zone
from db_app.data_base.dao import Db_save_state
from scrapping_app.scrapping.error_logger import log_error

def get_and_save_results_from_zones(zones,httpx_client,previous_url,house_dao):
    """
    for loop for downloading all the houses from zones list

    Parameters
    ----------
    zones:[] url zones to be downloaded
    httpx_client(req_html): httpx session
    previous_url: Previous URL to create the header and simulate human-like usage
    house_dao: Data Base Conection

    Return
    ------
    results:[] list with all the houses downloaded and their state
    """
    # List to check that everything is going well and to save the results
    results = []
    errors = 0
    if len(zones):
        for zone in zones:
            # From each subzone, we download the houses and their features
            newResults = get_and_save_houses_from_single_zone(httpx_client,zone,previous_url,house_dao)
            results = results + newResults[0]
            if not  newResults[1]:
                errors += 1
            else:
                errors = 0
            if errors == 2:
                log_error(f'connection loss')
                break
            previous_url = zone
    return results

def get_and_save_houses_from_zones(httpx_client,zones,previous_url,house_dao):
    """
    use get_and_save_results_from_zones and then print the results depending on the status

    Parameters
    ----------
    zones:[] url zones to be downloaded
    httpx_client(req_html): httpx session
    previous_url: Previous URL to create the header and simulate human-like usage
    house_dao: Data Base Conection

    Return
    ------
    results:[] list with all the houses downloaded and their state
    """
    # Once all the URLs of possible subzones for the entire area are downloaded
    results = get_and_save_results_from_zones(zones,httpx_client,previous_url,house_dao)
    for status in Db_save_state:
        # Print OK results and KO results
        print(Db_save_state(status).name)
        r = [int(obj["id"]) for obj in results if obj["status"] == status]
        print(r)
        print(f'{len(r)} resultados con status {Db_save_state(status).name}')
     #TODO: GUARDAR RESULTADOS EN txt
    return results
        
def get_and_save_houses_from_all_zones(httpx_client,area_url,previous_url,house_dao,zones_from_db):
    """
    Main function that first looks for all the subzones of the desired area,
    and then searches for all the houses in each subzone.

    Parameters
    ----------
        httpx_client(req_html.Httpx_client): httpx session
        area_url: URL of the entire area or zone where we want to search for houses
        previous_url: Previous URL to create the header and simulate human-like usage
        house_dao: Data Base Conection
        zones_from_db: get_zones_from_data_base or from idealista directly
        
    Return
    ------
    results:[] list with all the houses downloaded and their state
    """
    # Searching for all the subzones
    if zones_from_db:
        zones = house_dao.get_zones_from_data_base()
    else:
        zones = get_zones_from_aera(httpx_client,area_url,previous_url)
    # Once all the URLs of possible subzones for the entire area are downloaded
    results = get_and_save_houses_from_zones(zones,httpx_client,previous_url,house_dao)
    return results
    
 
