from django import forms
from .models import RealEstateListing

class RealEstatePredictionForm(forms.ModelForm):
    class Meta:
        model = RealEstateListing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RealEstatePredictionForm, self).__init__(*args, **kwargs)

        # Make all fields optional
        for field_name, field in self.fields.items():
            field.required = False

        # Set widget for fields with two options to CheckboxInput
        checkbox_fields = [
            'hasParking', 'hasGarden', 'hasSwimmingPool', 'hasTerrace',
            'armarios_empotrados', 'trastero', 'balcon', 'atico',
            'isNewDevelopment', 'isNeedsRenovating', 'isGoodCondition',
        ]

        for field_name in checkbox_fields:
            self.fields[field_name].widget = forms.CheckboxInput(attrs={'value': '1'})
            
                
    def clean(self):
        cleaned_data = super().clean()

        # Set default value for checkbox fields if not provided
        checkbox_fields = [
            'hasParking', 'hasGarden', 'hasSwimmingPool', 'hasTerrace',
            'armarios_empotrados', 'trastero', 'balcon', 'atico',
            'isNewDevelopment', 'isNeedsRenovating', 'isGoodCondition',
        ]

        for field_name in checkbox_fields:
            if field_name not in cleaned_data:
                cleaned_data[field_name] = 0

        return cleaned_data
