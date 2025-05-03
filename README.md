## Performance NOA

This repository contains tools and scripts for evaluating the performance of satellite-based and reanalysis models in estimating global horizontal irradiance (GHI) in Northwest Argentina (NOA), specifically for the sites of Salta (SA) and La Quiaca (LQ).


## Manuscript Information

    Title: Evaluation of Satellite and Reanalysis Models for Solar Irradiance Estimation in Northwest Argentina

    ID: 9498

    Authors:

        Rubén Ledesma – INENCO / UNSa – rdledesma@exa.unsa.edu.ar

        Rodrigo Alonso-Suárez – Solar Energy Laboratory, CENUR Litoral Norte, University of the Republic, Uruguay – r.alonso.suarez@gmail.com

        Germán Salazar – INENCO / UNSa – german.salazar@conicet.gov.ar

        Fernando Nollas – Servicio Meteorológico Nacional Argentino – fnollas@smn.gob.ar

        Olga Vilela – Center for Renewable Energy of the Federal University of Pernambuco (CER-UFPE) – ocv@ufpe.br

    Journal: IEEE Latin America Transactions

        IEEE Latin America Transactions

## Project Structure
🔍 Evaluation and Metrics

    Metrics.py, Metrics2.py: Calculate statistical metrics (MBE, MAE, RMSE, KSI, SS4).

    NollasQC.py: Quality control of ground-based measurement data.

## 📊 Results Visualization

    barsPlot*.py, barsSeason*.py: Generate bar plots by season, solar zenith angle (SZA), and location.

    inspecError.py, inspectAll*.py, inspectCams*.py, inspectNSRDBLQ.py: Scripts for visual inspection and error analysis.

## 🛰️ Time Series Generation

    generateTS*.py: Scripts to generate and store modeled GHI time series from:

        CAMS

        DSR

        ERA-5

        LSA-SAF

        MERRA-2

        NSRDB

        G-CIM

## 🗺️ Geographic Data

    Geo.py: Contains coordinates and geographic info for the measurement stations.

📚 Data Requests

If you would like to request the data used in this project, please contact the authors via email at rdledesma@exa.unsa.edu.ar.

🔧 Utilities

    generateVectors.py: Creates vectors for filtering or comparison.

    record.py: Auxiliary script for processing or logging.

Requirements

    Python 3.8+

    Required packages: numpy, pandas, matplotlib, seaborn, xarray, netCDF4, scipy

Typical Workflow

    Preprocess modeled and measured data using generateTS_*.py

    Run model evaluation via Metrics.py or Metrics2.py

    Visualize results using the barsPlot*, inspect*, or similar scripts

