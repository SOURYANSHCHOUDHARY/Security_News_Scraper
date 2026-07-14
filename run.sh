#!/bin/sh
set -e

echo "======================================="
echo " Threat Intelligence Platform "
echo "======================================="

echo ""
echo "Creating database and collecting articles..."

python app.py

echo ""
echo "Starting Streamlit Dashboard..."

streamlit run dashboard.py \
    --server.address=0.0.0.0 \
    --server.port=8501