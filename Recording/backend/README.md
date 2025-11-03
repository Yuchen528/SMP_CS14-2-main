# 🐍 Backend Service

## 1. Project Overview
This service expose RESTful API to See Me Please recording tool and video analysis tool from the Vue 
frontend. These APIs include:
- Create, list, and get **projectTask.json** from S3 bucket;
- Save recording files(**Screen, Camera, and Audio**) and user data to S3 bucket;
- Get the analysis results(**Heatmap**) from S3 bucket;
- Get and analyze the recording files, and save the results to S3 bucket. (**❗Not Implement Yet❗**)

For the backend, our group was divided into two sub groups(recording tool and analysis). The recording tool 
sub group was responsible to develop APIs, but the APIs for analysis are not completed due to the time limited.

## 2. Technology Stack
- **Language & Framework:** Python 3.9+, Flask  
- **API Tool:** Flask-RESTful  
- **Testing:** pytest, pytest-flask, moto
- **AWS SDK:** boto3 

## 3. Repository Layout
```text
backend/
├── venv/               # Python virtual environment
├── app.py              # Flask application entrypoint
├── s3_client.py        # Helper module for AWS S3 operations
├── requirements.txt    # Python dependencies
├── tests/              # Automated tests
│ ├── conftest.py       # pytest fixtures (app, client, DummyS3)
│ └── api_test.py       # CRUD API tests
└── README.md           # This file
```

## 4. Running the Service
1. source venv/bin/activate (#macOS/Linux)
**or** .\venv\Scripts\Activate (#Windows)
2. export FLASK_APP=app.py
3. flask run --host=0.0.0.0 --port=5000
**or** pytest -q -s --disable-warnings --maxfail=1

## 5. API Endpoints
- **projectTask:** /api/projectTask/*
- **recording result:** /api/recording/*
- **visualization:** /api/visualization/*
- **analysis:** **❗Not Implement Yet❗**

## 6. Troubleshooting
- **403 Forbidden:** Check your IAM policy allows s3:PutObject and s3:GetObject.
Verify AWS keys in **s3_client.py**.
- **Content Mixed:** For AWS deployment, the service applys HTTP protocol, and 
the frontend applys HTTPS protocol in this project. 

## 7. License & Maintainer
License: MIT

Maintainer: Huaxiao.Huang ‹huaxiao.huang19@gmail.com›, Liangyu.zhang