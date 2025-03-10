## Pi-dashboard

## Descrição

O Pi-dashboard é um projeto de software que visa a criação de um painel de visualização de dados de propriedades intelectuais (PI): Quantidade de PIs por tipo (Marca, Desenho Industrial, Patente, Programa de Computador), os titulares e cotitulares da instituição com mais publicações, os inventores e coinventores com mais publicações,  um gráfico de barras com a quantidade de PIs por tipo publicadas ao longo dos anos e uma nuvem de tags com as palavras mais relevantes dos títulos de PIs.


## Instalação

### Banco de Dados

o desenvolvimento é possível usar os bancos de dados SQLite ou MySQL, todavia o MySQL é mais fidedigno a produção. Para
usar o SQLite crie o arquivo .env no diretório src e escreva o seguinte:

```dotenv
ENVIRONMENT="DEV"
```

Caso prefira usar o MySQL primeiro deve-se instalar as seguintes dependências:

```bash
sudo apt-get install libmysqlclient-dev
sudo apt install mysql-server
```

Depois de instaladas é necessário rodar o seguinte comando no bash para criar o banco de dados e configurar um usuário:

```bash
sudo mysql -u root
```

Após rodar o comando deve-se rodar as linhas abaixo no terminal que vai abrir. Onde `<db>` é o nome do banco de dados,
`<user>` é o nome do usuário, `<password>` é a senha do usuário e `<host>` é o host, em geral `localhost` para máquina pessoal.

```mysql
CREATE DATABASE <db>;
CREATE USER '<user>'@'<host>' IDENTIFIED WITH mysql_native_password BY '<password>';
GRANT ALL PRIVILEGES ON <db>.* TO '<user>'@'<host>';
```

Após isso, deve-se criar arquivo `.env`

```dotenv
ENVIRONMENT="DEV"
DATABASE="MYSQL"
DATABASE_NAME="<db>"
DATABASE_USER="<user>"
DATABASE_HOST="<host>"
```


### Ambiente virtual 

Crie o ambiente virtual e instale as dependencias no mesmo
Para criar o ambiente virtual, ativa-lo e instalar as dependencias use (crie-o dentro da pasta raiz do projeto, ou seja,
diretamente no pi-dashboard):

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Scripts Assíncronos

Neste projeto foi utilizado crontab para automatização das produção e deleção de gráficos mensais. Para utilizar esta função, verifique a permissão de execução para o arquivo faz_rotinas.sh e o execute.

```bash
chmod +x faz_rotinas.sh
./faz_rotinas.sh
```

## Documentação

### Fluxo de Execução

Ao realizar uma requisição `GET` para a rota `/` ou passando como argumentos as instituições responsáveis por PI `/?instituicoes=<instituicao1, instituicao2, ...>`, o servidor faz uma requisição `GET` para o serviço do sistema responsável por fornecer os dados de PIs (gestao-pi), no primeiro caso é retornado os dados considerando todas instituições cadastradas no sistema.

O serviço do sistema retorna um JSON com os dados de PIs, que são processados pelo servidor do Pi-dashboard.

No primeiro caso
``` 
data = {
        "instituicoes": instituicoes,
        "panel_name": panel_name,
        "top_titulares": top_titulares,
        "top_inventors": top_inventors,
        "pis_count": pis_count,
        "chart": chart
    }
```

No segundo caso
```
data = {
        "instituicoes": instituicoes,
        "panel_name": panel_name,
        "top_titulares": top_titulares,
        "top_inventors": top_inventors,
        "pis_count": pis_count,
        "pis_dataset": pis_dataset,
        "wordcloud_dataset": wordcloud_dataset,
        "chart": chart
    }
```

O servidor do Pi-dashboard processa os dados e renderiza o template dashboard_single.html ou dashboard_multi.html dependendo da quantidade de instituições retornadas. Os gráficos mostrados no painel estão na pasta `dashboard/static/chart_storage`, se a requisição foi feita sem argumentos, os gráficos pisGrafico.html e wordcloud.png são utilizados, caso contrário, os gráficos utilizados são identificados a partir das instituições utilizadas (ex:pisGrafico_CEFET-MG-2025-03.html). 

Caso seja utilizada a opção de filtro, o servidor do Pi-dashboard faz uma requisição assíncrona (ajax) `POST` para o serviço do sistema com os argumentos passados, que retorna um JSON com os dados de PIs filtrados que são processados e renderizados na página.

Todos os gráficos são gerados localmente a partir dos dados retornados pelo serviço (wordcloud_dataset e pis_dataset).

### Detalhamento, Arquivos, Classes e Funções mais relevantes

#### Views.py

#### Produção de Gráficos

#### Settings.py

#### Deleção e produção de gráficos assíncronos









