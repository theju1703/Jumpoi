# ====================================================================
# Deploy Jompoi ETL Pipeline to Google Cloud Functions (2nd Gen)
# ====================================================================

param (
    [string]$ProjectId = $env:GCP_PROJECT,
    [string]$Region = "us-central1",
    [string]$FunctionName = "jompoi-mongo-bq-sync",
    [string]$MongoUri = $env:MONGO_URI,
    [string]$DatasetId = "jompoi_reporting"
)

if (-not $ProjectId) {
    Write-Error "Please specify -ProjectId or set GCP_PROJECT environment variable."
    exit 1
}

if (-not $MongoUri) {
    Write-Warning "MONGO_URI is not set. Ensure your Cloud Function has network access to your MongoDB Atlas / VPC."
}

Write-Host "Deploying $FunctionName to GCP Project $ProjectId in region $Region..."

gcloud functions deploy $FunctionName `
    --gen2 `
    --runtime=python311 `
    --region=$Region `
    --source=./cloud_function `
    --entry-point=sync_to_bigquery `
    --trigger-http `
    --allow-unauthenticated `
    --set-env-vars="MONGO_URI=$MongoUri,BQ_PROJECT_ID=$ProjectId,BQ_DATASET_ID=$DatasetId,MONGO_DB_NAME=jompoi_db" `
    --project=$ProjectId

Write-Host "Deployment completed."
