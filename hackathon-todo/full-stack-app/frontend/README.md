# Next.js Frontend Application

This directory contains the Next.js frontend application for the full-stack application.

## Getting Started

To get started with the frontend application, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd full-stack-app/frontend
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Run the development server**:
   ```
   npm run dev
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000` to view the application.

## Building for Production

To build the application for production, run:
```
npm run build
```

Then, you can start the production server with:
```
npm start
```

## Docker

To build and run the Docker container for the frontend application, use the following commands:

1. **Build the Docker image**:
   ```
   docker build -t frontend-app .
   ```

2. **Run the Docker container**:
   ```
   docker run -p 3000:3000 frontend-app
   ```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. 

## License

This project is licensed under the MIT License. See the LICENSE file for details.