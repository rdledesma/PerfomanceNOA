# Performance NOA

This repository contains tools and scripts for evaluating the performance of satellite-based and reanalysis models in estimating global horizontal irradiance (GHI) in Northwest Argentina (NOA), specifically for the sites of Salta (SA) and La Quiaca (LQ).

## Project Structure

### 🔍 Evaluation and Metrics
- `Metrics.py`, `Metrics2.py`: Calculate statistical metrics (MBE, MAE, RMSE, KSI, SS4).
- `NollasQC.py`: Quality control of ground-based measurement data.

### 📊 Results Visualization
- `barsPlot*.py`, `barsSeason*.py`: Generate bar plots by season, solar zenith angle (SZA), and location.
- `inspecError.py`, `inspectAll*.py`, `inspectCams*.py`, `inspectNSRDBLQ.py`: Scripts for visual inspection and error analysis.

### 🛰️ Time Series Generation
- `generateTS*.py`: Scripts to generate and store modeled GHI time series from:
  - `CAMS`
  - `DSR`
  - `ERA-5`
  - `LSA-SAF`
  - `MERRA-2`
  - `NSRDB`
  - `G-CIM`

### 🗺️ Geographic Data
- `Geo.py`: Contains coordinates and geographic info for the measurement stations.

### 📚 External Data Reading
- `readBSRN_*.py`: Scripts to read data from BSRN stations (DOM, IZA, SON).

### 🔧 Utilities
- `generateVectors.py`: Creates vectors for filtering or comparison.
- `record.py`: Auxiliary script for processing or logging.

## Requirements

- Python 3.8+
- Required packages: `numpy`, `pandas`, `matplotlib`, `seaborn`, `xarray`, `netCDF4`, `scipy`

## Typical Workflow

  -  Preprocess modeled and measured data using generateTS_*.py

  - Run model evaluation via Metrics.py or Metrics2.py

  -  Visualize results using the barsPlot*, inspect*, or similar scripts

## Author

    Rubén Ledesma – INENCO / UNSa – rdledesma@exa.unsa.edu.ar

