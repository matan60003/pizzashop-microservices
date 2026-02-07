# EX3 - Full-Stack Microservices Architecture

## Overview

A local microservices product featuring:

- **FastAPI Backend**: Core logic and data management.
- **SQLModel Persistence**: SQLite-backed permanent storage.
- **Async Worker**: Processes orders via Redis with retry logic.
- **Security**: JWT-protected routes and hashed credentials.

## Async & Idempotency

- **Worker**: Listens to `pizza_tasks` on Redis.
- **Retries**: Implements a 3-attempt retry strategy for failed background tasks.
- **Tracing**: Redis/Logfire excerpts included in demo logs.

## Security Baseline

- **Hashing**: Passlib/Bcrypt for safe password storage.
- **JWT**: Token-based access to `POST /items`.
