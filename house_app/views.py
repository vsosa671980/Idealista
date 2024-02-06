from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from db_app.data_base.dao import HouseDao
from django.core.paginator import Paginator
import json
from django.middleware.csrf import get_token
from house_app.grafic import generate_plot
import pandas as pd
import db_app.data_base.pull as prediction_prices



"""Get and return the tocken
"""
def send_tocken(request):
    csrf_token = get_token(request)
    return JsonResponse({
        "token" : csrf_token
    })
    
    """Return list of houses filtered
       param:
           page int
       return:
           JsonResponse list of houses
    """
def response_Json_houses(request,page=1):
   
   try: 
        if request.method == "POST":
            ## Convert the data received to python dictionary
            json_data = json.loads(request.body.decode('utf8'))
            ## Get the page number
            page = int(json_data['page'])
            ##  Get the filters received from client
            filters = json_data['filters']
            ## Create a new dao Object
            dao = HouseDao('idealista_data_base')
            houses = dao.filter_houses(**filters)
            ## Use paginator and inicate number of houses
            paginator = Paginator(houses, 5)
            page_articles = paginator.get_page(page) 
            ## Create dict with atributes selected
            articles_en_dict = [
               {"title": article.get('title', ''), "zone_url": article.get('zone_url', ''), "last_price": article.get('last_price',''),"predicted_price":article.get('predicted_price','')} 
                for article in page_articles]
            ## Create dict with data for send in the response
            data = {
                "pages":paginator.num_pages,
                "houses":articles_en_dict,
                "actual_page":page
            }
        return JsonResponse(data, safe=False)
    ## Retur error in case 
   except Exception as e: 
       return JsonResponse({
           "error": "Error Response" + str(e)
       })
       
"""Get page of loading Houses
Keyword arguments:
argument -- request
Return: render template
"""
def loading(request):
    return render(request,"houses/loading.html")

    """Get the main page of houses.
       Update the database with predicction prices
       Return:Render Template with atributes and grafic
    """
def pagination_houses(request,page=1):
    ##Instance the HouseDao object class
    dao = HouseDao('idealista_data_base')
    ## Get the predictions prices of the houses
    prediction_prices.predecir_precios()
    ## Get houses from database filtered
    houses = dao.filter_houses()
    ## Get the locations
    locations = [house['location_2']for house in houses]
    locations_filter = set(locations)
    ## Get the cities
    cities = [house['location_1'] for house in houses]
    cities_filter = set(cities)  
    ## Features of houses
    house_features = {
        "has_lift":"ascensor",
        "has_parking" :"estacionamiento",
         "has_garden" : "jardín",
         "has_swimming_pool" :    "piscina",
         "has_terrace" :  "terraza",
         "has_fitted_wardrobes":"armarios_empotrados", 
        "has_storage_room":" trastero",
        "has_balcony":"balcón"}
    ## Type of houses
    house_types = {
    'is_penthouse': "Atico",
    'is_duplex': "Duplex",
    'is_flat': "Piso",
    'is_studio': "Estudio",
    'is_apartment': "Apartamento",
    'is_loft': "Loft",
    'is_ground_floor': "Planta Baja",
    'is_semi_detached_house': "Casa Pareada",
    'is_townhouse': "Adosado",
    'is_bungalow': "Bungalow",
    'is_country_house': "Casa de Campo",
    'is_large_country_house': "Casa de campo Grande",
    'is_villa': "Villa",
    'is_terraced_house': "Casa Adosada",
        
    }
    ## Status of the houses
    houses_status = {
        'is_new_development':"nueva_construccion",
        "is_needs_renovation":"necesita reformas",
        "is_good_condition":"en buen estado"}
    
    ## Generate the grafic
    grafic = generate_plot()
    ## Return view with resources
    return render(request,"houses/houses.html",{ 
                                                
                                                'locations':locations_filter,
                                                'cities':cities_filter,
                                                'house_types':house_types,
                                                'house_features':house_features,
                                                'houses_status':houses_status,
                                                'grafic':grafic
                                               })
"""create a csv file from houses
"""
def generate_houses_csv(request):
    ## Data received from filters selected and past to 
     json_data = json.loads(request.body.decode('utf8'))
    ## Select the filters from dictionary
     filters = json_data['filters']
    ## Create object HouseDAo
     dao = HouseDao('idealista_data_base')
    ## List of houses filters
     houses = dao.filter_houses(**filters)
     ## Create dataframe 
     df_houses = pd.DataFrame(houses)
     print(df_houses)
     data_csv = df_houses.to_csv( index=False)
      # Crear una respuesta HTTP con el contenido del archivo CSV
     response_csv = HttpResponse(data_csv, content_type='text/csv')
     response_csv['Content-Disposition'] = 'attachment; filename="houses.csv"'
     return response_csv

"""Create Exel file and return it
Return: file HttResponse with file if houses
"""
def descargar_excel(request):
    # Crear un DataFrame de ejemplo
     ## Data received from filters selected and past to 
    json_data = json.loads(request.body.decode('utf8'))
    ## Select the filters from dictionary
    filters = json_data['filters']
    ## Create object HouseDAo
    dao = HouseDao('idealista_data_base')
    
    ## List of houses filters
    houses = dao.filter_houses(**filters)
    ## Create dataframe with houses
    df_houses = pd.DataFrame(houses)
    ## Get the names of columns
    columns_names = df_houses.columns
    # Generate Http Response
    response_excel = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response_excel['Content-Disposition'] = 'attachment; filename="houses.xlsx"'
    print("imprimniendo desde exel")
     # Save the data to exle
    df_houses.to_excel(response_excel, index=False, header=columns_names, sheet_name='Hoja1')
    ## Return exel
    return response_excel                                       