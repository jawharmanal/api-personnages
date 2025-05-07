# main.py
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

# ✅ Autoriser les requêtes CORS
origins = [
    "http://localhost:3000",  # Frontend React par exemple
    "http://127.0.0.1:5500",  # HTML + JS en local (ex: VSCode Live Server)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Tu peux mettre ["*"] pour tout autoriser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle
class Personnage(BaseModel):
    id: int
    nom: str
    equipe: str

# Données
personnages = [
    Personnage(id=1, nom="Olivier Atton", equipe="Nankatsu"),
    Personnage(id=2, nom="Thomas Price", equipe="Nankatsu")
]

# Endpoint protégé
@app.get("/personnages", response_model=List[Personnage])
def get_personnages(token: str = Header(...)):
    if token != "SECRET123":
        raise HTTPException(status_code=401, detail="Token invalide")
    return personnages
