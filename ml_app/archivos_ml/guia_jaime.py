import os
import sys
# get current directory
path = os.path.dirname(__file__)
# parent directory
parent = os.path.dirname(path)
grandParent = os.path.dirname(parent)
# appending a path
sys.path.append(grandParent)
from db_app.data_base.dao import HouseDao
from scrapping_app.scrapping.config import DATABASE_NAME
import pandas as pd

house_dao = HouseDao(DATABASE_NAME)

pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x)) #Limiting floats output to 3 decimal points

# DESCARGA DE DATOS
all_data_df = pd.DataFrame([house.serialize() for house in house_dao.filter_houses(active=True)])
all_data_df.set_index("id",inplace=True)

print(all_data_df.head())
print(all_data_df.columns)
print(all_data_df['zone_url'].unique())