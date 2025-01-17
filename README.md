# Bitcoin Price Tracker

A web application that displays Bitcoin price charts using React and Flask, deployed on Google Kubernetes Engine (GKE).

## Important Disclosure

This application was primarily developed with the assistance of an AI agent (Claude) through the Cursor IDE. While the code is functional and follows best practices, potential users should:
- Review and test the code thoroughly before use in production
- Be aware that the AI-generated code may have limitations or unforeseen issues
- Understand that security and performance characteristics may need additional validation
- Note that while the code is MIT licensed, some components may be derivative of training data

## Prerequisites

- Docker
- Google Cloud SDK
- kubectl
- Node.js 18+
- Python 3.11+

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Deployment to GKE

1. Set up Google Cloud Project:
```bash
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
```

2. Build and push Docker images:
```bash
# Backend
cd backend
docker build -t gcr.io/$PROJECT_ID/bitcoin-price-backend:latest .
docker push gcr.io/$PROJECT_ID/bitcoin-price-backend:latest

# Frontend
cd ../frontend
docker build -t gcr.io/$PROJECT_ID/bitcoin-price-frontend:latest .
docker push gcr.io/$PROJECT_ID/bitcoin-price-frontend:latest
```

3. Create GKE cluster:
```bash
gcloud container clusters create bitcoin-price-cluster \
    --num-nodes=2 \
    --zone=us-central1-a \
    --machine-type=e2-medium
```

4. Apply Kubernetes configurations:
```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

5. Get the external IP:
```bash
kubectl get service bitcoin-price-frontend
```

The application will be accessible at the external IP address provided by the LoadBalancer service.

## Architecture

- Frontend: React with Material-UI and Recharts for data visualization
- Backend: Flask API fetching data from CoinGecko
- Infrastructure: Google Kubernetes Engine with LoadBalancer service

## Monitoring

Monitor the application using Google Cloud's operations suite:
- Kubernetes Engine monitoring
- Cloud Monitoring dashboards
- Cloud Logging

## Security Notes

- The application uses CORS to allow frontend-backend communication
- Backend API is internal to the cluster
- Frontend is exposed via LoadBalancer with HTTPS recommended for production
