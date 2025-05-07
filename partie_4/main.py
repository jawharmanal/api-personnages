from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modèle pour les personnages reçus
class PersonnageScore(BaseModel):
    nom: str
    score: int

# Route POST /traitement
@app.post("/traitement")
def traitement(personnage: PersonnageScore):
    if personnage.score >= 90:
        niveau = "élite"
    elif personnage.score >= 75:
        niveau = "expert"
    else:
        niveau = "standard"

    return {
        "nom": personnage.nom,
        "score": personnage.score,
        "niveau": niveau
    }
