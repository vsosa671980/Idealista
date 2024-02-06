from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()

from enum import IntEnum

class ConstructionType(IntEnum):
    block_of_flats = 1
    semi_detached = 2
    independent = 3

class HeightType(IntEnum):
    single_floor = 0
    low_floors = 1
    mid_floors_without_elevator = 2
    mid_floors_with_elevator = 3
    high_floors_without_elevator = 4
    high_floors_with_elevator = 5
    
class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean,default=True)
    last_active_check_date = Column(DateTime)
    post_time = Column(DateTime)
    operation = Column(Integer)
    title = Column(String)
    is_penthouse = Column(Boolean,default=False)
    is_duplex = Column(Boolean,default=False)
    is_flat = Column(Boolean,default=False)
    is_studio = Column(Boolean,default=False)
    is_apartment = Column(Boolean,default=False)
    is_loft = Column(Boolean,default=False)
    is_ground_floor = Column(Boolean,default=False)
    is_semi_detached_house = Column(Boolean,default=False)
    is_townhouse = Column(Boolean,default=False)
    is_bungalow = Column(Boolean,default=False)
    is_country_house = Column(Boolean,default=False)
    is_large_country_house = Column(Boolean,default=False)
    is_villa = Column(Boolean,default=False)
    is_terraced_house = Column(Boolean,default=False)
    rooms_number = Column(Integer)
    baths_number = Column(Integer)
    floors = Column(Integer)
    floor_number = Column(Integer)
    built_area = Column(Float)
    usable_area = Column(Float)
    constructed_area = Column(Float)
    built_year = Column(Integer)
    plot_area = Column(Float)
    has_lift = Column(Boolean,default=False)
    has_parking = Column(Boolean,default=False)
    has_garden = Column(Boolean,default=False)
    has_swimming_pool = Column(Boolean,default=False)
    has_terrace = Column(Boolean,default=False)
    has_fitted_wardrobes = Column(Boolean,default=False)
    has_storage_room = Column(Boolean,default=False)
    has_balcony = Column(Boolean,default=False)
    is_new_development = Column(Boolean,default=False)
    is_needs_renovation = Column(Boolean,default=False)
    is_good_condition = Column(Boolean,default=False)
    latitude = Column(String)
    longitude = Column(String)
    location_1 = Column(String)
    location_2 = Column(String)
    location_3 = Column(String)
    location_4 = Column(String)
    zone_url = Column(String)
   
    prices = relationship('Price', backref='house',cascade="all, delete-orphan",lazy='dynamic')
    
    @hybrid_property
    def construction_type(self): 
        if (self.is_country_house or self.is_large_country_house
             or  self.is_villa or self.is_terraced_house):
            return ConstructionType.independent.value
        elif self.is_semi_detached_house or self.is_townhouse or  self.is_bungalow:
            return ConstructionType.semi_detached.value
        elif (self.is_penthouse or self.is_duplex or  self.is_flat or self.is_studio 
              or self.is_apartment or self.is_ground_floor or self.floor_number>1):
            return ConstructionType.block_of_flats.value
        else:
            return ConstructionType.independent.value
    
    @hybrid_property
    def mid_floors(self): 
        if ((self.floor_number == 2) or (self.floor_number == 3)) and (self.construction_type == ConstructionType.block_of_flats.value):
            return True
        return False
    
    @hybrid_property
    def low_floors(self): 
        if (self.floor_number == 1) and (self.construction_type == ConstructionType.block_of_flats.value): 
            return True
        return False

    @hybrid_property
    def high_floors(self): 
        if (self.floor_number > 3) and (self.construction_type == ConstructionType.block_of_flats.value): 
            return True
        return False
    
    @hybrid_property
    def height(self): 
        if self.high_floors:
            if self.has_lift:
                return HeightType.high_floors_with_elevator.value
            return HeightType.high_floors_without_elevator.value
        elif self.mid_floors:
            if self.has_lift:
                return HeightType.mid_floors_with_elevator.value
            return HeightType.mid_floors_without_elevator.value
        elif self.low_floors:
            return HeightType.low_floors.value
        else:
            return HeightType.single_floor.value
    
    @hybrid_property
    def min_surface(self): 
        return min([s for s in [self.built_area, self.usable_area, self.constructed_area] if s])
    
    @hybrid_property
    def max_surface(self): 
        return max([s for s in [self.built_area, self.usable_area, self.constructed_area] if s])
    
    @hybrid_property
    def last_price(self): 
        #TODO: CHECK -1 ...BUSCAMOS EL QUE TENGA LA ULTIMA FECHA
        return round([price_object.price for price_object in self.prices][-1])
       
    @hybrid_property
    def predicted_price(self):
        latest_price = (
            self.prices
            .order_by(Price.date.desc())  # Ordenar las instancias de Price por fecha descendente
            .first()  # Tomar la primera instancia (la más reciente)
    )    
        price = round(latest_price.predicted_price,2) 
        return price if latest_price else None
        """Create Dictionary of house
        """
    def serialize(self):
        return {
            "id": self.id,
            "active": self.active,
            "last_active_check_date":self.last_active_check_date,
            "post_time": self.post_time,
            "operation": self.operation,
            "title": self.title,
            "is_penthouse" : self.is_penthouse,
            "is_duplex" : self.is_duplex,
            "is_flat" : self.is_flat,
            "is_studio" : self.is_studio,
            "is_apartment" : self.is_apartment,
            "is_loft" : self.is_loft,
            "is_ground_floor" : self.is_ground_floor,
            "is_semi_detached_house" : self.is_semi_detached_house,
            "is_townhouse" : self.is_townhouse,
            "is_bungalow" : self.is_bungalow,
            "is_country_house" : self.is_country_house,
            "is_large_country_house" : self.is_large_country_house,
            "is_villa" : self.is_villa,
            "is_terraced_house" : self.is_terraced_house,
            "rooms_number": self.rooms_number,
            "baths_number": self.baths_number,
            "floors": self.floors,
            "height": self.height,
            "floor_number": self.floor_number,
            "low_floors": self.low_floors,
            "mid_floors": self.mid_floors,
            "high_floors": self.high_floors,
            "construction_type": self.construction_type,
            "min_surface": self.min_surface,
            "max_surface": self.max_surface,
            "plot_area":self.plot_area,
            "built_year": self.built_year,
            "has_lift": self.has_lift,
            "has_parking": self.has_parking,
            "has_garden": self.has_garden,
            "has_swimming_pool": self.has_swimming_pool,
            "has_terrace": self.has_terrace,
            "has_fitted_wardrobes": self.has_fitted_wardrobes,
            "has_storage_room": self.has_storage_room,
            "has_balcony": self.has_balcony,
            "is_new_development": self.is_new_development,
            "is_needs_renovation": self.is_needs_renovation,
            "is_good_condition": self.is_good_condition,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_1": self.location_1,
            "location_2": self.location_2,
            "location_3": self.location_3,
            "location_4": self.location_4,
            "zone_url": self.zone_url,
            "last_price":self.last_price,  
            "predicted_price":self.predicted_price
            
        }

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    house_id = Column(Integer, ForeignKey('houses.id'))
    price = Column(Float)
    predicted_price = Column(Float)
    __table_args__ = (UniqueConstraint('house_id', 'date'),)
    
    
    