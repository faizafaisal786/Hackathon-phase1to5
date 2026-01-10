# Frontend Helm Chart

This directory contains the Helm chart for the frontend application.

## Prerequisites

- Kubernetes cluster
- Helm installed

## Installation

To install the frontend application using Helm, run the following command:

```bash
helm install <release-name> ./frontend
```

Replace `<release-name>` with your desired release name.

## Configuration

You can customize the installation by modifying the `values.yaml` file. This file contains default configuration values that can be overridden during installation.

## Usage

After installation, you can access the frontend application through the service created by the Helm chart. Check the service details using:

```bash
kubectl get services
```

## Uninstallation

To uninstall the frontend application, use the following command:

```bash
helm uninstall <release-name>
```

Replace `<release-name>` with the name you used during installation.