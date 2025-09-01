from pathlib import Path
import pandas as pd
import sqlite3

def load_to_sqlite(csv_path: str | Path, db_path: str | Path, table_name: str, logger=None, if_exists: str = "replace"):
    """
    Load a CSV file into a SQLite database table.
    """
    if logger is None:
        from src.common.logging_setup import setup_logger
        logger = setup_logger()

    csv_path = Path(csv_path)
    db_path = Path(db_path)

    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_path}")
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    logger.info(f"Loading CSV into SQLite: {csv_path} -> {db_path}, table: {table_name}")
    
    df = pd.read_csv(csv_path)
    logger.info(f"Loaded {len(df)} rows from {csv_path}")

    if db_path.parent:
        db_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(name=table_name, con=conn, if_exists=if_exists, index=False)
        logger.info(f"Data loaded successfully into table '{table_name}' in {db_path}")
    except Exception as e:
        logger.exception(f"Failed to load data into SQLite: {e}")
        raise
