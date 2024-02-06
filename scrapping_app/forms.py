# forms.py
from django import forms

class CostumeForm(forms.Form):
    scrapping_options = forms.ChoiceField(choices=[(0, 'Get All Gran Canaria Zones from Idealista.'),
                                                    (1, 'Get All Gran Canaria Zones from last Update')],
                                                    label="Select Scrapping Option:")


    