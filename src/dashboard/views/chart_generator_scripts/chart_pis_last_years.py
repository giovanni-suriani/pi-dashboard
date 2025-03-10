import pandas as pd
import altair as alt
import argparse
# Importing the stylable_container from streamlit_extras package
import json
import matplotlib.pyplot as plt
import sys
import os
import django
four_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(four_levels_up)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pi_dashboard.settings')
django.setup()
from django.conf import settings
BASE_DIR = settings.BASE_DIR


def paletas_cores():
    L_BLUE = "#00FFFC"
    L_GREEN = "#83FF00"
    L_PURPLE = "#7C00FF"
    L_ORANGE = "#FF0003"

    LIGHT_THEME = [L_BLUE, L_GREEN, L_PURPLE, L_ORANGE]

    # PALETA ANALOGA
    M_LBLUE = "#00FFFC"
    M_MBLUE = "#00B2FF"
    M_HBLUE = "#0062FF"
    M_LGREEN = "#0DFFA9"
    M_HGREEN = "#0FFF58"

    ANALOGOUS_THEME = [M_LBLUE, M_MBLUE, M_HBLUE, M_LGREEN, M_HGREEN]

    # PALETA DE CORES ESCURO (DRACULA)
    D_BACKGROUND_COLOR = "#282A36"
    D_FOREGROUND = "#F8F8F2"
    D_CYAN = "#8BE9FD"
    D_GREEN = "#50FA7B"
    D_ORANGE = "#FFB86C"
    D_PINK = "#FF79C6"
    D_PURPLE = "#FF79C6"
    D_RED = "FF5555"
    D_YELLOW = "#F1FA8C"

    DARK_THEME = [
        D_CYAN,
        D_GREEN,
        D_ORANGE,
        D_PINK,
        D_PURPLE,
        D_RED,
        D_YELLOW,
        D_FOREGROUND,
        D_BACKGROUND_COLOR,
    ]

    return LIGHT_THEME, ANALOGOUS_THEME, DARK_THEME

def adicionando_pis_falsas(acumulado_pis):
    # Debug purpose
    acumulado_pis[2019]["Marca"] += 4
    acumulado_pis[2019]["Desenho Industrial"] += 1
    acumulado_pis[2019]["Programa de  Computador"] += 1
    acumulado_pis[2020]["Programa de  Computador"] += 4
    acumulado_pis[2020]["Marca"] += 8
    acumulado_pis[2020]["Desenho Industrial"] += 8
    acumulado_pis[2021]["Programa de  Computador"] += 10
    acumulado_pis[2021]["Desenho Industrial"] += 8
    acumulado_pis[2021]["Marca"] += 2
    acumulado_pis[2022]["Marca"] += 10
    acumulado_pis[2023]["Marca"] += 2
    acumulado_pis[2024]["Desenho Industrial"] += 8
    acumulado_pis[2024]["Programa de  Computador"] += 10

# Testando display de propriedade Intelectual
def get_acumulado_publicado_tipo_pi_por_ano(lista_pis):
    # Defasado, nao esta sendo usado
    # Retorna um dicionario, as chaves sao os anos e os valores sao um dicionario com o tipo_pi e a quantidade de pi's
    dict_acumulado = {}
    for pi in lista_pis:
        if pi["data_publicacao"].year not in dict_acumulado.keys():
            dict_acumulado[pi["data_publicacao"].year] = {
                "Patente": 0,
                "Programa de  Computador": 0,
                "Marca": 0,
                "Desenho Industrial": 0,
            }
            dict_acumulado[pi["data_publicacao"].year][pi["tipo_pi"]] += 1
        else:
            dict_acumulado[pi["data_publicacao"].year][pi["tipo_pi"]] += 1
    return dict_acumulado

def get_acumulado_gasto_tipo_pi_por_ano(lista_pis):
    # Defasado, nao esta sendo usado
    # Retorna um dicionario, as chaves sao os anos e os valores sao um dicionario com o tipo_pi e o gasto dela
    dict_acumulado = {}
    for pi in lista_pis:
        if pi["data_publicacao"].year not in dict_acumulado.keys():
            dict_acumulado[pi["data_publicacao"].year] = {
                "Patente": 0,
                "Programa de  Computador": 0,
                "Marca": 0,
                "Desenho Industrial": 0,
            }
            dict_acumulado[pi["data_publicacao"].year][pi["tipo_pi"]] += 1
        else:
            dict_acumulado[pi["data_publicacao"].year][pi["tipo_pi"]] += 1
    return dict_acumulado

def grafico_pi_publicadas(paleta , dataset, ano_inicio=2019, ano_fim=2024, pis_falsas=True, width=600, height=228):
    
    if not paleta:
        paletas = paletas_cores()
        paleta = paletas["ANALAGOUS_THEME"]
    array_de_datas = [i for i in range(ano_inicio, ano_fim+1, 1)]
    # Fazendo o DataFrame
    df = pd.DataFrame(
        {
            "Ano": [
                array_de_datas[i]
                for i in range(0, len(array_de_datas), 1)
                for key in [
                    "Patente",
                    "Marca",
                    "Programa de  Computador",
                    "Desenho Industrial",
                ]
            ],
            "Quantidade Publicada": [
                dataset[str(i)][key]
                for i in range(array_de_datas[0], array_de_datas[-1] + 1)
                for key in [
                    "Patente",
                    "Marca",
                    "Programa de  Computador",
                    "Desenho Industrial",
                ]
            ],
            # Definindo Label
            "Tipo_Pi": [
                key
                for i in range(array_de_datas[0], array_de_datas[-1] + 1)
                for key in [
                    "Patente",
                    "Marca",
                    "Programa Computador",
                    "Desenho Industrial",
                ]
            ],
        }
    )
    # Fazendo o Grafico
    
    chart = (
        alt.Chart(
            df,
            title=alt.Title(
                "Pi's Publicadas últimos "+str(ano_fim - ano_inicio + 1)+" Anos",
                orient="top",
                offset=20,
            ),
        )
        .mark_bar() #size = 20
        .encode(
            x=alt.X("Ano:O")
            .scale(paddingInner=0.1, paddingOuter=0)
            .title(None),  # Adjust padding to diminish gap),  # 'O' for ordinal data
            xOffset=alt.XOffset("Tipo_Pi:N").scale(
                paddingInner=0.1, paddingOuter=0.4
            ),  # Offset bars based on 'Type' (categorical data
            y=alt.Y("Quantidade Publicada").axis(labelFontWeight="bold"),
            color=alt.Color("Tipo_Pi:N")
            .scale(range=paleta)
            .legend(orient="bottom", title=None),  # Custom color palette, title = none
            tooltip=["Tipo_Pi", "Quantidade Publicada"],
        )
        .configure_axis(labelFontWeight="bold", titleFontSize=18)
        .configure_legend(titleFontSize=15, labelFontSize=15, labelLimit=0)
        .properties(
            width=width,
            height=height,
        )
    )
    return chart

def main(theme, dataset, ano_inicio, ano_fim, path_to_save = "dashboard/static", output_name = "pisGrafico"):
    
    paletas = {}
    paletas["LIGHT_THEME"], paletas["ANALOGOUS_THEME"], paletas["DARK_THEME"] = paletas_cores()
    dataset = json.loads(dataset) # Pis publicadas por ano por tipo!
    if not dataset:
        print("Dataset vazio")
        
    #print(dataset['2023'])
    
    pis_chart = grafico_pi_publicadas(paletas[theme], dataset, ano_inicio, ano_fim)

    # Save the figure as an HTML file
    pis_chart.save(path_to_save + "/"+ output_name +".html", embed_options={'renderer':'svg'}) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate PI charts.')
    parser.add_argument('--theme', type=str, required=True, help='Theme for the chart (e.g., LIGHT_THEME, ANALOGOUS_THEME, DARK_THEME)')
    parser.add_argument('--dataset', required=True, help='Dataset to be used in the chart')
    parser.add_argument('--ano_inicio', type=int, required=True, help='Initial year for the chart')
    parser.add_argument('--ano_fim', type=int, required=True, help='Final year for the chart')
    parser.add_argument('--path_to_save', type=str, required=False, help='Path to save the chart')
    parser.add_argument('--output_name', type=str, required=False, help='Output name for the chart')
    # parser.add... output_name
    args = parser.parse_args()
    main(args.theme, args.dataset, args.ano_inicio, args.ano_fim, args.path_to_save, args.output_name)



#with st.container(border=False):
#    st.markdown("This is a container with a border.")
#    st.altair_chart(pis_chart, theme=None)
#st.write("Sample text")

# text = chart.mark_text(
#    align="center",
#    baseline="middle",r
#    dx=60,
# ).encode(
#    text="Quantidade_Publicada"
# )


# print(propriedade_dict.values())
# print(objeto_display[0].tipo_pi.PATENTE)
# streamlit run app.py --server.headless true

# for index, row in df.iterrows():
#    for col in df.columns:
#        print(f"{col}: {row[col]}")
#    print("-" * 40)
