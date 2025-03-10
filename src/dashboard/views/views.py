from django.http import JsonResponse, HttpResponse 
from django.urls import reverse 
from django.views import View 
from django.shortcuts import get_object_or_404, render 
from django.views.decorators.cache import cache_page 
from django.core import serializers
import urllib 
from dashboard.models import *
from collections import defaultdict
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from requests import Session
import subprocess
import requests
import datetime
import json
import logging
import os

# Arquivo de coordenacao para multi ou single instituicao (utilitarios compartilhados dos dois e coordenacao)
from django.conf import settings
BASE_DIR = settings.BASE_DIR

HOST_GESTAO_PI = settings.HOST_GESTAO_PI # Servidor do GESTAO_PI

logger = logging.getLogger(__name__)

""" for item in query_set:
        print(item.tipo.nome) """

class PrettyJsonResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        # Ensure json_dumps_params contains indent and ensure_ascii=False for proper UTF-8 encoding
        if 'json_dumps_params' not in kwargs:
            kwargs['json_dumps_params'] = {}

        # Set default pretty-printing (indentation) and ensure ASCII characters are not escaped
        kwargs['json_dumps_params'].setdefault('indent', 4)
        kwargs['json_dumps_params'].setdefault('ensure_ascii', False)  # Enable proper UTF-8 output
        
        # Explicitly set content type to include UTF-8 charset
        kwargs.setdefault('content_type', 'application/json; charset=utf-8')
        
        # Call the parent class constructor
        super().__init__(data, **kwargs)


""" class RefreshView(View): """

def formata_instituicoes(instituicoes):
    # Dado as instituicoes, formata para uppercase e coloca em ordem alfabetica
    if not instituicoes:
        return []
    instituicoes = [instituicao.upper() for instituicao in instituicoes]
    return sorted(instituicoes)

def instituicoes_direction(instituicoes):
    # instituicoes upper casing
    new_inst = instituicoes
    #for instituicao in instituicoes:
    #    new_inst.append(instituicao.upper())
    mid = (len(new_inst) + 1) // 2  # Split point
    instituicao_left = new_inst[:mid]
    instituicao_right = new_inst[mid:]
    return instituicao_left, instituicao_right

def get_pis_and_wordcloud_data(instituicoes):
    instituicoes_str = ",".join(instituicoes)

    encoded_instituicoes = urllib.parse.quote(instituicoes_str, safe=',')
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

class DashboardView(View):
    def get(self, request):
        args = request.GET.get('instituicoes', '')
        """  if args:
            instituicoes = args.split(',')
            instituicoes = formata_instituicoes(instituicoes)
            logger.debug(f"instituicoes = {instituicoes} args = {args}")  
        else:
            instituicoes = [] """
        #return JsonResponse({'external_data': args})
        external_url = f'{HOST_GESTAO_PI}/app_dashboard/?instituicoes={args}'
        try:
            # Make the GET request to the external service
            response = requests.get(external_url)

            # Check if the request was successful
            response.raise_for_status()

            # Parse the response JSON
            data = response.json()

        except requests.exceptions.RequestException as e:
            # Handle errors in the GET request
            return JsonResponse({'error': str(e)}, status=500)
        
        data["instituicoes"] = formata_instituicoes(data["instituicoes"])
        logger.info(f"instituicoes received = {data['instituicoes']}")
        if not data["instituicoes"]:
            return HttpResponse("Instituicoes vazias", status=400)
        if data["panel_name"] == 'MULTI-INSTITUIÇÃO':
            data["css_file"] = "css/filter-screen_single.css"
            data["instituicao_left"], data["instituicao_right"] = instituicoes_direction(data["instituicoes"])
            #print(f"instituicoes = {instituicoes} inst left = {data['instituicao_left']} inst right = {data['instituicao_right']}")
            return render(request, 'dashboard_multi.html', data)
            
        else:
            #data["css_file"] = "css/filter-screen_single.css"
            #data["campis_left"], data["campis_right"] = campis_direction()
            #return PrettyJsonResponse(data)
            return render(request, 'dashboard_single.html', data)
        
    def post(self, request):
        external_url = f"{HOST_GESTAO_PI}/app_dashboard/"
        #print(f"POST request received, data = {request.POST}")
        #print(f"token = {get_token(request)}")
        # Create a requests session
        #session = Session()

        # Copy the session cookie from the incoming Django request
        logging.debug(f"All cookies: {request.COOKIES}")
        logging.warning(f"request data: {request.POST}")
        cookie_csrf_token = request.COOKIES.get('csrftoken')
        
        try:
            response = requests.post(
                external_url,
                data=request.POST,
                cookies={'csrftoken': cookie_csrf_token},
            )
            return JsonResponse(response.json())
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

class GraphicProducerDashboardView(View):
    def get(self, request):
        logger.warning(f"GET request received GARALHO")
        data = request.GET.dict()
        # print(f"GET request received, data = {data}")
        pis_dataset = data["pis_dataset"]
        wordcloud_dataset = data["wordcloud_dataset"]
        logger.debug(f"/////////////////\n pis_dataset = {pis_dataset}\n wordcloud_dataset = {wordcloud_dataset}\n/////////////////")
        instituicoes = json.loads(data["instituicoes"])
        instituicoes = formata_instituicoes(instituicoes)
        pis_dataset_obj = json.loads(pis_dataset)
        pis_dataset_keys = list(pis_dataset_obj.keys())
        logger.debug(f"instituicoes = {instituicoes}")
        logger.debug(f"wordcloud_dataset = {wordcloud_dataset}")

        try:
            chart_mem = ChartRequestsMemory.objects.get(instituicoes_request=str(instituicoes))
            chart_mem.request_amount += 1
            chart_mem.save()
        except ChartRequestsMemory.DoesNotExist:
            ChartRequestsMemory.objects.create(instituicoes_request=str(instituicoes), request_amount=1)

        chart_pis_result = GraphicProducerDashboardView.chart_pis_last_years(
            pis_dataset,
            ano_inicio=pis_dataset_keys[0],
            ano_fim=pis_dataset_keys[-1],
            instituicoes=instituicoes,
        )
        chart_wordcloud_result = GraphicProducerDashboardView.chart_wordcloud(
            dataset=wordcloud_dataset,
            instituicoes=instituicoes
        )

        results_path_json ={
            "chart_pis_result": chart_pis_result,
            "chart_wordcloud_result": chart_wordcloud_result
        }

        return JsonResponse(results_path_json)
        # return render(request, 'dashboard/results.html')

    def is_graphic_storage_full(path_to_save):
        # Verifica se a pasta de armazenamento de gráficos está cheia
        # Retorna 1 se estiver cheia, 0 caso contrario
        files = os.listdir(path_to_save)
        if len(files) > settings.MAXIMUM_CHARTS:
            return 1
        return 0

    def is_in_graphic_storage(output_name, path_to_save):
        # logger.debug(f"main_dir = {os.getcwd()}")
        # logger.debug(f"output_name = {output_name}")

        if os.path.exists(f"{path_to_save}/{output_name}"):
            return True
        return False

    def generate_output_name(chart_type = None, instituicoes = []):
        # print(f"chart_type = {chart_type}, instituicoes = {instituicoes}")

        if chart_type == "pisGrafico":
            current_date = datetime.datetime.now()
            formatted_date = current_date.strftime("-%Y-%m")
            if len(instituicoes) == 0:
                return f"pisGrafico"
            instituicao_identifier=''
            for instituicao in instituicoes:
                instituicao_identifier += "_"
                instituicao_identifier += instituicao
            if len(str(instituicao_identifier)) > 200:
                raise ValueError("instituicao_identifier too long")
            return f"pisGrafico{instituicao_identifier}{formatted_date}"
            # pis_grafico_campi1_campi2-ano-mes-dia.html

        if chart_type == "wordcloud":
            current_date = datetime.datetime.now()
            formatted_date = current_date.strftime("-%Y-%m")
            if len(instituicoes) == 0:
                return f"wordcloud"
            instituicao_identifier=''
            for instituicao in instituicoes:
                instituicao_identifier += "_"
                instituicao_identifier += instituicao
            if len(str(instituicao_identifier)) > 200:
                raise ValueError("instituicao_identifier too long")
            return f"wordcloud{instituicao_identifier}{formatted_date}"
            # wordcloud_campi1_campi2-ano-mes-dia.png

        logger.error(f"chart_type not valid, chart_type = {chart_type}" )  
        return None                  

    def chart_pis_last_years(dataset, ano_inicio = datetime.datetime.now().year - 4, 
                             ano_fim = datetime.datetime.now().year, 
                             script_path = os.path.join(BASE_DIR, "dashboard/views/chart_generator_scripts/chart_pis_last_years.py"),
                             path_to_save = os.path.join(BASE_DIR, "dashboard/static/chart_storage/pisGrafico"),
                             output_name = 'pisGrafico', instituicoes = []):
        # Gera grafico dinamicamente das patentes nos ultimos anos e salva 'output_name.html'
        # Retorna 1 se o grafico foi gerado com sucesso, 0 caso contrario
        # Print(test_set)
        theme = "ANALOGOUS_THEME"

        output_name = GraphicProducerDashboardView.generate_output_name("pisGrafico", instituicoes)

        if output_name is None:
            return 0

        # Verifica se a pasta de armazenamento de gráficos está cheia
        if GraphicProducerDashboardView.is_graphic_storage_full(path_to_save):
            logger.error(f"Graphic storage is full")
            return 0
            # return HttpResponse(f"Graphic storage is full", status

        if GraphicProducerDashboardView.is_in_graphic_storage(
            output_name + ".html", path_to_save
        ):
            return "/static/chart_storage/pisGrafico/" + output_name + ".html"
            # return HttpResponse(f"Pis last years already exists: {output_name}", status=200)
        
        if not dataset:
            logger.error(f"Dataset is Empty")
            return 0
            # return HttpResponse(f"Dataset is empty", status=500)
        # logger.debug(f"output_name = {output_name} dataset = {dataset}")
        
        if dataset:
            result = subprocess.run(
                [
                    "python3",
                    script_path,
                    "--theme",
                    theme,
                    "--dataset",
                    str(dataset),
                    "--ano_inicio",
                    str(ano_inicio),
                    "--ano_fim",
                    str(ano_fim),
                    "--path_to_save",
                    path_to_save,
                    "--output_name",
                    output_name,
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return "/static/chart_storage/pisGrafico/" + output_name + ".html"
                # return HttpResponse(f"Script ran successfully: {result.stdout}")
            else:
                logger.error(f"Error running script: {result.stderr}")
                return 0
                # return HttpResponse(f"Error running script: {result.stderr}", status=500)

    def chart_wordcloud(dataset = None, 
                        path_to_save = os.path.join(BASE_DIR, "dashboard/static/chart_storage/wordcloud_images"),
                        script_path = os.path.join(BASE_DIR, "dashboard/views/chart_generator_scripts/chart_wordcloud.py"), 
                        output_name = 'wordcloudio', instituicoes = []):
        # Gera grafico dinamicamente das patentes nos ultimos anos e salva, 'output_name.png', com 20 palavras!
        # o arquivo roda a partir do src! por isso o caminho do script é tomado a partir de cd src
        amount = 20
        
        output_name = GraphicProducerDashboardView.generate_output_name("wordcloud", instituicoes)

        if output_name is None:
            return 0

        #logger.debug(f"output_name = {output_name}")

        # Verifica se a pasta de armazenamento de gráficos está cheia
        if GraphicProducerDashboardView.is_graphic_storage_full(path_to_save):
            logger.error(f"Graphic storage is full")
            return 0

        if GraphicProducerDashboardView.is_in_graphic_storage(output_name + ".png", path_to_save):
            return "/static/chart_storage/wordcloud_images/" + output_name + ".png"
            # return HttpResponse(f"Wordcloud already exists: {output_name}", status=200)

        if not dataset:
            # return HttpResponse(f"Wordcloud dataset empty")
            return 0

        if dataset:
            result = subprocess.run(
                [
                    "python3",
                    script_path,
                    "--amount",
                    str(amount),
                    "--dataset",
                    str(dataset),
                    "--path_to_save",
                    path_to_save,
                    "--output_name",
                    output_name,
                ],
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            if result.returncode == 0:
                logger.debug(f"Wordcloud generated successfully: {result.stdout}")
                return "/static/chart_storage/wordcloud_images/" + output_name + ".png"
                # return HttpResponse(f"Script ran successfully: {result.stdout}")
            else:
                logger.error(f"Error running script: {result.stderr}")
                return 0
                # return HttpResponse(f"Error running script: {result.stderr}", status=500)
