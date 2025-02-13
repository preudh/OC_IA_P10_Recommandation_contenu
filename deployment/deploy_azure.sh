#!/bin/bash

# Définition des variables
RESOURCE_GROUP="P9ResourceGroup"  # Ton groupe de ressources existant
STORAGE_ACCOUNT="p10reco2025"  # Ton compte de stockage
FUNCTION_APP_NAME="p10-reco-function"
LOCATION="westeurope"
RUNTIME="python"

echo "📌 Vérification de la connexion à Azure..."
az account show &>/dev/null
if [ $? -ne 0 ]; then
  echo "❌ Vous n'êtes pas connecté à Azure. Exécutez 'az login' et réessayez."
  exit 1
fi

echo "📌 Création de l'Azure Function App..."
az functionapp create \
  --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --name $FUNCTION_APP_NAME \
  --storage-account $STORAGE_ACCOUNT \
  --runtime $RUNTIME

if [ $? -eq 0 ]; then
  echo "✅ Function App $FUNCTION_APP_NAME créée avec succès."
else
  echo "❌ Échec de la création de la Function App."
  exit 1
fi

echo "📌 Déploiement de l'Azure Function..."
func azure functionapp publish $FUNCTION_APP_NAME

if [ $? -eq 0 ]; then
  echo "✅ Déploiement terminé avec succès !"
  echo "🌍 URL de l'API : https://$FUNCTION_APP_NAME.azurewebsites.net/api/recommend_articles"
else
  echo "❌ Échec du déploiement."
  exit 1
fi

