#!/bin/bash

# Define the source directory and Helm chart name
SOURCE_DIR="kubernetes_scripts"
HELM_CHART_DIR="my-helm"

# Ensure helmify is installed
if ! command -v helmify &> /dev/null; then
    echo "Error: helmify is not installed. Please install it first."
    exit 1
fi

# Ensure the Helm chart directory exists
if [ ! -d "$HELM_CHART_DIR" ]; then
    echo "Error: Helm chart directory '$HELM_CHART_DIR' does not exist. Create it using 'helm create $HELM_CHART_DIR'."
    exit 1
fi

# Process all YAML files in the source directory
for yaml_file in "$SOURCE_DIR"/*.yaml; do
    if [ -f "$yaml_file" ]; then
        echo "Processing $yaml_file..."
        cat "$yaml_file" | helmify "$HELM_CHART_DIR"
    fi
done

echo "Conversion complete. Helm templates are in the '$HELM_CHART_DIR' directory."