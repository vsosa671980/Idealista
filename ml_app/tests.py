from django.test import TestCase
from django.urls import reverse
from .models import RealEstateListing
from .forms import RealEstatePredictionForm

class RealEstatePricePredictionTest(TestCase):
    def test_predict_real_estate_price_view(self):
        # Create a RealEstateListing instance with some sample data
        sample_data = {
            'atico': 1.0,
            'latitude': 2.0,
            'longitude': 3.0,
            'roomNumber': 4.0,
            'bathNumber': 2.5,
            'hasParking': 1.0,
            'hasGarden': 0.0,
            'hasSwimmingPool': 1.0,
            'hasTerrace': 0.0,
            'superficie_min': 150.0,
            'armarios_empotrados': 1.0,
            'trastero': 0.0,
            'parcela': 200.0,
            'balcon': 1.0,
            'altura': 3.0,
            'ubicacion_1': 'gran_canaria',
            'ubicacion_2': 'las_palmas_de_gran_canaria',
            'ubicacion_3': 0.0,
            'isNewDevelopment': 1.0,
            'isNeedsRenovating': 0.0,
            'isGoodCondition': 1.0,
        }

        # Submit the sample data to the view
        response = self.client.post(reverse('predict_real_estate_price'), data=sample_data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the form in the response context is an instance of RealEstatePredictionForm
        self.assertIsInstance(response.context['form'], RealEstatePredictionForm)

        # Check if the form is valid
        self.assertTrue(response.context['form'].is_valid())

        # Check if the prediction is present in the response context
        self.assertIn('prediction', response.context)

        # Check if the prediction is a float
        self.assertIsInstance(response.context['prediction'], float)

        # Add more specific assertions based on your requirements

    # Add more test methods as needed
