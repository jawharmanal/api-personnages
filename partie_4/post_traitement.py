import requests
import json

# Lire les données nettoyées depuis fichier_clean.json (de la partie 2)
with open("partie2/fichier_clean.json", "r", encoding="utf-8") as f:
    personnages = json.load(f)

# Pour chaque personnage, construire le payload et l’envoyer à /traitement
for p in personnages:
    payload = {
        "nom": p.get("name", "inconnu"),
        "score": p.get("total_revenue", 0)
    }

    response = requests.post("http://localhost:8000/traitement", json=payload)

    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['nom']} → {result['niveau']} (score : {result['score']})")
    else:
        print(f"❌ Erreur pour {payload['nom']} : {response.status_code}")
