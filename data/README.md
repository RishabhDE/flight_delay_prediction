# Data Directory

This directory contains the flight delay prediction dataset.

## Dataset Source

**Real Dataset**: Mendeley Data - "Dataset for Airline Departure Delay Prediction"
- **Source**: https://data.mendeley.com/datasets/xxwzw3tyfp/1
- **Size**: 5.5 million flight records from 2023
- **Format**: CSV with flight and weather features

## Files (Not Included in Git - Too Large)

Due to GitHub file size limitations, the following files are excluded from version control:

- `flight_data_complete.csv` (50,000 records sampled from 5.5M - ~16MB)
- `weather_data.csv` (weather station data)

## How to Get the Data

### Option 1: Download from Mendeley (Recommended)
1. Visit: https://data.mendeley.com/datasets/xxwzw3tyfp/1
2. Download the dataset ZIP file
3. Extract to this directory
4. Run Notebook 01 to process and load into Feature Store

### Option 2: Generate from Notebooks
If you run `01_data_preparation_and_feature_store.ipynb`, it will:
1. Automatically download the Mendeley dataset
2. Sample 50,000 records
3. Create `flight_data_complete.csv` in this directory
4. Load data into AWS SageMaker Feature Store

## Dataset Schema

### Features (12 total):
- **airline**: Airline carrier code
- **origin**: Origin airport code
- **destination**: Destination airport code
- **distance**: Flight distance in miles
- **day_of_week**: Day of week (0=Monday, 6=Sunday)
- **month**: Month (1-12)
- **departure_hour**: Scheduled departure hour (0-23)
- **temperature**: Temperature in Fahrenheit
- **wind_speed**: Wind speed in mph
- **precipitation**: Precipitation amount
- **visibility**: Visibility in miles
- **snow**: Snow indicator (0=no, 1=yes)

### Target Variable:
- **is_delayed**: Binary (0=on-time, 1=delayed ≥15 minutes)

## Statistics

- **Total Records**: 50,000 flights
- **Delay Rate**: ~17-22% (realistic from 2023 data)
- **Time Period**: 2023 flight data
- **Airlines**: 18 major US carriers
- **Airports**: 350+ origin/destination pairs

## Data Quality

- ✅ No missing values
- ✅ All features normalized/encoded
- ✅ Realistic delay distribution
- ✅ Real-world data (not synthetic)
- ✅ Balanced temporal distribution

## Citations

If you use this dataset, please cite:

```
Dataset for Airline Departure Delay Prediction
Mendeley Data, V1
https://data.mendeley.com/datasets/xxwzw3tyfp/1
```
