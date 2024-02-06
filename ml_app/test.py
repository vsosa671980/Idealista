import sys
import os
import sqlite3
import csv
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib


def predecir_precios():
    db_path = 'idealista_data_base.db'  
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute and save query for 'houses' and 'prices' in a single CSV file
    query = '''
        SELECT houses.*, prices.price
        FROM houses
        INNER JOIN prices ON houses.id = prices.house_id
    '''
    csv_file_path = 'completed_houses.csv'
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(columns)
        csv_writer.writerows(rows)

    conn.close()

    # Read the merged CSV file into a DataFrame
    merged_df = pd.read_csv('completed_houses.csv')

    # Save the merged DataFrame to a new CSV file
    merged_csv_path = 'completed_houses.csv'
    data = merged_df.to_csv(merged_csv_path, index=False)
    
    
    model = joblib.load('best_model.joblib')
    housing = pd.read_csv(data)
    housing.head()

    numeric_columns = ['usable_area', 'built_year', 'plot_area']
    imputer_numeric = SimpleImputer(strategy='mean')
    housing[numeric_columns] = imputer_numeric.fit_transform(housing[numeric_columns])

    housing = housing.drop(columns=['last_active_check_date'], axis=1)

    housing = housing.drop(columns=['title', 'location_4', 'zone_url'], axis=1)

    # Define the characters to remove
    characters_to_remove = '[,;/.\\!0-9]'

    # Replace characters in all object columns
    housing_object_columns = housing.select_dtypes(include='object').columns
    housing[housing_object_columns] = housing[housing_object_columns].apply(lambda x: x.str.replace(characters_to_remove, '', regex=True))

    # Now, you can proceed with one-hot encoding
    housing = pd.get_dummies(housing, columns=['location_1', 'location_2', 'location_3'], drop_first=True)

    # Define X and y
    X = housing.drop(columns='price', axis=1)
    y = housing['price']

    predicted = model.predict(X)
    
    return predicted