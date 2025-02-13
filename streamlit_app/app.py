import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# ✅ Charger les variables d'environnement
if os.path.exists(".env"):
    load_dotenv()
    st.sidebar.success("✅ Fichier .env chargé avec succès")
else:
    st.sidebar.warning("⚠️ Fichier .env non trouvé, utilisant les valeurs par défaut.")

# ✅ Définir l'URL de l'API en fonction du mode
USE_AZURE = os.getenv("USE_AZURE", "False").lower() == "true"

API_URL = os.getenv("AZURE_FUNCTION_URL")

if USE_AZURE:
    if API_URL:
        st.sidebar.info(f"🌍 Mode : **Déploiement Azure**\n🔗 API : {API_URL}")
    else:
        st.sidebar.error("❌ Erreur : AZURE_FUNCTION_URL non défini dans .env ou variables Azure.")
else:
    API_URL = "http://127.0.0.1:5000/api/recommend_articles"
    st.sidebar.warning("🖥️ Mode : **Local (Flask API)**")

# ✅ Charger la liste des utilisateurs depuis un fichier CSV stocké
@st.cache_data
def load_users():
    try:
        df = pd.read_csv("data/clicks_sample.csv")  # Vérifie que ce fichier existe dans `data/`
        user_ids = df["user_id"].unique().tolist()
        return sorted(user_ids)
    except FileNotFoundError:
        st.error("❌ Fichier `data/clicks_sample.csv` introuvable.")
        return []
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des utilisateurs : {e}")
        return []

# ✅ Interface utilisateur Streamlit
st.title("🔍 Système de Recommandation d'Articles")

# Sélection dynamique de l'utilisateur
user_ids = load_users()
if user_ids:
    user_id = st.selectbox("👤 Sélectionnez votre ID utilisateur :", user_ids)
else:
    st.error("❌ Impossible de charger la liste des utilisateurs.")

# ✅ Lancer la recommandation si un ID est sélectionné
if st.button("🎯 Obtenir des recommandations"):
    if not API_URL:
        st.error("❌ API non configurée. Vérifiez `AZURE_FUNCTION_URL` dans `.env` ou les variables d'Azure.")
    else:
        url = f"{API_URL}?user_id={user_id}"
        with st.spinner("🔍 Recherche des meilleurs articles..."):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                recommendations = response.json()

                if not recommendations:
                    st.warning("⚠️ Aucune recommandation disponible pour cet utilisateur.")
                else:
                    st.subheader("📌 Articles recommandés :")
                    for idx, article in enumerate(recommendations, start=1):
                        st.write(f"📖 **Article {idx}**: {article}")

            except requests.exceptions.Timeout:
                st.error("❌ Erreur : Délai d'attente dépassé pour l'API.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Erreur dans la récupération des recommandations : {e}")

