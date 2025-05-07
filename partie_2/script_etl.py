import requests
import json
import time

# Fonction ETL principale
def etl():
    toutes_donnees = []  # Stocke les résultats de toutes les pages
    page = 0  # On commence à la page 0

    while True:
        # URL avec pagination
        url = f"https://projects.propublica.org/nonprofits/api/v2/search.json?q=chat&page={page}"
        print(f"Requête page {page}...")

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                print(f"Erreur HTTP {response.status_code}")
                break

            data = response.json()

            # Si pas de résultats, on s'arrête
            if not data.get("organizations"):
                print("Plus de résultats.")
                break

            # On filtre les données utiles : ici, celles qui ont une ville définie
            page_filtrée = [
                org for org in data["organizations"]
                if org.get("city") and org.get("total_revenue", 0) > 0
            ]

            toutes_donnees.extend(page_filtrée)

            page += 1
            time.sleep(1)  # Pause entre les requêtes pour éviter de spammer l’API

        except requests.exceptions.Timeout:
            print("Timeout : serveur trop lent.")
            break
        except Exception as e:
            print(f"Erreur : {e}")
            break

    # Écrire les données dans un fichier JSON
    with open("fichier_clean.json", "w", encoding="utf-8") as f:
        json.dump(toutes_donnees, f, ensure_ascii=False, indent=2)

    print(f"{len(toutes_donnees)} organisations sauvegardées dans fichier_clean.json")


if __name__ == "__main__":
    etl()
