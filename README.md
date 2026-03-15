# Product Catalog Backend 

# Task Coverage

This repository covers **Task 3 – Containerization and Local Orchestration with Docker**, **Task 4 – CI/CD Pipeline (GitHub Actions + ArgoCD)**, and **Task 5 – Cloud Deployment and Monitoring on AWS** (EKS with Terraform, Prometheus/Grafana/Loki).

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

---

# Task 5 – Cloud Deployment and Monitoring on AWS

## Objective

To deploy the containerized FastAPI application to AWS and implement basic monitoring. The task allows:

- **Option A (EC2 with Docker):** Provision an EC2 instance, install Docker, and run the application container.
- **Option B (AWS ECS/EKS):** Deploy using Elastic Container Service (ECS) or Elastic Kubernetes Service (EKS).

This repository implements **Option B – EKS**. The application is deployed to an **Amazon EKS cluster** provisioned with **Terraform**, with deployment and updates handled by **Helm** and **ArgoCD** (see Task 4). Monitoring is implemented using **Prometheus**, **Grafana**, and **Loki** (instead of AWS CloudWatch) to avoid CloudWatch costs while providing equivalent observability.

## Task Requirements Addressed

| Requirement | Implementation |
|-------------|----------------|
| Provision necessary AWS resources (EC2, VPC, Security Groups, IAM roles) | **Terraform** provisions VPC, EKS cluster, node groups, and IAM via AWS/EKS and VPC modules. |
| Application accessible via a public endpoint | Application is exposed via Kubernetes **Service** (and optional **Ingress**/Load Balancer). Public URL depends on your Ingress/LB configuration. |
| Basic monitoring (e.g. CPU, network, logs) | **Prometheus** (metrics), **Grafana** (dashboards), **Loki** (logs) installed via **Helm**. |

## Infrastructure as Code (Terraform)

All AWS resources for the EKS cluster are defined in the **`terraform/`** directory.

### Resources Provisioned

- **VPC** (`terraform/vpc.tf`): Custom VPC with public, private, and intra subnets across two AZs; NAT Gateway for private subnet egress.
- **EKS Cluster** (`terraform/eks.tf`): EKS cluster with public API endpoint; add-ons: CoreDNS, kube-proxy, VPC-CNI.
- **EKS Node Group**: Managed node group `bankapp-ng` (e.g. `t2.medium`, SPOT), min 2 / max 3 nodes.
- **Security Groups & IAM**: Handled by the official Terraform AWS EKS and VPC modules (node security groups, cluster access, etc.).

### Terraform Files

| File | Purpose |
|-----|--------|
| `terraform/versions.tf` | Terraform and provider version constraints (AWS, Kubernetes, Helm, etc.) |
| `terraform/provider.tf` | AWS provider configuration (region from variable) |
| `terraform/variables.tf` | Input variables (cluster name, region, VPC CIDR, subnets, AZs, tags) |
| `terraform/vpc.tf` | VPC module (subnets, NAT gateway, Kubernetes-related tags) |
| `terraform/eks.tf` | EKS module (cluster, node group, add-ons) |

### Deploying the EKS Cluster

1. **Prerequisites:** Terraform ≥ 1.5, AWS CLI configured with credentials that can create EKS, VPC, and IAM resources.

2. **Initialize and apply:**
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

3. **Configure kubectl:**
   ```bash
   aws eks update-kubeconfig --region <aws_region> --name <cluster_name>
   ```
   Default cluster name from variables: `product-api-Cluster-V1`; default region: `ap-south-1`.

4. **Deploy the application:** Use the Helm chart and ArgoCD as described in Task 4 (e.g. apply `argocd/api.yaml` and sync the `helm/product-api` chart).

## Deployment Scripts / Instructions

- **Container image:** Built and pushed by **GitHub Actions** (Task 4) to Docker Hub (or your configured registry).
- **Deployment to EKS:**  
  - **Helm chart:** `helm/product-api`  
  - **GitOps:** ArgoCD application in `argocd/api.yaml` points to this repo and the `helm/product-api` path; ArgoCD deploys/updates the app when the chart or `values.yaml` (e.g. image tag) changes.

To deploy manually with Helm (without ArgoCD):

```bash
helm upgrade --install product-api ./helm/product-api -f ./helm/product-api/values.yaml
```

Ensure MongoDB is running in the cluster (or adjust `values.yaml` for an external MongoDB). For full automation, use the CI/CD pipeline and ArgoCD as in Task 4.

## Public URL of the Deployed Application

The application runs inside the EKS cluster. To make it publicly accessible you can:

- Enable and configure **Ingress** in `helm/product-api/values.yaml` (e.g. with an Ingress controller like NGINX and a load balancer), or  
- Use a **LoadBalancer**-type Service and use the provided AWS DNS name.

The exact **public URL** will depend on your chosen Ingress/Load Balancer setup (e.g. `http://<load-balancer-dns>/` or `https://your-domain.com/`). After configuring it, document the URL here or in your submission as the **Public URL of the deployed application**.

## Monitoring: Prometheus, Grafana, and Loki

Instead of AWS CloudWatch (to avoid cost), **basic monitoring** is implemented with a standard Kubernetes observability stack:

- **Prometheus** – metrics collection (CPU, memory, pod counts, etc.)
- **Grafana** – dashboards and visualization
- **Loki** – log aggregation

This follows the approach: *Monitoring my Kubernetes application with Prometheus & Grafana* (with Loki for logs).

### Installing the Monitoring Stack (Helm)

The stack can be installed with Helm, for example:

- **Prometheus:** e.g. `helm install prometheus prometheus-community/kube-prometheus-stack` (or `prometheus` chart) in a dedicated namespace.
- **Grafana:** Often included in the same stack; otherwise install the Grafana Helm chart.
- **Loki:** e.g. `helm install loki grafana/loki-stack` or the Grafana Loki chart.

(Exact commands and values depend on the Helm repos and chart versions you use; run from your cluster after `terraform apply` and `aws eks update-kubeconfig`.)

### What Is Monitored in Grafana

After generating traffic to the FastAPI API, the following can be observed in Grafana:

- **CPU usage** of pods (e.g. product-api and MongoDB)
- **Memory consumption** of pods
- **Pod count and status** (running, pending, etc.)

Logs from the application and other workloads can be explored in Grafana by using **Loki** as a data source.

### Screenshots of Dashboards

As per the task deliverables, include **screenshots of your Grafana dashboards** (and optionally Prometheus/Loki) showing the basic monitoring metrics above. You can add them to the repo (e.g. in a `docs/` folder) and reference them in this README or in your submission.

