import pytest
import pandas as pd
from pathlib import Path
import sqlite3

from src.etl.extract import read_crime_csv
from src.etl.transform import transform_crime_data
from src.etl.load import load_to_sqlite

@pytest.fixture
def sample_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_data = """Year,crimes.total,crimes.penal.code,crimes.person,murder,assault,sexual.offenses,rape,stealing.general,burglary,house.theft,vehicle.theft,out.of.vehicle.theft,shop.theft,robbery,fraud,criminal.damage,other.penal.crimes,narcotics,drunk.driving,population
1950,2784,2306,120,1,105,40,5,1578,295,NA,NA,NA,NA,3,209,72,477,0,49,7014000
1951,3284,2754,125,1,109,45,6,1899,342,NA,NA,NA,NA,3,310,73,530,0,66,7073000
1952,3160,2608,119,1,104,39,4,1846,372,NA,NA,NA,NA,3,217,82,553,0,78,7125000
1953,2909,2689,119,1,105,45,5,1929,361,NA,NA,NA,NA,4,209,88,220,0,91,7171000
1954,3028,2791,126,1,107,41,5,1981,393,NA,NA,NA,NA,4,236,101,237,0,103,7213000"""
    csv_path.write_text(csv_data)
    return csv_path

def test_extract(sample_csv):
    df = read_crime_csv(sample_csv)
    assert df.shape[0] == 5
    assert "year" in df.columns

def test_transform(sample_csv, tmp_path):
    df_raw = pd.read_csv(sample_csv, na_values=["NA"])
    clean_csv = tmp_path / "clean.csv"
    df_clean = transform_crime_data(df_raw, clean_csv)

    # Check that missing values are reduced
    assert df_clean.isna().sum().sum() <= df_raw.isna().sum().sum()
    
    # Check numeric columns converted
    numeric_cols = df_clean.columns.difference(['year'])
    assert all(pd.api.types.is_numeric_dtype(df_clean[col]) for col in numeric_cols)
    
    # Check CSV saved
    assert clean_csv.exists()

def test_load(sample_csv, tmp_path):
    df_raw = pd.read_csv(sample_csv, na_values=["NA"])
    clean_csv = tmp_path / "clean.csv"
    df_clean = transform_crime_data(df_raw, clean_csv)

    db_path = tmp_path / "test.sqlite"
    load_to_sqlite(clean_csv, db_path, "crime_test")

    with sqlite3.connect(db_path) as conn:
        df_db = pd.read_sql("SELECT * FROM crime_test", conn)
    assert df_db.shape[0] == 5
    assert "year" in df_db.columns
