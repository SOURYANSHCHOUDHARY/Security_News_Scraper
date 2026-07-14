#!/bin/sh
set -e

echo "======================================="
echo " Threat Intelligence Dashboard "
echo "======================================="

echo "Running scraper..."
python app.py || echo "Scraper failed. Starting dashboard with existing database."

echo "Starting Streamlit..."

streamlit run dashboard.py \
  --server.address=0.0.0.0 \
  --server.port=${PORT:-8501}