# 📌 On-Prem REST API to Amazon S3 (Raw Zone) using Airflow & AWS Glue

## 📖 Overview

This project demonstrates a **production-grade data ingestion pipeline** that pulls data from an **on-premise Branch Analytics Portal exposing a REST API** and stores the data in **Amazon S3 (Raw Zone)**.

The pipeline is **orchestrated using Apache Airflow** and uses an **AWS Glue Python Shell job** to securely fetch paginated API data using **AWS Secrets Manager** for authentication.

---

## 🏗 Architecture

**Flow:**

1. Apache Airflow triggers the AWS Glue job on a scheduled basis  
2. AWS Glue securely retrieves API credentials from AWS Secrets Manager  
3. Glue connects to the on-prem REST API via VPN / Direct Connect  
4. API data is fetched using pagination  
5. Raw JSON data is written to Amazon S3 with date-based partitioning  

**Key Design Principles:**
- Secure authentication
- Cost-optimized ingestion
- Raw zone immutability
- Retry and failure handling
- Audit-friendly storage

---

## 🧰 Technology Stack

| Component | Purpose |
|--------|--------|
| Apache Airflow | Orchestration & scheduling |
| AWS Glue (Python Shell) | REST API ingestion |
| AWS Secrets Manager | Secure credential storage |
| Amazon S3 | Raw data storage |
| AWS IAM | Access control |
| CloudWatch | Logging & monitoring |

---

## 📁 S3 Data Layout

```text
s3://branch-analytics-raw/
└── api_name=branch_metrics/
    └── load_date=YYYY-MM-DD/
        └── branch_metrics_YYYYMMDD_HHMMSS.json
