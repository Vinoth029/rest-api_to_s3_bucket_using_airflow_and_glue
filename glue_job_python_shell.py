import json
import time
import boto3
import requests
from datetime import datetime

# ------------------------------
# CONFIG
# ------------------------------
SECRET_NAME = "branch_analytics_api_secret"
REGION = "ap-south-1"
S3_BUCKET = "branch-analytics-raw"
PAGE_SIZE = 500
MAX_RETRIES = 3
SLEEP_BETWEEN_CALLS = 1  # seconds

# ------------------------------
# CLIENTS
# ------------------------------
secrets_client = boto3.client("secretsmanager", region_name=REGION)
s3_client = boto3.client("s3")

# ------------------------------
# LOAD SECRETS
# ------------------------------
secret_response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
secrets = json.loads(secret_response["SecretString"])

API_URL = secrets["base_url"]
API_TOKEN = secrets["api_token"]

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# ------------------------------
# PAGINATION LOGIC
# ------------------------------
page = 1
all_records = []

while True:
    params = {
        "page": page,
        "page_size": PAGE_SIZE
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                API_URL,
                headers=headers,
                params=params,
                timeout=60
            )
            response.raise_for_status()
            break
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise Exception(f"API failed after retries: {e}")
            time.sleep(2)

    payload = response.json()

    records = payload.get("data", [])
    if not records:
        print(f"No more records. Pagination ended at page {page}")
        break

    all_records.extend(records)
    print(f"Fetched page {page} with {len(records)} records")

    page += 1
    time.sleep(SLEEP_BETWEEN_CALLS)

# ------------------------------
# WRITE RAW DATA TO S3
# ------------------------------
load_date = datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

s3_key = (
    f"api_name=branch_metrics/"
    f"load_date={load_date}/"
    f"branch_metrics_{timestamp}.json"
)

s3_client.put_object(
    Bucket=S3_BUCKET,
    Key=s3_key,
    Body=json.dumps(all_records)
)

print(f"Successfully written {len(all_records)} records to s3://{S3_BUCKET}/{s3_key}")
