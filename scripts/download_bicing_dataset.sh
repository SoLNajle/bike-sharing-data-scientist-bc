#!/bin/sh

# Install Kaggle CLI
pip install kaggle

# Check if data has already been downloaded
if ls /data/bicing/* &> /dev/null; then
    echo "Data already downloaded."
else
    # Download the dataset from Kaggle
    kaggle datasets download -d edomingo/bicing-stations-dataset-bcn-bike-sharing -p /data/bicing --unzip
    echo "Data download complete."
fi