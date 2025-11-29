import os
import csv
from api.models.scrapper_data import ScrapperBooks
from api.models.user import db
from api.__init__ import create_app

app = create_app()

# pega o caminho absoluto da pasta onde o script está
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "data", "books.csv")

def importar_csv(caminho_csv):
    with app.app_context():
        with open(caminho_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                novo_registro = ScrapperBooks(**row)
                db.session.add(novo_registro)

            db.session.commit()

        print("Importação concluída!")

importar_csv(csv_path)
