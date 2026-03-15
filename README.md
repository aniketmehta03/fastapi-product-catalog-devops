# Product Catalog Backend 

# Task Coverage

This repository focuses primarily on **Task 3 – Containerization and Local Orchestration with Docker**, as discussed with the assignment coordinator.

## Task 1 – UI/UX Design and Frontend

The UI/UX design and frontend/mobile implementation were not included in this repository.  
Since the focus of my role is **DevOps engineering**, the implementation effort was directed toward backend containerization, infrastructure setup, and service orchestration.

## Task 2 – Backend API Development

A working FastAPI backend service is included in this repository.  
The current implementation models a **mobile app catalog API** and demonstrates:

- REST API development with FastAPI
- CRUD operations
- MongoDB integration
- Automatic API documentation using Swagger UI

This backend service serves as the application component required for **Task 3 containerization**.

---

# Task 3 – Containerization and Local Orchestration with Docker

## Objective

The objective of this task is to demonstrate the ability to:

- Containerize an application using Docker
- Manage multi-service environments
- Orchestrate services using Docker Compose
- Configure communication between services
- Persist database data using Docker volumes

---

# Services

The application consists of two services:

### FastAPI Application
- Implements REST API endpoints
- Handles product catalog operations
- Runs using **Uvicorn**

### MongoDB Database
- Stores application data
- Runs as a separate container
- Persists data using Docker volumes

---

# Dockerfile

The FastAPI backend is containerized using a **multi-stage Docker build**.

Key features:

- Lightweight base image (`python:3.12-slim`)
- Multi-stage dependency installation
- Non-root container user
- Exposes port `8000`
- Runs FastAPI using Uvicorn

---

# Docker Compose

The project uses **docker-compose** to orchestrate the application stack.

The compose configuration:

- Defines services for **FastAPI** and **MongoDB**
- Enables network communication between services
- Exposes the API on port `8000`
- Persists MongoDB data using Docker volumes

---

# Running the Application

Build and start the full stack using Docker Compose.

```bash
docker compose up --build
```

After the containers start successfully, the API will be available at:

**API Base URL**

http://localhost:8000

**Swagger API Documentation**

http://localhost:8000/docs



---

## Stopping the Services

To stop and remove the running containers:

```bash
docker compose down
```


## Kubernetes Deployment using Helm

In addition to Docker Compose, the application can also be deployed using **Helm on Kubernetes**.

Helm is used as a package manager for Kubernetes to simplify deployment and configuration.

---

# Task 4 – CI/CD Pipeline (GitHub Actions + ArgoCD)

## Objective

To set up a Continuous Integration/Continuous Delivery (CI/CD) pipeline for the containerized FastAPI application. The pipeline automates build, tagging, registry push, and deployment.

**Implementation choice:** This repository uses **GitHub Actions** for CI and **ArgoCD** for CD instead of Jenkins, with equivalent automation and the same principles (source control, build, tag, push, deploy).

## Pipeline Stages

### 1. Source Code Management

- **Trigger:** Push to `main` or `feature/devops-assignment-setup` when relevant files change (`Dockerfile`, `*.py`, `requirements.txt`).
- **Action:** GitHub Actions checks out the latest code from the repository using `actions/checkout@v3`.

### 2. Build

- The **Docker image** of the FastAPI application is built on every pipeline run.
- Build runs on GitHub-hosted `ubuntu-latest` runners.

### 3. Tagging

- The image is tagged with a **meaningful version**: the **Git commit SHA** (`${{ github.sha }}`), e.g. `username/backend-product-api:abc1234`.
- This gives every build a unique, traceable tag.

### 4. Push to Registry

- The built image is pushed to **Docker Hub** (or another container registry if configured).
- Authentication uses GitHub Secrets: `DOCKER_USERNAME` and `DOCKER_PASSWORD`.

### 5. Helm / ArgoCD Sync

- After push, the pipeline updates **Helm** `values.yaml` with the new image tag (commit SHA).
- The change is committed and pushed back to the repo, so **ArgoCD** can sync and deploy the new image to Kubernetes.

### 6. Basic Testing (Placeholder)

- The task required a placeholder for automated tests. A simple always-pass step can be added to the workflow (e.g. run a script or `echo "Tests passed"`) when you are ready to integrate real tests.

## Deliverables

| Requirement            | Delivered artifact                                                                 |
|------------------------|-------------------------------------------------------------------------------------|
| Pipeline script        | **`.github/workflows/dynamic.yml`** – GitHub Actions workflow (equivalent to Jenkinsfile) |
| Deployment             | **ArgoCD** – GitOps-based deployment; application manifest in **`argocd/api.yaml`**     |
| Documentation          | This **README** – pipeline stages and setup instructions                            |

## How to Set Up

### GitHub Actions (CI)

1. **Secrets** (Settings → Secrets and variables → Actions):
   - `DOCKER_USERNAME` – Docker Hub username (or registry username).
   - `DOCKER_PASSWORD` – Docker Hub password or access token.

2. **Workflow:** The workflow is in `.github/workflows/dynamic.yml`. It runs automatically on push to the configured branches when the specified paths change.

3. **Optional – test placeholder:** Add a step in the workflow, for example:
   ```yaml
   - name: Run tests (placeholder)
     run: echo "Tests passed"  # Replace with real test command later
   ```

### ArgoCD (CD)

1. **Install ArgoCD** in your Kubernetes cluster (see [ArgoCD docs](https://argo-cd.readthedocs.io/)).

2. **Apply the Application manifest:**
   ```bash
   kubectl apply -f argocd/api.yaml
   ```

3. **Configure the repo in ArgoCD** (if not using public repo): add the repository in ArgoCD and any required credentials.

4. **Sync:** With `syncPolicy.automated`, ArgoCD will sync when `helm/product-api` or `values.yaml` changes (e.g. after the CI pipeline updates the image tag).

### Summary

- **CI:** GitHub Actions builds the Docker image, tags with commit SHA, pushes to Docker Hub, and updates `helm/product-api/values.yaml`.
- **CD:** ArgoCD watches the repo and deploys the Helm chart to Kubernetes; new image tags from CI are picked up on the next sync.

Evaluation criteria addressed: pipeline configuration, CI/CD principles, Docker image tagging and registry push, and automation via GitHub Actions and ArgoCD.


