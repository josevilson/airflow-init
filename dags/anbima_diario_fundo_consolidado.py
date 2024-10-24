import os
from datetime import datetime
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

# Importações para Playwright
from playwright.sync_api import sync_playwright

# Definir o caminho onde o arquivo será salvo
# AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/opt/airflow/')
DOWNLOAD_DIR = "/usr/local/airflow/include/downloads"

# Criar a DAG usando a TaskFlow API
@dag(
    schedule_interval='@daily',  # Pode ajustar conforme necessário
    start_date=days_ago(1),
    catchup=False,
    tags=['anbima', 'playwright']
)
def download_anbima_funds():

    # Task para baixar o arquivo
    @task()
    def download_funds_file():
        # Inicializando o Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Acessando a página da ANBIMA
            page.goto("https://www.anbima.com.br/pt_br/informar/estatisticas/fundos-de-investimento/fi-consolidado-diario.htm")

            # Espera até o botão de download estar disponível e clica no botão
            page.wait_for_selector("[data-anbima-arquivo-contentid]")
            with page.expect_download() as download_info:
                page.click("[data-anbima-arquivo-contentid]")

            # Aguarda o download e pega o arquivo
            download = download_info.value
            
            file_path = os.path.join(DOWNLOAD_DIR,download.suggested_filename)
            print(os.getcwd())
            download.save_as(download.suggested_filename)

            # Fecha o browser
            browser.close()

            # Retorna o caminho do arquivo salvo
            return file_path

    # Task de impressão do caminho do arquivo
    @task()
    def print_file_path(file_path: str):
        print(f"Arquivo baixado e salvo em: {file_path}")

    # Definir a ordem das tarefas
    file_path = download_funds_file()
    print_file_path(file_path)

# Instanciar a DAG
download_anbima_funds_dag = download_anbima_funds()