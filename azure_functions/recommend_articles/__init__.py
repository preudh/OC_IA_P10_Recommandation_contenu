
import azure.functions as func
import numpy as np
import pandas as pd
import json

from azure_functions.shared.azure_blob import load_model, load_embeddings, load_clicks


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function for article recommendations."""
    try:
        user_id = req.params.get("user_id")
        if not user_id:
            return func.HttpResponse(
                "Missing parameter: user_id",
                status_code=400
            )

        # Convert user_id to int
        try:
            user_id = int(user_id)
        except ValueError:
            return func.HttpResponse(
                "Invalid user_id parameter. It must be an integer.",
                status_code=400
            )

        # Load model, embeddings, and user clicks
        # NOTE: remove load_model() if you do not actually use the ALS model
        model = load_model()
        embeddings = load_embeddings()
        clicks_df = load_clicks()

        # Get all articles clicked by the user
        user_clicks = clicks_df[clicks_df["user_id"] == user_id]["article_id"].tolist()

        if not user_clicks:
            return func.HttpResponse(
                "No interactions found for this user.",
                status_code=404
            )

        # Retrieve embeddings for user clicked articles
        # Check that embeddings is a NumPy array or handle dictionary appropriately
        user_embeddings = embeddings[user_clicks]

        # Compute similarity (dot product)
        similarity_scores = np.dot(embeddings, user_embeddings.T).sum(axis=1)

        # Select the top 5 most similar articles
        recommended_indices = np.argsort(similarity_scores)[::-1][:5]

        # Optionally, exclude articles already clicked by user
        # recommended_indices = [idx for idx in recommended_indices if idx not in user_clicks]

        # Return recommendations as valid JSON
        return func.HttpResponse(
            json.dumps(recommended_indices.tolist()),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            f"Server error: {str(e)}",
            status_code=500
        )


