import logging
import logging.handlers
from pathlib import Path
import os

def setup_logger(name: str = "etl", log_path: str | os.PathLike[str] = "logs/etl.log") -> logging.Logger:
    """Returns a logger that writes to file and console with rotation."""
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Add handlers only if they do not exist
    if not logger.hasHandlers():
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
        )

        file_handler = logging.handlers.RotatingFileHandler(
            log_path, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(fmt)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(fmt)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
