# Weather REST API

A FastAPI-based REST API that provides weather information and request logging functionality.

## Features

REST microservice with two endpoints:
   - /location
      - Stores request metadata in a local database
      - Fetches today’s weather at that location from NOAA.org
      - Record the status of the request in the database
      - Return results

   -  /requests
      - Retrieves the most recent requests

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)

## Running the Application

### Using Docker Compose 

1. Clone the repository
2. Navigate to the project directory
3. Run the following command:
   ```bash
   docker-compose up --build
   ```

This will start:
- MongoDB database
- MongoDB Express (web interface for MongoDB)
- FastAPI application

The services will be available at:
- FastAPI: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- MongoDB Express: http://localhost:8081


## Running Tests

### Using Docker

1. Build and run the tests:
   ```bash
   docker-compose run fastapi pytest
   ```



## API Endpoints

### Get Weather Information
```
GET /{latitude},{longitude}
```
Example: `GET /39.7456,-97.0892`

### Get Recent Requests
```
GET /requests/{limit}
```
Example: `GET /requests/10`
