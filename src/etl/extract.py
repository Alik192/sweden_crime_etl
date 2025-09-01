from pathlib import Path
import pandas as pd

def read_crime_csv(path: str | Path, nrows: int | None = None, logger=None) -> pd.DataFrame:
    """Load the CSV (or sample using nrows)."""
    if logger is None:
        from src.common.logging_setup import setup_logger
        logger = setup_logger()

    p = Path(path)
    if not p.exists():
        logger.error(f"CSV file not found: {p}")
        raise FileNotFoundError(f"CSV file not found: {p}")
    
    logger.info(f"Reading CSV file: {p}")
    df = pd.read_csv(p, nrows=nrows)
    
    # Normalize columns
    df.columns = [c.strip().lower().replace(" ", "_").replace(".", "_") for c in df.columns]
    logger.info(f"Columns after normalization: {list(df.columns)}")
    
    return df
