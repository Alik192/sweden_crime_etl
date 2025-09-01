from pathlib import Path
import sys
from src.common.config import CONFIG
from src.etl.extract import read_crime_csv
from src.etl.transform import transform_crime_data
from src.etl.load import load_to_sqlite
from src.common.logging_setup import setup_logger

# Initialize logger once
logger = setup_logger(name="etl", log_path=str(CONFIG.log_path))

def main():
    try:
        logger.info("Starting ETL process")

        # Extract
        df_raw = read_crime_csv(CONFIG.raw_path, logger=logger)

        # Transform
        clean_csv_path = CONFIG.raw_path.parent / "sweden_crime_clean.csv"
        df_clean = transform_crime_data(df_raw, output_path=clean_csv_path, logger=logger)

        # Load
        load_to_sqlite(clean_csv_path, CONFIG.sqlite_path, CONFIG.table_name, logger=logger)

        logger.info("ETL process completed successfully")

    except Exception as e:
        logger.exception(f"ETL process failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
