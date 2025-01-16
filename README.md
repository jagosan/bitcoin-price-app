# Bitcoin Price Tracker

A web application that displays Bitcoin price charts using React and Flask, deployed on Google Kubernetes Engine (GKE).

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