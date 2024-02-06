from django.urls import  path
from scrapping_app.views import scrapping, scrapping_process,scrapping_all

urlpatterns = [
    path('scrapping/', scrapping, name='scrapping'),
    path('scrapping_all/', scrapping_all, name='scrapping_all'),
    path('scrapping_process/<int:id>/', scrapping_process ,  name='scrapping_process'),
   
]

