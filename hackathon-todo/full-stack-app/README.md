# Full Stack Application

This project is a full-stack application consisting of a FastAPI backend and a Next.js frontend.

## Project Structure

```
full-stack-app
├── backend
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── pages
│   │   └── index.js
│   └── README.md
└── README.md
```

## Backend

The backend is built using FastAPI. 

### Setup

1. Navigate to the `backend` directory.
2. Build the Docker image:
   ```
   docker build -t fastapi-backend .
   ```
3. Run the Docker container:
   ```
   docker run -d -p 8000:8000 fastapi-backend
   ```

### Usage

Access the API at `http://localhost:8000`.

## Frontend

The frontend is built using Next.js.

### Setup

1. Navigate to the `frontend` directory.
2. Build the Docker image:
   ```
   docker build -t nextjs-frontend .
   ```
3. Run the Docker container:
   ```
   docker run -d -p 3000:3000 nextjs-frontend
   ```

### Usage

Access the application at `http://localhost:3000`.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.