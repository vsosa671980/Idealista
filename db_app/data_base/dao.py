import os
import sys
from django.http import Http404
# get current directory
path = os.path.dirname(__file__)
# parent directory
parent = os.path.dirname(path)
grandParent = os.path.dirname(parent)
# appending a path
sys.path.append(grandParent)
from db_app.data_base.model import Base, House, Price
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import create_engine,func,asc
from sqlalchemy.orm import joinedload

from datetime import datetime
import os
import enum

class Db_save_state(enum.IntEnum):
    new_house_added = 1
    new_price_added = 2
    house_and_price_duplicated = 3
    error = 4
    pending = 5
    
    """Class of HouseS
    """
class HouseDao:
    ## Constructor of houseDao
    def __init__(self,database_name):
        """
        Constructor que crea una conexión con la base de datos houses.db
        """
        database_name = f'{database_name}.db'
        db_path = os.path.join(os.path.dirname(__file__), database_name)
        db_uri = 'sqlite:///{}'.format(db_path)
        #Create the engine object
        self.engine = create_engine(db_uri)
        #self.engine = create_engine('sqlite:///app_idealista/data/houses.db', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)
   
        """Add House to database
           param: house_object
                  price float
                  date datetime
        """
    def add_house(self, house:House, price, date):
      
        # Check if the house exist by its id
        if not self.find_houses_by_id(house.id):
            try:
                # Add House
                self.session.add(house)
                self.session.flush()
                # Create a new Price oject
                new_price = Price(house_id=house.id, price=price, date=date)
                # Add price to database
                self.session.add(new_price)
                self.session.commit()
                # Return the house
                return {'id': house.id, 'price': price, 'date': date, 'status':Db_save_state.new_house_added}
            except Exception as e:
                print(f'Error adding new house: {e}')
                self.session.rollback()
                return {'id': house.id, 'price': price, 'date': date,'status':Db_save_state.error}
        # Check if the house exist in the database 
        elif not self.session.query(Price).filter_by(date=date,house_id=house.id).first(): 
            try:
                # Create a price object with the existing house ID, the new price, and the date
                new_price = Price(house_id=house.id, price=price, date=date)
                self.session.add(new_price)
                self.session.commit()
                # In this case, I activate it, as I am sure I found it and am adding it
                self.update_ad_state(house.id,True)
                # We return the created house with its ID and the associated price
                return {'id': house.id, 'price': price, 'date': date,'status':Db_save_state.new_price_added}
            except Exception as e:
                print(f'Error adding new price: {e}')
                self.session.rollback()
                return {'id': house.id, 'price': price, 'date': date,'status':Db_save_state.error}
        self.update_ad_state(house.id,True)
        return {'id': house.id, 'price': price, 'date': date,'status':Db_save_state.house_and_price_duplicated}
    
    """Update the status of house
          Param: id(int): id de la casa
                 active(bool): Nuevo estado, inactivo activo
          Return boolean
    """
    def update_ad_state(self,id:int,active:bool):
        try:
            if active:
                self.session.query(House).filter_by(id=id).update({'active': active,'last_active_check_date': datetime.now()})
            else:
                self.session.query(House).filter_by(id=id).update({'active': active})
            self.session.commit()
            return True
        except Exception as e:
            print(f'Error updating house active: {e}')
            return None
   
        """Find Houses by id
        """
    def find_houses_by_id(self,id):
        try:
            return self.session.get(House,id)
        except Exception as e:
            print(f'Error finding house by id: {e}')
            return None


    """Delete House
       Param: id int
       Return: boolean
    """
    def delete_house_by_id(self,id):
     
        try:
            house = self.find_houses_by_id(id)
            if house:
                self.session.delete(house)
                self.session.commit()
                return id,True
            else:
                print("House not found in the database")
                return id,False
        except Exception as e:
            print(f'Error deleting house by id: {e}')
            self.session.rollback()
            return None,False
        """Filter Houses
           params: string
           Return: boolean
        """
    def filter_houses(self,**kwargs):
        ## Filter Houses actives
        status_house = {'active':True}
        # Combine all filters 
        filters = {**status_house, **kwargs}
        try:
            list_houses_model = self.session.query(House).filter_by(**filters).all()
            list_houses_model.sort(key=lambda house: house.last_price,reverse=False)
            list_houses_dict = [house.serialize() for house in list_houses_model]
            return list_houses_dict
        except Exception as e:
            print(f'Error filtering houses: {e}')
            raise Http404("No found")
            return None
    """Get the houses from zone
    
    Keyword arguments:
    Parameters:zone_url - string
    Return: boolean
    """
       
    def houses_ids_from_zone(self,zone_url):
        try:
            result =  self.session.query(House).with_entities(House.id).filter(House.zone_url == zone_url).all()
            return [r[0] for r in result]
        except Exception as e:
            print(f'Error filtering houses from zone: {e}')
            return None
    
        """Get the last price of the house selected
           Parameters: id int
           Return:last_price boolean or None
        """
    def find_house_last_price_by_id(self,id):
        try:
            last_price = self.session.query(Price).filter(Price.house_id == id).order_by(Price.date.desc()).first()
            return last_price
        except Exception as e:
            print(f'Error finding last price houseid {id}: {e}')
            return None
    """
    def get_zones_from_data_base(self):
        unique_zone_urls = self.session.query(House.zone_url).distinct().all()
        return [url[0] for url in unique_zone_urls]
    """ 
    def get_zones_from_data_base(self):
        #TODO: lista con todas las URLS sin repetir
        result = (
        self.session.query(
            House.zone_url,
            func.count().label('element_count')
        )
        .filter(House.active == True)  # Filtro para obtener solo elementos con active=True
        .group_by(House.zone_url)
        .all()
         )
        return result
        """Get all the houses
        """
    def get_all_houses(self):
        try:
            houses = self.session.query(House).all()
            return houses
        except Exception as e:
            print(e)
    
  