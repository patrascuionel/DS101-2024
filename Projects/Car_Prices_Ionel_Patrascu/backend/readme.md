# Backend

This backend service processes data and relies on model files and other necessary assets.

**Important Assumption:** All required input files (e.g., trained models, scalers, column lists) are expected to be located in the `notebook_output/` directory relative to the backend's execution path.

## Docker

This backend service can be containerized using Docker. A `Dockerfile` is provided in this directory to build the Docker image.

To build the image, navigate to the `backend` directory and run:

```bash
docker build -t backend-service .
```

To run the container:

```bash
docker run -p 8000:8000 backend-service
```

This will start the service and map port 8000 of the container to port 8000 on the host machine.
