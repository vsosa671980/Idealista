from django.shortcuts import render
from django.http import HttpResponse
from scrapping_app.scrapping.main import get_zones, get_houses_from_zone_url
from scrapping_app.scrapping.config import FINAL_URL, ZONE_URLS_FILE,URL_MAIN_IDEALISTA
from scrapping_app.forms import CostumeForm
import pandas as pd
import json

def scrapping(request):
    downloading = False
    results = []
    if request.method == 'POST':
        option_form = CostumeForm(request.POST)
        if option_form.is_valid():
            # Opcion de descarga de las zonas desde idealista o desde el archivo csv
            option = option_form.cleaned_data['scrapping_options']
            # Descargamos las url de las zonas de gran canaria
            results = get_zones(FINAL_URL,option)
            new_results = []
            for tupla in results:
                # Con esto resetamos el estado de descarga a 0 de todas las zonas.
                new_results.append((tupla[0],tupla[1],0))
            columnas = ['url', 'houses', 'status']
            df = pd.DataFrame(new_results, columns=columnas)
            data = df.to_json(orient="index")
            data = json.loads(data)   
            # Ahora ya guardamos el archivo csv de las zonas actualizado con el estado de descarga de cada zona a 0
            df.to_csv(ZONE_URLS_FILE, index=False)
            # Con este parametro mostramos un formato diferente de html, con la tabla de zonas
            downloading = True
        return render(request, 'scrapping/scrapping.html', {'downloading':downloading,
                                                            'data':data.items()})
    else:
        option_form = CostumeForm()
        return render(request, 'scrapping/scrapping.html', {'option_form': option_form,
                                                            'downloading':downloading})

def scrapping_process(request, id):
    if request.method == 'POST':
        # Identificamos la url de la zona que vamos a descargar
        df = pd.read_csv(ZONE_URLS_FILE)
        zone_url = df.loc[df.index[id], 'url']
        zone_url = zone_url.replace(URL_MAIN_IDEALISTA, "")
        # Descargamos todos los inmuebles de la zona
        get_houses_from_zone_url(zone_url)
        # Actualizamos el valor de status de la zona que vamos a descargar a OK
        df.loc[df.index[id], 'status'] = 'OK'
        df.to_csv(ZONE_URLS_FILE, index=False)
        data = df.to_json(orient="index")
        data = json.loads(data) 
        downloading = True
        # Cargamos de nuevo la pagina con el dato actualizado de la zona descargada
        return render(request, 'scrapping/scrapping.html', {'downloading':downloading,
                                                            'data':data.items()})


def scrapping_all(request):
    df = pd.read_csv(ZONE_URLS_FILE)
    # Descargamos todas las zonas que no hayan sido descargadas individualmente antes
    for zone in df[df['status']!='OK']['url']:
        zone_url = zone.replace(URL_MAIN_IDEALISTA, "")
        get_houses_from_zone_url(zone_url)
    df['status']=['OK']
    data = df.to_json(orient="index")
    data = json.loads(data)  
    downloading = True
    # Cargamos de nuevo la pagina con todas las zonas descargadas
    return render(request, 'scrapping/scrapping.html', {'downloading':downloading,
                                                            'data':data.items()})