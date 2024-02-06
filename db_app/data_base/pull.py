import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def predecir_precios():
    # Database connection
    db_path = "db_app\data_base\idealista_data_base.db"
    try:
        with sqlite3.connect(db_path) as conn:
            query = '''
                SELECT houses.*, prices.price
                FROM houses
                INNER JOIN prices ON houses.id = prices.house_id
            '''
            merged_df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error: {e}")
    # Drop unnecessary columns
    merged_df = merged_df.drop(columns=['title', 'location_4', 'zone_url', 'last_active_check_date'], axis=1)

    # Convert all columns to numeric and replace non-numeric values with NaN
    try:
        merged_df = merged_df.apply(pd.to_numeric, errors='coerce')
    except ValueError as e:
        print(f"Error converting to numeric: {e}")

    # Replace empty cells with the mean for all columns
    try:
        merged_df = merged_df.apply(lambda col: col.fillna(col.mean()))
    except Exception as e:
        print(f"Error filling NaN values with mean: {e}")

    # Convert 'post_time' column to numeric representation
    try:
        merged_df['post_time'] = pd.to_numeric(pd.to_datetime(merged_df['post_time']).dt.strftime('%Y%m'))
    except ValueError as e:
        print(f"Error converting 'post_time' to numeric: {e}")

    # Define the characters to remove
    characters_to_remove = '[,;/:.\\!0-9]'

    # Replace characters in all object columns
    try:
        merged_df_object_columns = merged_df.select_dtypes(include='object').columns
        merged_df[merged_df_object_columns] = merged_df[merged_df_object_columns].apply(lambda x: x.str.replace(characters_to_remove, '', regex=True))
    except Exception as e:
        print(f"Error replacing characters in object columns: {e}")

    # One-hot encoding for categorical columns
    try:
        merged_df = pd.get_dummies(merged_df, columns=['location_1', 'location_2', 'location_3'], drop_first=True)
    except Exception as e:
        print(f"Error performing one-hot encoding: {e}")

    # Split the data into features (X) and target variable (y)
    X = merged_df.drop(columns=['price'])
    y = merged_df['price']

    # Handle missing values in X using SimpleImputer
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

    # Create and train the model
    try:
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
    except Exception as e:
        print(f"Error creating and training the model: {e}")

    # Model prediction
    try:
        merged_df['predicted_price'] = model.predict(X_imputed)
    except Exception as e:
        print(f"Error making predictions with the model: {e}")

    # Save the DataFrame to a new CSV file
    merged_df.to_csv('predicted_prices.csv', index=False)


    # Update the database with the predicted prices
    try:
        # Add a new column to the 'prices' table if not exist
        cursor = conn.cursor()
        ## Get information of table prices
        cursor.execute("PRAGMA table_info(prices)")
        ## Get the columns of table prices in list
        columns = [column[1] for column in cursor.fetchall()]
        ## Check if table exist
        if 'predicted_price' not in columns:
            conn.execute("ALTER TABLE prices ADD COLUMN IF NOT EXISTS predicted_price REAL")
        
        # Update the 'prices' table with the predicted prices
        for index, row in merged_df.iterrows():
            house_id = row['id']
            predicted_price = row['predicted_price']
            conn.execute(f"UPDATE prices SET predicted_price = ? WHERE house_id = ?", (predicted_price, house_id))

        # Commit the changes
        conn.commit()
    except Exception as e:
        print(f"Error updating the database: {e}")
        
    print(merged_df)    
    # Return the entire DataFrame with predicted prices
    return merged_df

# TEST!!!!  Run the function to TEST THE FUCTIONALITH OF THE SCRIPT!!!
##predecir_precios()
