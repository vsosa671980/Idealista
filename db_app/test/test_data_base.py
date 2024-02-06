import pytest
from db_app.data_base.dao import HouseDao, Base, Db_save_state
from db_app.data_base.model import House, Price
from datetime import datetime
import pandas as pd
from scrapping_app.scrapping.config import TEST_DATABASE_NAME
# pytest --collect-only

def create_house(id,price,date):
    data = pd.Series({'id': id,'active':True, 'last_active_check_date':date, 
        'post_time': date,'operation':1, 'title': "1",
        "is_penthouse":1, "is_duplex" :0, "is_flat" : 0, "is_studio" : 0, "is_apartment" : 0, "is_loft" : 0,
        "is_ground_floor" : 0, "is_semi_detached_house" : 0, "is_townhouse" : 0, "is_bungalow" : 0, 
        "is_country_house" : 0, "is_large_country_house" : 0, "is_villa" : 0, "is_terraced_house" : 0,
        'rooms_number':3, 'baths_number': 2, 'floors':1, 'floor_number':4,
        'built_area':40.3,'usable_area':39.3, 'constructed_area': 50.1, 'built_year': 2019, 
        'plot_area': None, 'has_lift': True, 'has_parking': False, 'has_garden': False, 
        'has_swimming_pool': 1, 'has_terrace':0, 'has_fitted_wardrobes': 1, 'has_storage_room': 0,
        'has_balcony':False, 'is_new_development': False, 'is_needs_renovation':False,
        'is_good_condition':True, 'latitude': "1111", 'longitude':"1111", 
        'location_1': "1111",'location_2': "1111", 'location_3': "1111", 
        'location_4': "1111", 'zone_url':"1111", 
        'price':price, 'date': date })
    new_house = House(id=data['id'],active=data['active'],last_active_check_date=datetime.now(), 
        post_time= datetime.now(), operation=data['operation'],title=data['title'],
        is_penthouse = data['is_penthouse'],is_duplex = data['is_duplex'],is_flat = data['is_flat'],is_studio = data['is_studio'],
        is_apartment = data['is_apartment'],is_loft = data['is_loft'],is_ground_floor = data['is_ground_floor'],
        is_semi_detached_house = data['is_semi_detached_house'], is_townhouse = data['is_townhouse'],
        is_bungalow = data['is_bungalow'], is_country_house = data['is_country_house'],
        is_large_country_house = data['is_large_country_house'], is_villa = data['is_villa'],
        is_terraced_house = data['is_terraced_house'], rooms_number =  data['rooms_number'],
        baths_number = data['baths_number'], floors =  data['floors'], floor_number = data['floor_number'],
        built_area = data['built_area'],  usable_area = data['usable_area'], constructed_area = data['constructed_area'],
        built_year = data['built_year'], plot_area = data['plot_area'], has_lift = data['has_lift'],
        has_parking = data['has_parking'], has_garden = data['has_garden'], has_swimming_pool = data['has_swimming_pool'],
        has_terrace = data['has_terrace'], has_fitted_wardrobes = data['has_fitted_wardrobes'], 
        has_storage_room = data['has_storage_room'], has_balcony = data['has_balcony'], 
        is_new_development = data['is_new_development'], is_needs_renovation = data['is_needs_renovation'], 
        is_good_condition = data['is_good_condition'], latitude = data['latitude'], longitude = data['longitude'], 
        location_1 = data['location_1'], location_2 = data['location_2'], location_3 = data['location_3'],
        location_4 = data['location_4'], zone_url = data['zone_url']
       ) 
    new_price = Price(price=data['price'], date=datetime.fromtimestamp(data['date']))
    return new_house,new_price

@pytest.fixture(scope='module')
def test_session():
    data_Base = HouseDao(TEST_DATABASE_NAME)
    # Eliminar tablas de la base de datos de prueba
    Base.metadata.drop_all(data_Base.engine)
    Base.metadata.create_all(data_Base.engine)
    return data_Base

def test_add_house_and_delete(test_session):
    """
    This test function adds and removes a house and
    its associated price from a database.
    """
     # Se crea una referencia a la base de datos de prueba.
    data_Base = test_session
    # Se crea una casa y su precio utilizando la función "crear_casa".
    house, price = create_house(1, 1200, 1676933183.260)
    # Se agrega la casa y su precio a la base de datos.
    result = data_Base.add_house(house, price.price, price.date)
    # Comprobación de que la casa se ha creado correctamente.
    housedb = data_Base.session.get(House, house.id)
    assert result['status'] == Db_save_state.new_house_added
    assert housedb is not None
    assert housedb.rooms_number == house.rooms_number
    assert housedb.title == house.title
    # Comprobación de que el precio se ha creado correctamente.
    assert len(housedb.prices) == 1
    assert housedb.prices[0].price == price.price
    assert housedb.prices[0].date == price.date
    # Se comprueba que el precio se ha guardado correctamente en la base de datos.
    pricedb = data_Base.session.query(Price).filter_by(date=price.date).filter_by(house_id=house.id).first()
    assert pricedb.date == price.date
    assert pricedb.price == price.price
    assert pricedb.house_id == housedb.id
    # Se elimina la casa de la base de datos utilizando su ID.
    data_Base.delete_house_by_id(housedb.id)
    # Se comprueba que la casa y el precio asociado han sido eliminados de la base de datos.
    assert data_Base.session.query(House).count() == 0
    assert data_Base.session.query(Price).count() == 0

def test_find_houses_by_id(test_session):
    """
    Esta función de prueba busca casas en la base de datos por su ID.
    """
    # Se crea una referencia a la base de datos de prueba.
    data_Base = test_session
    # Se crea una casa y su precio utilizando la función "crear_casa".
    house, price = create_house(1, 1200, 1676933183.260)
    # Se agrega la casa y su precio a la base de datos.
    result = data_Base.add_house(house, price.price, price.date)
    assert result['status'] == Db_save_state.new_house_added
    # Se comprueba que la función "find_houses_by_id" devuelve correctamente la casa.
    assert data_Base.find_houses_by_id(house.id).id == house.id
    # Se comprueba que la función "find_houses_by_id" devuelve "None" para un ID no existente.
    assert data_Base.find_houses_by_id(8) == None
    # Se comprueba que la función "find_houses_by_id" devuelve "None" para un ID no válido.
    assert data_Base.find_houses_by_id("9") == None
    # Se elimina la casa de la base de datos utilizando su ID.
    data_Base.delete_house_by_id(house.id)
    # Se comprueba que la casa y el precio asociado han sido eliminados de la base de datos.
    assert data_Base.session.query(House).count() == 0
    assert data_Base.session.query(Price).count() == 0

def test_delete_house_by_id(test_session):
    """
    Esta función de prueba elimina casas de la base de datos por su ID.
    """
     # Se crea una referencia a la base de datos de prueba.
    data_Base = test_session
    # Se crea una casa y su precio utilizando la función "crear_casa".
    house, price= create_house(1, 1200, 1676933183.260)
    # Se agrega la casa y su precio a la base de datos.
    result = data_Base.add_house(house, price.price, price.date)
    assert result['status'] == Db_save_state.new_house_added
    # Se comprueba que la función "delete_house_by_id" devuelve un resultado correcto para un ID no existente.
    assert data_Base.delete_house_by_id("8") == ("8", False)
    # Se comprueba que la función "delete_house_by_id" devuelve un resultado correcto para un ID no válido.
    assert data_Base.delete_house_by_id(8) == (8, False)
    # Se elimina la casa de la base de datos utilizando su ID y se comprueba que la función devuelve un resultado correcto.
    assert data_Base.delete_house_by_id(house.id) == (1, True)
    # Se comprueba que la casa ya ha sido eliminada de la base de datos y que la función devuelve un resultado correcto para una casa ya eliminada.
    assert data_Base.delete_house_by_id(1) == (1, False)

def test_filter_houses(test_session):
    """
    Esta función de prueba comprueba la funcionalidad de filtrado de casas.
    """
     # Se crea una referencia a la base de datos de prueba.
    data_Base = test_session
    # Se crean dos casas y sus respectivos precios utilizando la función "crear_casa".
    house, price = create_house(1, 1200, 1676933183.260)
    house2, price2 = create_house(2, 1300, 1676933185.260)
    # Se agregan las casas y sus precios a la base de datos.
    result = data_Base.add_house(house, price.price, price.date)
    assert result['status'] == Db_save_state.new_house_added
    result2 = data_Base.add_house(house2, price2.price, price2.date)
    assert result2['status'] == Db_save_state.new_house_added
    # Se comprueba que la función de filtrado devuelve una lista vacía para una búsqueda inválida.
    assert data_Base.filter_houses(rooms_number=3, has_parking=True) == []
    # Se comprueba que la función de filtrado devuelve una lista con dos elementos para una búsqueda por número de habitaciones y sin aparcamiento.
    assert len(data_Base.filter_houses(rooms_number=3, has_parking=False)) == 2
    # Se comprueba que la función de filtrado devuelve "None" para una búsqueda inválida.
    assert data_Base.filter_houses(whatever=3, has_parking=False) == None
    # Se comprueba que la función de filtrado devuelve una lista con la misma cantidad de elementos que hay en la base de datos para una búsqueda vacía.
    assert len(data_Base.filter_houses()) == data_Base.session.query(House).count()

def test_create_houses_same_id_different_price_and_date(test_session):
    """
    Prueba que se pueda agregar una casa con el mismo ID pero diferente precio y fecha a la base de datos.
    """
    data_Base = test_session
    # Eliminar tablas de la base de datos de prueba
    data_Base.session.query(House).delete()
    data_Base.session.query(Price).delete()
    # Se eliminan todas las casas y precios existentes en la base de datos de prueba para comenzar con una base de datos vacía.
    # Crear dos casas con el mismo ID pero diferentes precios y fechas
    house2,price2 = create_house(2,1200,1676933183.260)
    house3,price3 = create_house(2,1300,1676933185.260)
    # Agregar las casas a la base de datos
    result1 = data_Base.add_house(house2,price2.price,price2.date)
    result2 = data_Base.add_house(house3,price3.price,price3.date)
    # Verificar que la casa y su precio fueron agregados correctamente
    assert result1['status'] == Db_save_state.new_house_added
    assert result2['status'] == Db_save_state.new_price_added
    housedb = data_Base.session.query(House).filter_by(id=house2.id).first()
    assert len(housedb.prices) == 2
    prices_db = sorted(housedb.prices, key=lambda price: price.date)
    assert prices_db[0].price == price2.price
    assert prices_db[0].date == price2.date
    assert prices_db[1].price == price3.price
    assert prices_db[1].date == price3.date
    # Limpiar la base de datos de prueba
    data_Base.delete_house_by_id(house2.id)
    assert data_Base.session.query(House).count() == 0
    assert data_Base.session.query(Price).count() == 0


def test_create_house_same_id_same_price_and_date(test_session):
    """
    Prueba que al agregar varias casas con el mismo ID, precio y fecha a la base de datos,
    no da problemas
    """
    # Se inicializa la base de datos de prueba
    data_Base = test_session
    # Eliminar tablas de la base de datos de prueba
    data_Base.session.query(House).delete()
    data_Base.session.query(Price).delete()
    # Se eliminan todas las casas y precios existentes en la base de datos
    # de prueba para comenzar con una base de datos vacía.
    house4,price4 = create_house(4,1300,1676933185.260)
    # Se crea una casa y un precio con id, precio y fecha iguales y se agregan a la base de datos de prueba tres veces
    result1 = data_Base.add_house(house4,price4.price,price4.date)
    result2 = data_Base.add_house(house4,price4.price,price4.date)
    result3 = data_Base.add_house(house4,price4.price,price4.date)
    assert result1['status'] == Db_save_state.new_house_added
    assert result2['status'] == Db_save_state.house_and_price_duplicated
    assert result3['status'] == Db_save_state.house_and_price_duplicated
    # Se verifica que la cantidad de casas y precios en la base de datos de prueba sea 1
    assert data_Base.session.query(House).count() == 1
    assert data_Base.session.query(Price).count() == 1
    # Se elimina la casa de la base de datos de prueba
    data_Base.delete_house_by_id(house4.id)
    # Se verifica que la cantidad de casas y precios en la base de datos de prueba sea 0
    assert data_Base.session.query(House).count() == 0
    assert data_Base.session.query(Price).count() == 0

def test_create_house_same_id_different_price_and_date(test_session):
    data_Base = test_session
    # Eliminar tablas de la base de datos de prueba
    data_Base.session.query(House).delete()
    data_Base.session.query(Price).delete()
    # Se eliminan todas las casas y precios existentes en la base de datos
    # de prueba para comenzar con una base de datos vacía.
    # Se crean tres casas con el mismo ID (5) pero con diferentes precios y fechas utilizando la función crear_casa. 
    house5,price5 = create_house(5,1300,1676933185.260)
    house5,price6 = create_house(5,1400,1676933187.260)
    house5,price7 = create_house(5,1500,1676933188.260)
    # Se agregan las tres casas creadas anteriormente a la base de datos utilizando el método add_house de la sesión de prueba.
    result1 = data_Base.add_house(house5,price5.price,price5.date)
    result2 = data_Base.add_house(house5,price6.price,price6.date)
    result3 = data_Base.add_house(house5,price7.price,price7.date)
    assert result1['status'] == Db_save_state.new_house_added
    assert result2['status'] == Db_save_state.new_price_added
    assert result3['status'] == Db_save_state.new_price_added
    # Se verifica que la base de datos contenga una sola casa y tres precios.
    assert data_Base.session.query(House).count() == 1
    assert data_Base.session.query(Price).count() == 3
    # Se elimina la casa con el ID 5 de la base de datos utilizando el método delete_house_by_id de la sesión de prueba.
    data_Base.delete_house_by_id(house5.id)
    # Se verifica que la cantidad de casas y precios en la base de datos de prueba sea 0
    assert data_Base.session.query(House).count() == 0
    assert data_Base.session.query(Price).count() == 0


def test_find_house_last_price_by_id(test_session):
    data_Base = test_session
    # Eliminar tablas de la base de datos de prueba
    data_Base.session.query(House).delete()
    data_Base.session.query(Price).delete()
    # Se crean tres casas con el mismo ID (5) pero con diferentes precios y fechas utilizando la función crear_casa. 
    house5,price5 = create_house(5,1300,1676933185.260)
    house5,price6 = create_house(5,1400,1676933187.260)
    house5,price7 = create_house(5,1500,1676933188.260)
    # Se agregan las tres casas creadas anteriormente a la base de datos utilizando el método add_house de la sesión de prueba.
    result1 = data_Base.add_house(house5,price5.price,price5.date)
    result2 = data_Base.add_house(house5,price6.price,price6.date)
    result3 = data_Base.add_house(house5,price7.price,price7.date)
    assert result1['status'] == Db_save_state.new_house_added
    assert result2['status'] == Db_save_state.new_price_added
    assert result3['status'] == Db_save_state.new_price_added
    # utiliza la función find_house_last_price_by_id  para encontrar el ultimo precio de la casa por id de la casa
    pricedb = data_Base.find_house_last_price_by_id(house5.id)
    # Se compueba que el id de la casa del precio es el mismo que la casa creada
    assert pricedb.house_id == house5.id
    # Se comprueba que la fecha del precio de la base de datos es la ultima
    assert pricedb.date == price7.date


def test_update_house_active(test_session):
    data_Base = test_session
    # Eliminar tablas de la base de datos de prueba
    data_Base.session.query(House).delete()
    data_Base.session.query(Price).delete()
    # Se crea casa 
    house_10,price_10 = create_house(10,1300,1676933185.260)
    # Se agrega a la base de datos utilizando el método add_house de la sesión de prueba.
    result1 = data_Base.add_house(house_10,price_10.price,price_10.date)
    assert result1['status'] == Db_save_state.new_house_added
    housedb = data_Base.find_houses_by_id(10)
    assert housedb.active == True
    update_house = data_Base.update_ad_state(10,False)
    housedb2 = data_Base.find_houses_by_id(10)
    assert housedb2.active == False
    update_house = data_Base.update_ad_state(10,True)
    housedb3 = data_Base.find_houses_by_id(10)
    assert housedb3.active == True
    


