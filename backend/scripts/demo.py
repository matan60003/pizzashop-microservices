#!/bin/bash
echo "--- Starting EX3 Demo ---"
echo "1. Building and launching the stack..."
docker compose up -d --build
echo "2. Waiting for API to be healthy..."
sleep 5
echo "3. API is ready at http://localhost:8000/docs"
echo "4. Checking Worker logs..."
docker compose logs worker
echo "--- Demo Complete ---"