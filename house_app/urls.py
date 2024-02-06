from django.urls import  path

from . import views

urlpatterns = [
    path('pagination/',views.pagination_houses, name='pagination_default'),
    #path('pagination/<int:page>/',views.pagination_houses, name='pagination_houses'),
    path('houses/',views.response_Json_houses, name='houses'),
    path('token/',views.send_tocken, name='token'),
    path('houses_csv/',views.generate_houses_csv, name='houses_csv'),
    path('houses_excel/',views.descargar_excel, name='houses_excel'),
    path('loading/',views.loading, name='loading'),

]
