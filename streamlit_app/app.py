import streamlit as st
import pandas as pd
import requests


# 📌 Charger la liste des utilisateurs à partir du fichier CSV
@st.cache_data
def load_users():
    try:
        df = pd.read_csv("data/clicks_sample.csv")  # Remplace par le bon chemin si besoin
        user_ids = df["user_id"].unique().tolist()  # Extraire les IDs uniques
        return sorted(user_ids)  # Trier pour un affichage plus propre
    except Exception as e:
        st.error(f"Erreur lors du chargement des utilisateurs : {e}")
        return []


# 📌 Interface utilisateur
st.title("🔍 Système de Recommandation d'Articles")

# Sélection dynamique de l'utilisateur
user_ids = load_users()
if user_ids:
    user_id = st.selectbox("Sélectionnez votre ID utilisateur :", user_ids)
else:
    st.error("❌ Impossible de charger la liste des utilisateurs.")

# 📌 Lancer la recommandation si un ID est sélectionné
if st.button("Obtenir des recommandations"):
    url = f"https://VOTRE_AZURE_FUNCTION_URL/api/recommend_articles?user_id={user_id}"

    with st.spinner("🔍 Recherche des meilleurs articles..."):
        response = requests.get(url)

    if response.status_code == 200:
        st.subheader("📌 Articles recommandés :")
        recommendations = response.json()  # Supposons que l'API retourne une liste JSON
        for idx, article in enumerate(recommendations, start = 1):
            st.write(f"📖 **Article {idx}**: {article}")
    else:
        st.error("❌ Erreur dans la récupération des recommandations.")

