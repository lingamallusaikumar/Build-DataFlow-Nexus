# DataFlow Nexus
Real-Time Data Pipeline & Intelligence Platform

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install
```

## Build
```bash
docker-compose build
```

## Run
```bash
docker-compose up -d
python run.py
```

## Dependencies
- Python 3.12+
- Flask, SQLAlchemy, Celery, Redis
- Node.js (for UI dependencies)

## Usage
Navigate to http://localhost:5000/dashboard to access the UI.
