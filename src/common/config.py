from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

@dataclass(frozen=True)
class Config:
    raw_path: Path = Path(os.getenv("RAW_PATH", "data/sweden_crime.csv"))
    sqlite_path: Path = Path(os.getenv("SQLITE_PATH", "data/warehouse.sqlite"))
    table_name: str = os.getenv("TABLE_NAME", "crime_sweden_yearly")
    log_path: Path = Path(os.getenv("LOG_PATH", "logs/etl.log"))

# Global CONFIG object to import anywhere
CONFIG = Config()
if __name__ == "__main__":
    print(CONFIG.raw_path)
    print(CONFIG.sqlite_path)
