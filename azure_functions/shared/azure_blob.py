import io
import numpy as np
import pickle
import pandas as pd
import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

# 🔹 Charger les variables d'environnement
load_dotenv()

# 🔹 Récupérer les informations d'authentification
tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT")

# 🔹 Se connecter à Azure Blob Storage avec Service Principal
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=credential
)

# 🔹 Conteneur où sont stockés les fichiers
CONTAINER_NAME = "models"

def load_blob(blob_name):
    """
    Charge un fichier depuis Azure Blob Storage.

    :param blob_name: Nom du fichier dans le conteneur Azure Blob.
    :return: Contenu brut du fichier.
    """
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    return blob_client.download_blob().readall()

def load_model():
    """
    Charge le modèle ALS stocké sur Azure Blob Storage.

    :return: Modèle ALS sous forme d'objet NumPy.
    """
    model_data = load_blob("als_implicit_model.npz")
    with io.BytesIO(model_data) as f:
        return np.load(f, allow_pickle=True)

def load_embeddings():
    """
    Charge les embeddings des articles depuis Azure Blob Storage.

    :return: Dictionnaire des embeddings chargé depuis un fichier Pickle.
    """
    embeddings_data = load_blob("articles_embeddings.pickle")
    with io.BytesIO(embeddings_data) as f:
        return pickle.load(f)

def load_clicks():
    """
    Charge les interactions utilisateurs (historique de clics) depuis Azure Blob Storage.

    :return: DataFrame Pandas contenant les données d'interactions.
    """
    clicks_data = load_blob("clicks_sample.csv")
    with io.BytesIO(clicks_data) as f:
        clicks_df = pd.read_csv(f)
    return clicks_df

