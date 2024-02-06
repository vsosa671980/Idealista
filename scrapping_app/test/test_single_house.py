import pytest
from scrapping_app.scrapping.req_html import  open_html_file, Httpx_Client
from scrapping_app.scrapping.single_house import  parser_house_id, parser_and_save_house_id
from scrapping_app.scrapping.config import OperationType, URL_MAIN_IDEALISTA, URL_GOOGLE, TEST_DATABASE_NAME
from bs4 import BeautifulSoup as bs
from db_app.data_base.dao import HouseDao, Base, Db_save_state

import os
# pytest --collect-only

def soup_online_from_id(id):
    session = Httpx_Client("idealista")
    # comenzamos viniendo de google y abrimos sesión abriendo la página de idealista.
    previous_url = URL_GOOGLE
    next_url = URL_MAIN_IDEALISTA
    html = session.get_html_from_url(next_url,previous_url)
    # Hariamos una primera busqueda de la zona y nos aparece el mapa viniendo de idealista.com.
    previous_url = next_url
    house_url = f"https://www.idealista.com/inmueble/{id}/"
    #house_url = "https://www.idealista.com/inmueble/101985304/"
    html = session.get_html_from_url(house_url,previous_url)
    soup = bs(html, 'html.parser')
    session.session.close()
    return soup

class Helpers:

    house_testers=[ 

            {'id':0, 'active' : True, # last_active_check_date, post_time
            'operation':1,'title':'piso en venta en calle lomo la plana, 26',
            'is_penthouse' : True, 'is_duplex' : False,'is_flat': True,'is_studio' : False,
            'is_apartment' : False,'is_loft' : False,'is_ground_floor' : False,
            'is_semi_detached_house' : False,'is_townhouse' : False,'is_bungalow' : False,
            'is_country_house' : False,'is_large_country_house' : False,
            'is_villa' : True,'is_terraced_house' : False,
            'rooms_number': 3, 'baths_number': 2,
            'floors': 1, 'floor_number': 5,
            'built_area': 95.0, 'usable_area': None, 'constructed_area': 95.0,
            'built_year': None, 'plot_area': None,
            'has_lift': 1, 'has_parking':1,
            'has_garden': 1, 'has_swimming_pool': 1, 'has_terrace': 0,
            'has_fitted_wardrobes': True, 'has_storage_room': False,
            'has_balcony': 0,
            'is_new_development': 0, 'is_needs_renovation': 0,
            'is_good_condition': 1 ,
            'latitude': 28.099291, 'longitude': -15.4529486,  
            'location_1': 'Gran Canaria, Las Palmas', 
            'location_2':'Las Palmas de Gran Canaria', 
            'location_3': 'Distrito Ciudad Alta',
            'location_4': 'Barrio Siete Palmas',
            'zone_url':'test_url', 
            'price': 288000,'status' : 5},

            {'id':1, 'active' : True, # last_active_check_date, post_time
            'operation':1,'title':' chalet adosado en venta en avenida juan carlos i, 5',
            'is_penthouse' : False, 'is_duplex' : False,'is_flat': False,'is_studio' : False,
            'is_apartment' : False,'is_loft' : False,'is_ground_floor' : False,
            'is_semi_detached_house' : True,'is_townhouse' : False,'is_bungalow' : False,
            'is_country_house' : False,'is_large_country_house' : False,
            'is_villa' : False,'is_terraced_house' : False,
            'rooms_number': 4, 'baths_number': 3,
            'floors': 2, 'floor_number': 0,
            'built_area':286.0, 'usable_area': None, 'constructed_area': 286.0,
            'built_year': 2022, 'plot_area': None,
            'has_lift': 0, 'has_parking':1,
            'has_garden': 1, 'has_swimming_pool': 1, 'has_terrace': 0,
            'has_fitted_wardrobes': True, 'has_storage_room': False,
            'has_balcony': 0,
            'is_new_development': 1, 'is_needs_renovation': 0,
            'is_good_condition': 0 ,
            'latitude': 28.1176036, 'longitude': -15.4446137,  
            'location_1': 'Gran Canaria, Las Palmas', 
            'location_2':'Las Palmas de Gran Canaria', 
            'location_3': 'Distrito Ciudad Alta',
            'location_4': 'Barrio Siete Palmas',
            'zone_url':'test_url', 
            'price': 1425000,'status' : 5},

            {'id':2, 'active' : True, # last_active_check_date, post_time
            'operation':1,'title':' chalet pareado en venta en calle hoya del enamorado, 127',
            'is_penthouse' : False, 'is_duplex' : False,'is_flat': False,'is_studio' : False,
            'is_apartment' : False,'is_loft' : False,'is_ground_floor' : False,
            'is_semi_detached_house' : False,'is_townhouse' : True,'is_bungalow' : False,
            'is_country_house' : False,'is_large_country_house' : False,
            'is_villa' : False,'is_terraced_house' : False,
            'rooms_number': 5, 'baths_number': 4,
            'floors': 3, 'floor_number': 0,
            'built_area':215.0, 'usable_area': 175.0, 'constructed_area': 215.0,
            'built_year': None, 'plot_area': None,
            'has_lift': 0, 'has_parking':1,
            'has_garden': 0, 'has_swimming_pool': 0, 'has_terrace': 1,
            'has_fitted_wardrobes': True, 'has_storage_room': True,
            'has_balcony': 0,
            'is_new_development': 0, 'is_needs_renovation': 0,
            'is_good_condition': 1,
            'latitude': 28.1013327, 'longitude': -15.4498641,  
            'location_1': 'Gran Canaria, Las Palmas', 
            'location_2':'Las Palmas de Gran Canaria', 
            'location_3': 'Distrito Ciudad Alta',
            'location_4': 'Barrio Siete Palmas',
            'zone_url':'test_url', 
            'price': 430000,'status' : 5},

            {'id':3, 'active' : True, # last_active_check_date, post_time
            'operation':1,'title':'piso en venta en avenida pintor felo monzón s/n',
            'is_penthouse' : True, 'is_duplex' : False,'is_flat': True,'is_studio' : False,
            'is_apartment' : False,'is_loft' : False,'is_ground_floor' : False,
            'is_semi_detached_house' : False,'is_townhouse' : False,'is_bungalow' : False,
            'is_country_house' : False,'is_large_country_house' : False,
            'is_villa' : False,'is_terraced_house' : False,
            'rooms_number': 3, 'baths_number': 2,
            'floors': 1, 'floor_number': 2,
            'built_area':103.0, 'usable_area': 75.0, 'constructed_area':103.0,
            'built_year': 2022, 'plot_area': None,
            'has_lift': 1, 'has_parking':1,
            'has_garden': 0, 'has_swimming_pool': 1, 'has_terrace': 1,
            'has_fitted_wardrobes': False, 'has_storage_room': True,
            'has_balcony': 0,
            'is_new_development': 1, 'is_needs_renovation': 0,
            'is_good_condition': 0,
            'latitude': 28.1024396, 'longitude': -15.4532376,  
            'location_1': 'Gran Canaria, Las Palmas', 
            'location_2':'Las Palmas de Gran Canaria', 
            'location_3': 'Distrito Ciudad Alta',
            'location_4': 'Barrio Siete Palmas',
            'zone_url':'test_url', 
            'price': 268000,'status' : 5}
            ]
   
    @staticmethod
    def assert_house(house_from_html,number_house):
        """
        Auxiliar que comprobará todas las claves de los diccionarios de las casas
        para ver que corresponden con lo que lee la funcionparser_house_id 
        del archivo single_house.py
        """
        house = Helpers.house_testers[number_house]
        for key in list(house.keys()):
            if key in ['fecha','fecha_ultimo_check_activo']:
                continue
            assert house_from_html.get(key) == house.get(key)
        
@pytest.fixture
def helpers():
    return Helpers

@pytest.fixture(scope='module')
def db_conn():
    dao = HouseDao(TEST_DATABASE_NAME)
    # Eliminar tablas de la base de datos de prueba
    Base.metadata.drop_all(dao.engine)
    Base.metadata.create_all(dao.engine)
    return dao

@pytest.fixture
def test_soups():
    """
    Lee los cuatro archivos html de casas de test
    
    RETURN
    ------
    [soup]: Lista de las 4 html ya procesados por bs

    """
    soups=[]
    for i in range(4):
        try:
            test_path = os.path.dirname(__file__)
            filename=f'{test_path}/casa_{i}_test_html.text'
            html = open_html_file(filename)
            soup = bs(html, 'html.parser')
            soups.append(soup)
        except Exception as e:
            print(e)
    return soups

def test_offline_read_tester_soups(test_soups,helpers):
    """
    We assume that Idealista has not changed its format. This test
    only checks the format of the already downloaded HTML files.
    Starting from houses previously downloaded with their HTML in text files:
        casa_0_test_html.txt
        casa_1_test_html.txt
        casa_2_test_html.txt
        casa_3_test_html.txt
    It tests that the parser_house_id function in the single_house.py file correctly reads
    the soup file and returns a valid dictionary according to the house.
    """
    soups = test_soups
    assert len(soups) == 4
    for i,soup in enumerate(soups):
        house = parser_house_id(soup,i,OperationType.sale,'test_url')
        helpers.assert_house(house,i)

def test_parser_and_save_house_id_offline(test_soups,db_conn):
    soups = test_soups
    for i,soup in enumerate(soups):
        house = parser_and_save_house_id(soup,i,OperationType.sale,'test_url',db_conn)
        assert house['id'] == i
        assert house['status'] == Db_save_state.new_house_added
        house_db=db_conn.find_houses_by_id(i)
        assert house_db.id == i


