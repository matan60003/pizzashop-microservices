# 🍕 Pizza Order System - EX3 (Full-Stack Microservices)


## 🚀 Project Overview

This project is a distributed pizza ordering system built with a Microservices architecture. It includes a FastAPI backend, an Nginx frontend, and an asynchronous task processing system using Redis and a background Worker.

### Key Features:

- **Microservices Orchestration**: All services run seamlessly using Docker Compose.
- **Asynchronous Processing**: Orders are sent to a **Redis** queue and processed by a dedicated **Worker** service.
- **Security**: Protected endpoints using **JWT (JSON Web Tokens)** authentication.
- **Advanced Export**: Detailed CSV export with **UTF-8-SIG** encoding for perfect Hebrew support in Excel.

---

## 🏗️ Project Structure

- **/backend**: FastAPI server (Port 8000) - Handles API logic, Auth, and DB.
- **/frontend**: Nginx web server (Port 8080) - User interface for placing orders.
- **Redis**: Message broker for task management.
- **Worker**: Background service that processes order tasks from Redis.
- **Database**: SQLite (SQLModel) for persistent storage.

---

## 🛠️ How to Run

The entire system is containerized. To start all services, run:

bash
docker compose up --build

Accessing the System:
Frontend (UI): http://localhost:8080

API Documentation (Swagger): http://localhost:8000/docs

📡 API Endpoints
POST /signup: Register a new user.

POST /login: Authenticate and receive a JWT Bearer Token.

GET /items: Retrieve all orders (Public).

POST /items: Create a new order (Secure - requires JWT).

GET /export-csv: Export all orders to a detailed CSV file (Secure - requires JWT).

🧪 Testing & Validation
Backend Tests: Run pytest inside the /backend directory.

Asynchronous Logs: Observe the worker logs in the terminal to verify background task processing.
