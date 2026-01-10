# Backend Helm Chart

This directory contains the Helm chart for the backend application. Below are the details regarding the structure and usage of this chart.

## Chart Structure

- **templates/**: Contains the Kubernetes resource templates for the backend application.
  - **deployment.yaml**: Defines the Deployment resource for managing the backend application pods.
  - **service.yaml**: Defines the Service resource for exposing the backend application.
  - **configmap.yaml**: Contains non-confidential data in key-value pairs for the backend application.
  - **secrets.yaml**: Stores sensitive information securely, such as passwords or API keys.

- **values.yaml**: Contains the default configuration values for the backend Helm chart. You can override these values during installation or upgrades.

- **Chart.yaml**: Contains metadata about the backend Helm chart, including its name, version, and description.

## Installation Instructions

To install the backend application using this Helm chart, follow these steps:

1. Ensure you have Helm installed on your system.
2. Navigate to the backend directory:
   ```
   cd helm-chart-project/backend
   ```
3. Install the chart:
   ```
   helm install <release-name> .
   ```
   Replace `<release-name>` with your desired release name.

## Usage

After installation, you can manage the backend application using Helm commands. For example, to upgrade the release, use:
```
helm upgrade <release-name> .
```

To uninstall the release, use:
```
helm uninstall <release-name>
```

## Notes

- Make sure to configure the `values.yaml` file according to your environment before installation.
- Review the templates in the `templates/` directory to customize the Kubernetes resources as needed.