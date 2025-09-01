# Sweden Crime ETL Project

## Overview
This project automates the ETL (Extract, Transform, Load) process for historical Sweden crime data. The pipeline extracts data from a CSV file, cleans and transforms it, and loads it into a SQLite database for analysis and reporting. Logging is included for full traceability.

---

## Project Structure
- `main.py` – Orchestrates the ETL process.
- `src/etl/extract.py` – Reads the raw CSV file into a DataFrame.
- `src/etl/transform.py` – Cleans, normalizes, and handles missing values in the data.
- `src/etl/load.py` – Loads the cleaned data into SQLite.
- `src/common/logging_setup.py` – Configures logging to console and file.
- `src/common/config.py` – Stores file paths and table configuration.
- `data/` – Contains raw and transformed CSV files and the SQLite database.
- `logs/` – Stores ETL logs.
- `test/` – Contains unit tests and test results.

---

## ETL Process

### 1. Extraction
- Reads `sweden_crime.csv`.
- Normalizes column names.
- Supports reading in chunks for very large files.
- Logs the number of rows and column names.

### 2. Transformation
- Cleans missing values using forward-fill and backward-fill.
- Normalizes column names and ensures numeric types.
- Optionally saves a clean CSV file (`sweden_crime_clean.csv`).
- Logs missing value handling and save location.

### 3. Loading
- Loads the cleaned CSV into a SQLite database (`warehouse.sqlite`).
- Table name: `crime_sweden_yearly`.
- Supports `replace`, `append`, or `fail` strategies.
- Logs the number of rows loaded and confirmation of database write.

### 4. Logging
- Writes logs both to console and file (`logs/etl.log`) with rotation.
- Tracks ETL progress, warnings, and errors.
- Old logs can be deleted to keep the log folder clean.

---

## How to Run
1. Activate the Python virtual environment.
2. Ensure `sweden_crime.csv` exists in the `data/` folder.
3. Run the ETL pipeline:

bash
python main.py

## Testing

Unit tests for the ETL pipeline are included in `test/test_etl.py`.

## Automation (Windows Task Scheduler)

The ETL can be scheduled to run automatically.

Use the provided `run_etl.bat` file:

```bat
@echo off
cd /d C:\Users\alikh\Desktop\sweden_crime_etl
call .venv\Scripts\activate
python main.py

