from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path

# Initialisation de l'application
app = FastAPI()

# ---------------------- Modèle de données ----------------------

# Modèle pour les personnages reçus via webhook
class WebhookPersonnage(BaseModel):
    nom: str
    score: int

# ---------------------- Chemins des fichiers ----------------------

# Fichier JSON pour historiser les personnages
log_file = Path(__file__).parent / "webhook_log.json"

# Fichier texte pour simuler une notification
notif_file = Path(__file__).parent / "notifications.txt"

# Si le fichier JSON n'existe pas, on le crée vide
if not log_file.exists():
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump([], f)

# ---------------------- Route Webhook ----------------------

@app.post("/webhook/personnage")
async def recevoir_personnage(data: WebhookPersonnage):
    # Déterminer le niveau en fonction du score
    niveau = "élite" if data.score >= 90 else "standard"

    # Créer l'événement complet
    evenement = {
        "nom": data.nom,
        "score": data.score,
        "niveau": niveau
    }

    # 🔹 Étape 1 : Enregistrement dans webhook_log.json
    with open(log_file, "r", encoding="utf-8") as f:
        historique = json.load(f)
    historique.append(evenement)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(historique, f, indent=2, ensure_ascii=False)

    # 🔹 Étape 2 : Écrire une ligne de notification dans notifications.txt
    message = f"⚡ Notification : {data.nom} ({niveau}) ajouté avec score {data.score}\n"
    with open(notif_file, "a", encoding="utf-8") as f:
        f.write(message)

    # Affichage dans la console
    print(f"📥 Webhook reçu : {evenement}")
    print(message.strip())

    # Réponse renvoyée à l’expéditeur
    return {
        "status": "ok",
        "message": "Personnage enregistré et notification envoyée",
        "data": evenement
    }
