import os
import sys
# get current directory
path = os.path.dirname(__file__)
# parent directory
parent = os.path.dirname(path)
grandParent = os.path.dirname(parent)
# appending a path
sys.path.append(grandParent)
import httpx
from bs4 import BeautifulSoup as bs
from time import sleep
from scrapping_app.scrapping.error_logger import log_error
from scrapping_app.scrapping.config import URL_GOOGLE
import random

def save_html_file(html,file_name):
    """
    Función Auxiliar
    Guarda el fichero html en la ruta que le indiquemos,
    haciendo un encoding primero

    Parámetros
    ----------
        html: Fichero HTML a guardar
        file_name: Ruta donde lo guardaremos
    """
    try:
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(html)
    except Exception as e:
        log_error(f'(req_html.py) Error saving html file: {e}')

def open_html_file(file_name):
    """
    Función Auxiliar
    Abre el fichero html de la ruta que le indiquemos,
    haciendo un encoding primero

    Parámetros
    ----------
        file_name: Ruta donde se encuentra el fichero
    """
    try:
        with open(file_name,'r', encoding='utf-8') as fp:
            return fp.read()
    except Exception as e:
        log_error(f'(req_html.py) Error opening html file: {e}')
        return None 

class Httpx_Client():
    """
    Clase para gestionar la sesión httpx para peticiones del html de la página web
    """

    def __init__(self,page):
        """
        Constructor que crea un Cliente/Sesión htppx

        Parámetros
        ----------
            page: str informativo de la página , que no servirá al crear los header de las peticiones
        """
        self.page = page
        # comenzamos viniendo de google
        self.previous_url = URL_GOOGLE
        try:
            self.session = httpx.Client(headers=self.generate_header(self.previous_url), follow_redirects=True)
        except Exception as e:
            log_error(f'(req_html.py) Error init HTTPX Client: {e}')
            self.session = None

    def generate_header(self,newreferer_url):
        """
        Función que nos genera unos headers para evitar problemas de catch de la página

        Parámetros
        ----------
            newreferer_url: URL de la página que simulamos que venimos
        """
        sec_fetch_site = 'same-origin' if self.page in newreferer_url else 'cross-site'
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': newreferer_url,
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': sec_fetch_site,
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }
        return header

    def get_html_from_url(self,url,previous_url):
        """
        Función que nos realiza la petición de la url

        Parámetros
        ----------
            url: URL de la página que queremos solicitar
            previous_url: URL de la página que simulamos que venimos para simular
                uso humano

        Return
        ------
            html: Texto html de la petición de la URL
        """
        try:
            # TODO: Meter un header diferente en cada request si metemos proxies
            header = self.generate_header(previous_url)
            r = round(random.uniform(1,7.0),2)
            sleep(r)
            # TODO: Meter un proxie en cada request y quitar los tiempos de espera
            req = self.session.get(url,headers=header)
            # TODO: CHEQUEAR RESPONSE PARA COMPROBAR QUE SE HA DESCARGADO BIEN, O QUE HA HECHO REDIRECT, O SI ENTRÓ EL CATCH
            html = req.text
        except Exception as e:
            log_error(f'(req_html.py) Error getting HTML from URL {url}: {e}')
            html = None
        return html
    
    
    
        









