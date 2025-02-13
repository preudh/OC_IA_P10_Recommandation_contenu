import azure.functions as func
import numpy as np
import pandas as pd
from shared.azure_blob import load_model, load_embeddings, load_clicks

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function principale pour générer des recommandations"""
    user_id = req.params.get("user_id")
    if not user_id:
        return func.HttpResponse("Veuillez spécifier un user_id", status_code=400)

    # Charger le modèle, les embeddings et les interactions utilisateur depuis Azure Blob Storage
    model = load_model()
    embeddings = load_embeddings()
    clicks_df = load_clicks()

    # Récupérer les articles consultés par l'utilisateur (exemple : dernière session)
    user_clicks = clicks_df[clicks_df["user_id"] == int(user_id)]["article_id"].tolist()

    if not user_clicks:
        return func.HttpResponse("Aucune interaction trouvée pour cet utilisateur.", status_code=404)

    # Récupérer les embeddings des articles consultés
    user_embeddings = embeddings[user_clicks]

    # Calculer la similarité (produit scalaire entre les embeddings)
    similarity_scores = np.dot(embeddings, user_embeddings.T).sum(axis=1)

    # Sélectionner les 5 articles les plus similaires
    recommended_indices = np.argsort(similarity_scores)[::-1][:5]

    return func.HttpResponse(str(recommended_indices.tolist()), status_code=200)

