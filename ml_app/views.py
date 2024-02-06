from django.shortcuts import render
from .forms import RealEstatePredictionForm
from .models import RealEstateListing
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib

# Function to clean and predict 
def clean_and_predict(features, model_path='best_model.joblib'):
    # Load the trained RandomForestRegressor model
    model = joblib.load(model_path)

    # Create a DataFrame with the provided features
    data = pd.DataFrame([features], columns=RealEstateListing._meta.get_all_field_names())

    # Data cleaning steps
    data = perform_data_cleaning(data)

    # Make a prediction
    prediction = model.predict(data)[0]
    return prediction

# Function to perform data cleaning
def perform_data_cleaning(data):
    # Drop unnecessary columns
    data = data.drop(columns=['last_active_check_date', 'title', 'location_4', 'zone_url'], axis=1)

    # Convert date column to numeric format
    data['post_time'] = pd.to_numeric(pd.to_datetime(data['post_time']).dt.strftime('%Y%m'))

    # Remove unwanted characters from object columns
    characters_to_remove = '[,;/.\\!0-9]'
    data_object_columns = data.select_dtypes(include='object').columns
    data[data_object_columns] = data[data_object_columns].apply(lambda x: x.str.replace(characters_to_remove, '', regex=True))

    # Perform one-hot encoding
    data = pd.get_dummies(data, columns=['location_1', 'location_2', 'location_3'], drop_first=True)

    return data

# View function
def predict_real_estate_price(request):
    form = RealEstatePredictionForm(request.POST or None)
    prediction = None

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            # Extract features from the form
            features = [getattr(instance, field) for field in RealEstateListing._meta.get_all_field_names()]

            # Make prediction using the helper function
            prediction = clean_and_predict(features)

    context = {'form': form, 'prediction': prediction}
    return render(request, 'ml/predict_real_estate_price.html', context)
