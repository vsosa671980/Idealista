# coding: utf-8
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
import scrapping_app.scrapping.single_house_aux as aux
import json
from datetime import datetime
#from django.utils import timezone
 #TODO: Pendiente time utc de django
import db_app.data_base.model as mod
from db_app.data_base.dao import Db_save_state
from scrapping_app.scrapping.error_logger import log_error

def parser_house_id(single_house_soup,id,operation,zone_url):
    """
    Get all single  house data from idealista.

    Parameters
    ----------
    single_house_soup: bs element from html single house
    id: id house from idealista
    operation: FROM CONFIG.PY rent or sale
    zone_url: House´s Zone

    Return
    ------
    {'id':id, 'active' : True, 'last_active_check_date' : datetime.now(),
            'post_time':datetime.fromtimestamp(postTime), 'operation':operation,'title':title,
            'is_penthouse' : is_penthouse,'is_duplex' : is_duplex,'is_flat': is_flat,'is_studio' : is_studio,
            'is_apartment' : is_apartment,'is_loft' : is_loft,'is_ground_floor' : is_ground_floor,'is_semi_detached_house' : is_semi_detached_house,
            'is_townhouse' : is_townhouse,'is_bungalow' : is_bungalow, 
            'is_country_house' : is_country_house,'is_large_country_house' : is_large_country_house,'is_villa' : is_villa,
            'is_terraced_house' : is_terraced_house, 'rooms_number': rooms_number,'baths_number': baths_number,
            'floors': floors, 'floor_number': floor_number,
            'built_area': built_area, 'usable_area': usable_area, 'constructed_area': constructed_area,
            'built_year': built_year, 'plot_area': plot_area,
            'has_lift': has_lift, 'has_parking':has_parking,'has_garden': has_garden,
            'has_swimming_pool': has_swimming_pool, 'has_terrace': has_terrace,
            'has_fitted_wardrobes': has_fitted_wardrobes, 'has_storage_room': has_storage_room,
            'has_balcony': has_balcony,
            'is_new_development': is_new_development, 'is_needs_renovation': is_needs_renovation,
            'is_good_condition': is_good_condition ,
            'latitude': latitude, 'longitude': longitude, 
            'location_1': location_1, 'location_2':location_2, 
            'location_3': location_3, 'location_4': location_4,
            'zone_url':zone_url, 
            'price': price, 'date':datetime.now(),'status' : Db_save_state.pending}

    or 

    {'id': id, 'price': None, 'date': None,'status':Db_save_state.error}: in case of error 
    
    """
    errors = 0

    title,new_error = aux.extract_title(single_house_soup)
    errors += new_error

    description,new_error = aux.extract_description(single_house_soup)
    errors += new_error
    is_penthouse = aux.check_keywords_in_text(title + description, ["ático", "última planta","atico"])
    is_duplex = aux.check_keywords_in_text(title + description, ["dúplex", "duplex"])
    is_flat = aux.check_keywords_in_text(title, ["piso"])
    is_studio = aux.check_keywords_in_text(title + description, ["estudio"])
    is_apartment = aux.check_keywords_in_text(title + description, ["apartamento"])
    is_loft = aux.check_keywords_in_text(title + description, ["loft"])
    is_ground_floor = aux.check_keywords_in_text(title , ["bajo"])
    is_semi_detached_house = aux.check_keywords_in_text(title + description, ["chalet adosado"])
    is_townhouse = aux.check_keywords_in_text(title + description, ["chalet pareado"])
    is_bungalow = aux.check_keywords_in_text(title + description, ["bungallow"])
    is_country_house = aux.check_keywords_in_text(title + description, ["finca rustica"])
    is_large_country_house = aux.check_keywords_in_text(title, ["caserón"])
    is_villa = aux.check_keywords_in_text(title + description, ["villa"])
    is_terraced_house = aux.check_keywords_in_text(title + description, ["casa terrera", "casa rural"])
    latitude,longitude,new_error = aux.extract_coordinates(single_house_soup)
    errors += new_error

    basic_c,new_error = aux.extract_basic_caracts(single_house_soup)

    has_fitted_wardrobes = 'armarios empotrados' in basic_c
    has_storage_room = "trastero" in basic_c
    is_ground_floor = is_ground_floor or ("bajo" in basic_c)
    plot_area = None
    has_terrace = has_balcony = 0
    built_year = None
    built_area = usable_area =  None
    floors = floor_number = 1

    for item in basic_c:  
        try:
            if "construido en " in item:  
                built_year = int(item.split("construido en ")[1])
            if "parcela de " in item:  
                plot_area = float(item.split("parcela de ")[1].split()[0].replace(".",""))
            if "terraza" in item: 
                has_terrace = 1
            if "balcón" in item: 
                has_balcony = 1
            if "construidos" in item and "útiles" in item:
                built_area = float(item.split()[0].replace(".",""))
                usable_area = float(item.split()[3].replace(".",""))
            elif "útiles" in item: 
                usable_area = float(item.split()[0].replace(".",""))
            elif "construidos" in item:
                built_area = float(item.split()[0].replace(".",""))
            if "plantas" in item:
                floors = int(item.split()[0])
            if "planta" in item:
                try:
                    string = item.split()[1]
                    string = string[:-1]
                    floor_number = int(string)
                except:
                    floor_number = 0
            

        except Exception as e:
            log_error(f'(single_house.py) Error basic_c {e}')
            errors += 1
    
    location_1,location_2,location_3,location_4,error = aux.extract_location(single_house_soup)
    errors += error

    try:
        scripts = single_house_soup.find_all("script")
        for script in scripts:
            if "var utag_data" in str(script):
                data = json.loads(str(script).split("var utag_data =")[1].split(";")[0])
                break
    except Exception as e:
        log_error(f'(single_house.py) Error var utag_data {e}')
        errors += 1
        data = None
    try:
        rooms_number = int(data["ad"]["characteristics"]["roomNumber"])
    except:
        rooms_number = 0
    try:
        baths_number = int(data["ad"]["characteristics"]["bathNumber"])
    except:
        baths_number = 0
    try:
        has_lift = int(data["ad"]["characteristics"]["hasLift"])
    except:
        has_lift = 0
    try:
        has_parking = int(data["ad"]["characteristics"]["hasParking"])
    except:
        has_parking = 0
    try:
        has_garden = int(data["ad"]["characteristics"]["hasGarden"])
    except:
        has_garden = 0
    try:
        has_swimming_pool = int(data["ad"]["characteristics"]["hasSwimmingPool"])
    except:
        has_swimming_pool = 0
    try:
        has_terrace = int(data["ad"]["characteristics"]["hasTerrace"]) or has_terrace or has_balcony
    except:
        has_terrace = has_terrace or has_balcony 
    try:
        constructed_area = float(data["ad"]["characteristics"]["constructedArea"])
    except:
        constructed_area = None
    try:
        is_new_development=int(data["ad"]["condition"]["isNewDevelopment"])
        if (is_new_development == 1) and not built_year:
            built_year = 2022
    except:
        is_new_development = 0
    try:
        is_needs_renovation = int(data["ad"]["condition"]["isNeedsRenovating"])
    except:
        is_needs_renovation = 0
    try:
        is_good_condition = int(data["ad"]["condition"]["isGoodCondition"])
    except:
        is_good_condition = 0
    try:
        postTime = int(data['post']['time'])/1000 # Por tener formato javascript de 13 digitos
    except:
        postTime = None
    if plot_area!=None:
        has_garden = 1

    try:
         #TODO: Pendiente time utc de django
        price = int(single_house_soup.find("div",{"class":"info-data"}).find("span",{"class":"info-data-price"}).text.replace(".","").replace("€",""))
        return {'id':id, 'active' : True, 'last_active_check_date' : datetime.now(),
            'post_time':datetime.fromtimestamp(postTime), 'operation':operation,'title':title,
            'is_penthouse' : is_penthouse,'is_duplex' : is_duplex,'is_flat': is_flat,'is_studio' : is_studio,
            'is_apartment' : is_apartment,'is_loft' : is_loft,'is_ground_floor' : is_ground_floor,'is_semi_detached_house' : is_semi_detached_house,
            'is_townhouse' : is_townhouse,'is_bungalow' : is_bungalow, 
            'is_country_house' : is_country_house,'is_large_country_house' : is_large_country_house,'is_villa' : is_villa,
            'is_terraced_house' : is_terraced_house, 'rooms_number': rooms_number,'baths_number': baths_number,
            'floors': floors, 'floor_number': floor_number,
            'built_area': built_area, 'usable_area': usable_area, 'constructed_area': constructed_area,
            'built_year': built_year, 'plot_area': plot_area,
            'has_lift': has_lift, 'has_parking':has_parking,'has_garden': has_garden,
            'has_swimming_pool': has_swimming_pool, 'has_terrace': has_terrace,
            'has_fitted_wardrobes': has_fitted_wardrobes, 'has_storage_room': has_storage_room,
            'has_balcony': has_balcony,
            'is_new_development': is_new_development, 'is_needs_renovation': is_needs_renovation,
            'is_good_condition': is_good_condition ,
            'latitude': latitude, 'longitude': longitude, 
            'location_1': location_1, 'location_2':location_2, 
            'location_3': location_3, 'location_4': location_4,
            'zone_url':zone_url, 
            'price': price, 'date':datetime.now(),'status' : Db_save_state.pending}
            #TODO: Posttime  chequear en idealista
    except Exception as e:
        log_error(f'(single_house.py) Error creating return {e}')
    return {'id': id, 'price': None, 'date': None,'status':Db_save_state.error}


def parser_and_save_house_id(single_house_soup,id,operation,zone_url,dao):
    """
    Using parser_house_id(single_house_soup,id,operation,zone_url) it get all single  house data
    from idealista.

    Parameters
    ----------
    single_house_soup: bs element from html single house
    id: id house from idealista
    operation: FROM CONFIG.PY rent or sale
    zone_url: House´s Zone
    dao: db manager

    Return
    ------
    dao.add_house(new_house,new_price.price,new_price.date)

    or 

    house: in case of error from parser_house_id(single_house_soup,id,operation,zone_url) -> {'id': id, 'price': None, 'date': None,'status':Db_save_state.error}
    """
    house = parser_house_id(single_house_soup,id,operation,zone_url)
    if house['status'] == Db_save_state.pending:
        #TODO: Pendiente time utc de django
        new_house = mod.House(id=house['id'], active = house['active'], last_active_check_date = datetime.now(),
                post_time=  house['post_time'], operation=house['operation'],title=house['title'],
                is_penthouse = house['is_penthouse'],is_duplex = house['is_duplex'],
                is_flat = house['is_flat'],is_studio = house['is_studio'],
                is_apartment = house['is_apartment'],is_loft = house['is_loft'],
                is_ground_floor = house['is_ground_floor'],is_semi_detached_house = house['is_semi_detached_house'],
                is_townhouse = house['is_townhouse'],is_bungalow = house['is_bungalow'],
                is_country_house = house['is_country_house'],is_large_country_house = house['is_large_country_house'],
                is_villa = house['is_villa'],is_terraced_house = house['is_terraced_house'],
                rooms_number= house['rooms_number'], baths_number= house['baths_number'],
                floors= house['floors'], floor_number= house['floor_number'],
                built_area= house['built_area'], usable_area= house['usable_area'],
                constructed_area= house['constructed_area'], built_year= house['built_year'],
                plot_area= house['plot_area'],
                has_lift= house['has_lift'], has_parking= house['has_parking'],
                has_garden= house['has_garden'], has_swimming_pool= house['has_swimming_pool'],
                has_terrace= house['has_terrace'], has_fitted_wardrobes= house['has_fitted_wardrobes'],
                has_storage_room= house['has_storage_room'], has_balcony= house['has_balcony'], 
                is_new_development= house['is_new_development'], is_needs_renovation= house['is_needs_renovation'], 
                is_good_condition= house['is_good_condition'],
                latitude= house['latitude'], longitude= house['longitude'], 
                location_1= house['location_1'], location_2= house['location_2'],
                location_3= house['location_3'], location_4= house['location_4'],
                zone_url=zone_url
                ) 
        #TODO: Posttime   datetime.fromtimestamp(Posttime)
        new_price = mod.Price(price=house['price'],
                        date=house['date'])  
       #TODO: Posttime   datetime.fromtimestamp(Posttime)
        return dao.add_house(new_house,new_price.price,new_price.date)
    return house

