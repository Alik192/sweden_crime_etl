from pathlib import Path
import pandas as pd

def transform_crime_data(df: pd.DataFrame, output_path: Path | str = None, logger=None) -> pd.DataFrame:
    """Transform raw crime data: handle missing values, normalize types, optionally save clean CSV."""
    if logger is None:
        from src.common.logging_setup import setup_logger
        logger = setup_logger()

    logger.info("Starting transformation")
    
    df_clean = df.copy()
    
    # Normalize column names
    df_clean.columns = [c.strip().lower().replace(" ", "_").replace(".", "_") for c in df_clean.columns]
    
    # Handle missing values
    na_before = df_clean.isna().sum().sum()
    df_clean.ffill(inplace=True)
    df_clean.bfill(inplace=True)
    na_after = df_clean.isna().sum().sum()
    
    logger.info(f"Missing values before: {na_before}, after: {na_after}")
    
    # Ensure numeric columns are correct type
    numeric_cols = df_clean.columns.difference(['year'])
    df_clean[numeric_cols] = df_clean[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Save transformed CSV if requested
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(output_path, index=False)
        logger.info(f"Clean CSV saved to {output_path}")
    
    return df_clean
