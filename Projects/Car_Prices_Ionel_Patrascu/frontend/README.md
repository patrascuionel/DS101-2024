# Frontend

This directory contains a React-based frontend application for the BMW Car Price Predictor. It allows users to input car features and receive a price prediction from the backend service.

## Prerequisites

- Node.js and npm

## Installation

1.  Navigate to the `frontend` directory.
2.  Install the dependencies:
    ````bash
    npm install
    ````

## Running the Application

### Development Mode

To run the application in development mode:

````bash
npm start
````
This will start the development server and open the application in your default web browser.

### Production Build
To create a production build of the application:

````bash
npm run build
````
This will generate a `build` directory containing the optimized production files.
### Running the Production Build
To run the production build, you can use a static server. One option is to use `serve`:
````bash
npm install -g serve
serve -s build
````
This will serve the production build on a local server, typically accessible at `http://localhost:5000`.

## Docker
To run the frontend in a Docker container, you can use the provided Dockerfile. First, ensure you have Docker installed, then build and run the container:
```bash
docker build -t bmw-car-price-predictor-frontend .
docker run -p 3000:3000 bmw-car-price-predictor-frontend
```
This will build the Docker image and run it, making the frontend accessible at `http://localhost:3000`.