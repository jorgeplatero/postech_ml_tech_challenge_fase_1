from airflow.decorators import dag, task
from datetime import datetime
import subprocess
import logging


SCRAPER_SCRIPT = 'book_scraper.py'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@task
def run_scraper():
    """Executa o script de webscraping."""
    logging.info(f"Iniciando a execução do script: {SCRAPER_SCRIPT}")
    try:
        result = subprocess.run(
            ['python', SCRAPER_SCRIPT],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info(f"Scraper executado com sucesso. Saída:\n{result.stdout}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar o scraper: {e.stderr}")
        raise
    except FileNotFoundError:
        logging.error(f"Script '{SCRAPER_SCRIPT}' não encontrado. Verifique o path.")
        raise

@dag(
    dag_id='books_to_scrape',
    start_date=datetime(2025, 11, 25),
    schedule='@daily',
    catchup=False,
    tags=['webscraping', 'books'],
    doc_md='',
)
def book_scraping_dag():
    """
    DAG para automatizar o webscraping do Books to Scrape e persistir os dados 
    em um banco de dados no PostgreSQL.
    """
    scrape = run_scraper()
    scrape

book_scraping_dag()