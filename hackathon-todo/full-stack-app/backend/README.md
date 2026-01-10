# FastAPI Backend Application

This directory contains the FastAPI backend application for the full-stack app.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd full-stack-app/backend
   ```

2. **Build the Docker image**:
   ```
   docker build -t fastapi-backend .
   ```

3. **Run the Docker container**:
   ```
   docker run -d -p 8000:8000 fastapi-backend
   ```

4. **Access the application**:
   Open your browser and go to `http://localhost:8000`.

## Usage

The FastAPI application provides a set of APIs that can be accessed at the `/docs` endpoint for interactive API documentation.

## Dependencies

The required Python packages are listed in `requirements.txt`. Make sure to install them if you are running the application locally without Docker.

## Contributing

Feel free to submit issues or pull requests for any improvements or bug fixes.