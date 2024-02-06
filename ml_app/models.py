from django.db import models

class RealEstateListing(models.Model):
    atico = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    roomNumber = models.FloatField()
    bathNumber = models.FloatField()
    hasParking = models.FloatField()
    hasGarden = models.FloatField()
    hasSwimmingPool = models.FloatField()
    hasTerrace = models.FloatField()
    superficie_min = models.FloatField()
    armarios_empotrados = models.FloatField()
    trastero = models.FloatField()
    parcela = models.FloatField()
    balcon = models.FloatField()
    altura = models.FloatField()
    ubicacion_1 = models.FloatField()
    ubicacion_2 = models.FloatField()
    ubicacion_3 = models.FloatField(default=0)
    # ubicacion_4 = models.FloatField()
    # url_zona = models.CharField(max_length=255, blank=True, null=True)
    isNewDevelopment = models.FloatField()
    isNeedsRenovating = models.FloatField()
    isGoodCondition = models.FloatField()
    price = models.FloatField()  # Target variable