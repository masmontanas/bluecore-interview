# Async Counter API

A minimal FastAPI application that increments a counter in Redis using a service-oriented architecture and circuit breaker pattern. Designed to be robust, containerized, and production-ready.

---

## 🧰 Features

- ✅ Circuit breaker for Redis to gracefully handle outages.
- ✅ Environment-specific configuration via `config.yaml` + environment variable support for sensitive values.
- ✅ JSON-structured logging.
- ✅ Graceful shutdown with Redis cleanup.
- ✅ Kubernetes deployment-ready (for testing via minikube).
- ✅ Pytest-based unit testing.
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

## Reviewer notes

Most of the time and attention was applied toward making the application itself robust, as well as providing
the building blocks for the k8s configuration that would be required for a production deployment.

Though the k8s resources are defined in a manifest file, it should outline all the necessary configuration options
for a production-ready deployment (probes, secure runtime config, hpa, etc.)

In a situation where the app would need to be developed under a time constraint to hand off to a more junior developer,
the basic building blocks and reference material would be there, allowing the colleague to focus on:
- CI/CD
  - Publishing the image to a remote registry
  - Release management with integration testing wired up
- linting
- type-checking
- configuration management
- Creating a helm chart, or using a CD tool like ArgoCD
- Writing integration tests to run during release

### Exposing this service publicly

In order to properly expose this service for public use, the following would be needed at a minimum.

1. An ingress or api resource, to expose the service via a public ip.
2. A TLS certificate, preferably through an integration with LetsEncrypt (via CertManager) or an equivalent service.

### Additional Security Considerations

Configuration options are currently defined for each environment in the config.yaml file.
However, support has been added to allow overwriting sensitive values with environment variables,
with the expectation being that a k8s secret resource would contain sensitive values and be mounted as env-variables.

Redis connectivity isn't currently protected with a password, which would not be viable for production.
