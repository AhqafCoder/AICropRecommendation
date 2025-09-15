# Raw Data Documentation

This directory contains the original CSV files used for training the crop AI models.

## Files Overview

### 1. Crop_recommendation.csv (150KB)
**Purpose:** Main training dataset for crop recommendation model
**Rows:** ~2,200 samples
**Columns:**
- `N` - Nitrogen content in soil (kg/ha or relative index)
- `P` - Phosphorus content in soil (kg/ha or relative index) 
- `K` - Potassium content in soil (kg/ha or relative index)
- `temperature` - Temperature (°C)
- `humidity` - Humidity (%)
- `ph` - Soil pH (pH units, 0-14 scale)
- `rainfall` - Rainfall (mm, appears to be seasonal/annual)
- `label` - Target crop name (rice, maize, wheat, etc.)

**Data Quality:** Clean, no missing values observed in sample
**Usage:** Primary dataset for crop classification model

### 2. Crops and livestock products.csv (4.2MB)
**Purpose:** FAO production data for yield and market information
**Rows:** ~25,000+ records
**Columns:**
- `Domain Code`, `Domain` - Dataset identifier ("QCL")
- `Area Code (M49)`, `Area` - Country/region codes and names
- `Element Code`, `Element` - Metric type (Area harvested, Yield, Production)
- `Item Code (CPC)`, `Item` - Crop/product identifier and name
- `Year Code`, `Year` - Year of data (2022-2023 observed)
- `Unit` - Measurement unit (ha, kg/ha, t)
- `Value` - Numeric value for the metric
- `Flag`, `Flag Description` - Data quality indicators (A=Official, E=Estimated)

**Data Quality:** Mix of official and estimated values
**Usage:** Market prices, yields, and production data for profit estimation

### 3. Sub Divisional Monthly Rainfall from 1901 to 2017.csv (445KB)
**Purpose:** Historical rainfall data for India by subdivision
**Rows:** ~4,200 records (117 years × ~36 subdivisions)
**Columns:**
- `SUBDIVISION` - Geographic subdivision name
- `YEAR` - Year (1901-2017)
- `JAN` through `DEC` - Monthly rainfall (mm)
- `ANNUAL` - Annual total rainfall (mm)
- `JF`, `MAM`, `JJAS`, `OND` - Seasonal totals (Winter, Pre-monsoon, Monsoon, Post-monsoon)

**Data Quality:** Some missing values (0 may indicate missing or actual zero rainfall)
**Usage:** Historical rainfall patterns for feature engineering

## Canonical Features for Models

Based on analysis, the following canonical features will be used:

### Crop Recommendation Model
- `N, P, K` - Soil nutrient content (units: kg/ha or relative index)
- `temperature` - Temperature (°C)
- `humidity` - Humidity (%)
- `ph` - Soil pH (pH units)
- `rainfall` - Rainfall (mm, seasonal/annual - needs clarification)
- `label` - Target crop name

### Additional Features (from other datasets)
- `region` - Geographic region (from subdivision data)
- `yield_kg_per_ha` - Expected yield (from FAO data)
- `market_price` - Crop market price (from FAO data)

## Data Processing Notes
1. **Units Standardization:** Ensure consistent units across all datasets
2. **Missing Values:** Handle zeros in rainfall data (distinguish missing vs actual zero)
3. **Geographic Mapping:** Map subdivision names to regions for consistency
4. **Temporal Alignment:** Align historical data with appropriate time periods
5. **Outlier Detection:** Check for unrealistic values in all numeric columns

## Next Steps
1. Implement preprocessing pipeline in `src/preprocess.py`
2. Create feature engineering functions in `src/features.py`
3. Establish train/test splits with proper stratification
