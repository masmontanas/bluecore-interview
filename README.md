# Async Counter API

A minimal FastAPI application that increments a counter in Redis using a service-oriented architecture and circuit breaker pattern. Designed to be robust, containerized, and production-ready.

---

## 🧰 Features

- ✅ Circuit breaker for Redis to gracefully handle outages
- ✅ Environment-specific configuration via `config.yaml` + environment variables
- ✅ JSON-structured logging
- ✅ Graceful shutdown with Redis cleanup
- ✅ Kubernetes deployment-ready (for testing via minikube)
- ✅ Pytest-based unit testing
---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.9+
- Docker and docker-compose
- Minikube (optional, for local Kubernetes testing)

### Environment Setup
_Syntax will vary by OS_

1. Create a new python virtual environment.
2. Activate the virtual environment.
3. Install requirements

## Testing

Unit tests (which have no external dependencies) are located in the `/tests` directory,
and integration tests should be added to `/integration_tests`.

### Running tests locally

```bash
# From the root directory
pytest tests
```


### Running the application locally using docker

```bash

# Application will be accessible over http://localhost:8080/docs
docker-compose up

# To tear it down
docker-compose down
```

### Running the application locally using minikube

```bash
minikube start

# Ensure k8s context is set to minikube
kubectl config use-context minikube

# From root directory of repo
minikube image build -t counter-api:latest .
kubectl apply -f k8s/counter-app

# Test using a port-forward and navigate to http://localhost:8080/docs
kubectl port-forward service/counter-api 8080:808

```

