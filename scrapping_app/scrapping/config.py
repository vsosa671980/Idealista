import enum

class OperationType(enum.IntEnum):
    rent = 0
    sale = 1 

#URLS IDEALISTA
IDEALISTA_NAME ='idealista'
URL_MAIN_IDEALISTA =  "https://www.idealista.com"
URL_MAIN_SALE_IDEALISTA =  URL_MAIN_IDEALISTA + "/venta-viviendas"
URL_MAIN_RENT_IDEALISTA =  URL_MAIN_IDEALISTA + "/alquiler-viviendas"
URL_MAIN_HOUSE_IDEALISTA =  URL_MAIN_IDEALISTA + "/inmueble"

#URLS
URL_GOOGLE = "https://www.google.es/"

#ID_TEST
HOUSE_ID_TEST="101985304"

#ERRORs LOG File Name
ERROR_LOG_FILE_NAME = 'errors.log'

#DATABASE NAME
DATABASE_NAME = 'idealista_data_base'
TEST_DATABASE_NAME = 'test_idealista_data_base'

FINAL_URL  = "/venta-viviendas/las-palmas/gran-canaria/mapa"

ZONE_URLS_FILE  = "scrapping_app/scrapping/zone_urls.csv"
ZONE_URLS_FILE_NAME = "zone_urls.csv"