from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_real_estate_price, name='predict_real_estate_price'),

]