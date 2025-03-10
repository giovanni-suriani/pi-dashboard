# Charts that are commonly used in the dashboard are produced anteriorly here
import sys
import os
import django
import requests
from django.http import JsonResponse
#four_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
three_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(three_levels_up)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pi_dashboard.settings')
django.setup()

from dashboard.models import *
from dashboard.views.views import GraphicProducerDashboardView as ChartProducer
import logging
import urllib.parse
import altair as alt
import argparse
import ast

from django.conf import settings
BASE_DIR = settings.BASE_DIR
HOST_GESTAO_PI = settings.HOST_GESTAO_PI
logger = logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(funcName)s:%(message)s")
logger = logging.getLogger(__name__)


def get_pis_dataset(instituicoes):
    # Join the list into a comma-separated string
    instituicoes_str = ",".join(instituicoes)

    encoded_instituicoes = urllib.parse.quote(instituicoes_str, safe=',')
    #TODO: MUDAR A URL EM PRODUÇÃO
    external_url_dataset = f'{HOST_GESTAO_PI}/app_dashboard/pis_dataset/?instituicoes={encoded_instituicoes}'
    try:
        requests.get(external_url_dataset).raise_for_status()
        data = requests.get(external_url_dataset).json()
        #logger.debug(f"Data = {data}")
        data_pis_dataset = data["pis_dataset"]
        logger.debug(f"Data = {data_pis_dataset}")
        return data["pis_dataset"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        return None
       
def get_wordcloud_dataset(instituicoes):
    instituicoes_str = ",".join(instituicoes)
    encoded_instituicoes = urllib.parse.quote(instituicoes_str, safe=',')
    external_url_dataset = f'{HOST_GESTAO_PI}/app_dashboard/wordcloud_dataset/?instituicoes={encoded_instituicoes}'
    try:
        requests.get(external_url_dataset).raise_for_status()
        data = requests.get(external_url_dataset).json()
        data_wordcloud_dataset = data["wordcloud_dataset"]
        logger.debug(f"wordcloud data = {data_wordcloud_dataset}")
        return data["wordcloud_dataset"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        return None
           
def print_records():
    records = ChartRequestsMemory.objects.all().order_by('request_amount').reverse()
    for record in records :
        print(f"Record: {record}")
        #campi_list = ast.literal_eval(record.instituicoes_request)
    if len(records) == 0:
        print("No records found")
        
def make_common_charts():
    records = ChartRequestsMemory.objects.all().order_by('request_amount').reverse()
    for i, record in enumerate(records):
        if i >= settings.MAXIMUM_CHARTS: # Usa-se '>=' pois i comeca no 0
            break
        logger.info(f"Record{i}: {record.instituicoes_request}")
        instituicoes = ast.literal_eval(record.instituicoes_request)
        logger.debug(f"instituicoes list: {instituicoes}")
        pis_dataset = get_pis_dataset(instituicoes)
        pis_dataset_obj = json.loads(pis_dataset)
        pis_dataset_keys = list(pis_dataset_obj.keys())
        wordcloud_dataset = get_wordcloud_dataset(instituicoes)
        logger.debug(f"wordcloud")
        #logger.debug(f"diretorio atual = {os.getcwd()} {BASE_DIR}")
        #alt.Chart.from_dict(pis_dataset)
        
        chart_pis_result = ChartProducer.chart_pis_last_years(
                dataset=pis_dataset,
                ano_inicio=pis_dataset_keys[0],
                ano_fim=pis_dataset_keys[-1],
                script_path=os.path.join(BASE_DIR, "dashboard/views/chart_generator_scripts/chart_pis_last_years.py"),
                path_to_save=os.path.join(BASE_DIR, "dashboard/static/chart_storage/pisGrafico"),
                instituicoes=instituicoes,
            )
        
        chart_wordcloud_result = ChartProducer.chart_wordcloud(
                dataset=wordcloud_dataset,
                path_to_save=os.path.join(BASE_DIR, "dashboard/static/chart_storage/wordcloud_images"),
                instituicoes=instituicoes,
            )
        
        logger.info(f"chart_pis_result = {chart_pis_result}")
        logger.info(f"chart_wordcloud_result = {chart_wordcloud_result}")
        #logger.warning(f"chart_pis_result = {chart_pis_result}")
    
def make_initial_charts():
    # Generate the charts for all the institutions (wordcloud and pis) 
    pis_dataset = get_pis_dataset(["all"])
    pis_dataset_obj = json.loads(pis_dataset)
    pis_dataset_keys = list(pis_dataset_obj.keys())
    wordcloud_dataset = get_wordcloud_dataset(["all"])
    chart_pis_result = ChartProducer.chart_pis_last_years(
                dataset=pis_dataset,
                ano_inicio=pis_dataset_keys[0],
                ano_fim=pis_dataset_keys[-1],
                script_path=os.path.join(BASE_DIR, "dashboard/views/chart_generator_scripts/chart_pis_last_years.py"),
                path_to_save=os.path.join(BASE_DIR, "dashboard/static/chart_storage/pisGrafico"),
            )
        
    chart_wordcloud_result = ChartProducer.chart_wordcloud(
            dataset=wordcloud_dataset,
            path_to_save=os.path.join(BASE_DIR, "dashboard/static/chart_storage/wordcloud_images"),
        )
        
    logger.info(f"General chart_pis_result = {chart_pis_result}")
    logger.info(f"General chart_wordcloud_result = {chart_wordcloud_result}")
        
def delete_all_records():
    logger.info("Deletando todos os registros de ChartRequestsMemory")
    ChartRequestsMemory.objects.all().delete()
    print_records()        
    
#print_records()



from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = "Generate initial and common charts, also, delete all records of ChartRequestsMemory"

    def add_arguments(self, parser):
        parser.add_argument('--initial', action='store_true', required=False, help='Generate initial and common charts') # action='store_true' creates a boolean (true) argument if specified
        parser.add_argument('--delete_records', action='store_true', required=False, help='Delete all records of ChartRequestsMemory')
    
        
    def handle(self, *args, **options):
        # Replace this with your actual logic:
        logger.info(f"Executando rotina em {datetime.now()}")
        print_records()
        if options['initial']:
            make_initial_charts()
            make_common_charts()
        if options['delete_records']:
            delete_all_records()
            
#python3 make_common_charts.py --initial 
        
        
    
        
        