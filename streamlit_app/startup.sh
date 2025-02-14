#!/usr/bin/env bash

mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# Lancer Streamlit sur le port qu’Azure alloue :
streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT
