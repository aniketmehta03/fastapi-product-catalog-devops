# Product Catalog Backend – Docker Containerization

This repository contains the **containerized backend service for a Product Catalog application** built using **FastAPI and MongoDB**.

The implementation focuses on **Task 3: Containerization and Local Orchestration with Docker** from the Unified Technical Assessment.

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
