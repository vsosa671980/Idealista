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
from scrapping_app.scrapping.error_logger import log_error

def extract_text(element):
    """
    Extract text from bs element

    Parameters
    ----------
    element: bs element

    Return
    ------
    text
    """
    try:
        return element.text.lower() if element else ""
    except Exception as e:
        log_error(f' (single_house_aux.py) Error rextracting text {e}')
        return ""

def extract_title(single_house_soup):
    """
    Extract the title from bs element

    Parameters
    ----------
    single_house_soup: bs 

    Return
    ------
    text,error
    """
    try:
        return extract_text(single_house_soup.find("span",{"class":"main-info__title-main"})),0
    except Exception as e:
        log_error(f' (single_house_aux.py) Error rextracting title {e}')
        return "",1
        
        

def extract_description(single_house_soup):
    """
    Extract the description from bs element

    Parameters
    ----------
    single_house_soup: bs 

    Return
    ------
    text,error
    """
    try:
        return extract_text(single_house_soup.find("div",{"class":"comment"}).find("p")),0
    except Exception as e:
        return "",1

def check_keywords_in_text(text:str, keywords:str):
    """
    Check if the keword is in the text

    Parameters
    ----------
    text: str
    keywords: str

    Return
    ------
    Bool
    """
    try:
        return any(keyword in text for keyword in keywords)
    except Exception as e:
        log_error(f' (single_house_aux.py) Error checking keywords in text {e}')
        return None
    
def extract_coordinates(single_house_soup):
    """
    extract from bs  element the house coordinates

    Parameters
    ----------
    single_house_soup:bs 

    Return
    ------
    (latitude number,longitude,number of errors)
    """
    try:
        scripts = single_house_soup.find_all("script")
        for script in scripts:
            if "var config" in str(script):
                break
        latitude = float(str(script).split('latitude')[1].split(',')[0].split()[1].replace("'",""))
        longitude = float(str(script).split('latitude')[1].split(',')[1].strip().split()[1].replace("'",""))
        return latitude, longitude, 0
    except Exception as e:
        log_error(f' (single_house_aux.py) Error extracting coordinates {e}')
        return None, None, 1
    
def extract_basic_caracts(single_house_soup):
    """
    extract from bs  element the house basic caracteristics

    Parameters
    ----------
    single_house_soup:bs 

    Return
    ------
    [c_basicas]
    """
    try:
        c1 = single_house_soup.find("section",{"id":"details"}).find("div",{"class":"details-property-feature-one"}).find_all("li")
        return [caract.text.strip().lower() for caract in c1],0
    except Exception as e:
        log_error(f' (single_house_aux.py) Error extracting basic caracts {e}')
        return [],1

def extract_location(single_house_soup):
    """
    extract from bs  element the house location, city, municipy...

    Parameters
    ----------
    single_house_soup:bs 

    Return
    ------
    (location_1,location_2,location_3,location_4,number of errors)
    """
    error=0
    try:
        location = single_house_soup.find('div',{'id':'headerMap'})
        location = [zone.text.strip() for zone in location.find_all('li')]
    except Exception as e:
        log_error(e)
        error += 1
        location = []
    try:
        location_1 = location[-1]
    except :
        
        location_1 = None
    try:
        location_2 = location[-2]
        if  location_2 == "":
            location_2 = location_1
    except :
       
        location_2 = location_1
    try:
        location_3 = location[-3]
        if  location_3 == "":
            location_3 = location_2
    except :
        
        location_3 = location_2
    try:
        location_4 = location[-4]
        if  location_4 == "":
            location_4 = location_3
    except :
       
        location_4 = location_3
    return location_1,location_2,location_3,location_4,error

