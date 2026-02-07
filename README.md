# Pizza Order API - EX1

This is a simple FastAPI application for managing pizza orders, running inside a Docker container.

## Project Structure

- `main.py`: The FastAPI application with CRUD endpoints.
- `test_main.py`: Pytest suite for testing the API endpoints.
- `Dockerfile`: Instructions to containerize the application.
- `requirements.txt`: List of required Python packages.

## How to build the image

docker build -t pizza-app .

## How to run the container

docker run -p 8000:8000 pizza-app

## API Endpoints

- **GET /items**: Returns all pizza orders.
- **POST /items**: Create a new pizza order.
- **PUT /items/{id}**: Update an existing order.
- **DELETE /items/{id}**: Remove an order.

## How to Run Tests (Pytest)

pytest

## Example Call (Using Curl)

curl -X GET http://127.0.0.1:8000/items

# EX2

## Project Structure

- **/backend**: FastAPI server (Port 8000)
- **/frontend**: Nginx web server (Port 8080)

## How to Run

1. **Start Backend**:

   - `cd backend`
   - `docker build -t pizza-backend .`
   - `docker run -d -p 8000:8000 pizza-backend`

2. **Start Frontend**:
   - `cd frontend`
   - `docker build -t pizza-frontend .`
   - `docker run -d -p 8080:80 pizza-frontend`

## Testing

Run `pytest` inside the `/backend` folder to verify the API.

## Features

- View all pizza orders from the database (GET).
- Add new pizza orders via a web form (POST).
- Fully containerized environment.
