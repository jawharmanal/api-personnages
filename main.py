# Importation des modules nécessaires
from fastapi import FastAPI, Header, HTTPException  # FastAPI et sécurité via Header
from fastapi.middleware.cors import CORSMiddleware  # Pour autoriser les appels du frontend
from typing import List  # Pour déclarer une liste typée
from pydantic import BaseModel  # Pour les modèles de données (validation)
import json  # Pour lire et écrire des fichiers JSON
from pathlib import Path  # Pour gérer les chemins de fichiers

# Création de l'application FastAPI
app = FastAPI()

# ---------------------- CORS ----------------------

# Origines autorisées à appeler l'API (ex : frontend React, fichier HTML local...)
origins = [
    "http://localhost:3000",       # Pour front React local
    "http://127.0.0.1:5500",       # Pour Live Server sur VSCode
    "file://"                      # Pour page HTML ouverte localement
]

# Activation de la gestion CORS dans l'application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Autorise ces domaines
    allow_credentials=True,
    allow_methods=["*"],          # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"]           # Autorise tous les headers (dont "token")
)

# ---------------------- Modèles ----------------------

# Modèle Pydantic pour un personnage (GET)
class Personnage(BaseModel):
    id: int
    nom: str
    equipe: str

# Modèle Pydantic pour un score (POST)
class Score(BaseModel):
    name: str
    city: str
    avis: str

# ---------------------- Chargement ou création du JSON ----------------------

# Chemin vers le fichier JSON contenant les personnages
chemin = Path(__file__).parent / "personnages.json"

# Si le fichier n'existe pas, on le crée automatiquement avec deux personnages
if not chemin.exists():
    print("⚠️ Fichier personnages.json non trouvé. Création automatique...")
    exemple_personnages = [
        {"id": 1, "nom": "Olivier Atton", "equipe": "Nankatsu"},
        {"id": 2, "nom": "Thomas Price", "equipe": "Nankatsu"}
    ]
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(exemple_personnages, f, ensure_ascii=False, indent=2)

# Lecture du fichier JSON (maintenant présent à coup sûr)
with open(chemin, "r", encoding="utf-8") as f:
    personnages = [Personnage(**p) for p in json.load(f)]

# ---------------------- Endpoints ----------------------

# ✅ Endpoint GET /personnages (protégé par un token)
@app.get("/personnages", response_model=List[Personnage])
def get_personnages(token: str = Header(...)):
    # Vérification du token
    if token != "SECRET123":
        raise HTTPException(status_code=401, detail="Token invalide")
    # Renvoie la liste des personnages
    return personnages

# ✅ Endpoint POST /scores (reçoit un score et le log en console)
@app.post("/scores")
def post_scores(score: Score, token: str = Header(...)):
    # Vérification du token
    if token != "SECRET123":
        raise HTTPException(status_code=401, detail="Token invalide")
    
    # Affichage du score reçu dans la console
    print(f"✅ Score reçu : {score}")
    
    # Retourne un message de confirmation
    return {"message": "Score reçu", "data": score}
