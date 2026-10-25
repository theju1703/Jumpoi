#!/usr/bin/env bash
# ====================================================================
# Deploy Jompoi ETL Pipeline to Google Cloud Functions (2nd Gen)
# ====================================================================

set -e

PROJECT_ID="${1:-$GCP_PROJECT}"
REGION="${2:-us-central1}"
FUNCTION_NAME="${3:-jompoi-mongo-bq-sync}"
DATASET_ID="${4:-jompoi_reporting}"

if [ -z "$PROJECT_ID" ]; then
    echo "Error: GCP Project ID is required. Pass it as the first argument or set GCP_PROJECT."
    exit 1
fi

echo "Deploying ${FUNCTION_NAME} to Google Cloud (Project: ${PROJECT_ID}, Region: ${REGION})..."

gcloud functions deploy "${FUNCTION_NAME}" \
    --gen2 \
    --runtime=python311 \
    --region="${REGION}" \
    --source=./cloud_function \
    --entry-point=sync_to_bigquery \
    --trigger-http \
    --allow-unauthenticated \
    --set-env-vars="MONGO_URI=${MONGO_URI},BQ_PROJECT_ID=${PROJECT_ID},BQ_DATASET_ID=${DATASET_ID},MONGO_DB_NAME=jompoi_db" \
    --project="${PROJECT_ID}"

echo "Cloud Function deployed successfully."
