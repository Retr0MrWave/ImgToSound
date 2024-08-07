import sys
from pathlib import Path
from loguru import logger


def setup_logger() -> None:
    log_file = Path(f"img2sound.log")
    err_file = Path(f"img2sound.err")

    fmt = ("<green>{time:YYYY-MM-DD HH:mm:ss Z}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>")

    logger.configure(
        handlers=[
            {"sink": log_file, "level": 'DEBUG', "format": fmt, "rotation": "25 MB", "retention": 5},
            {"sink": err_file, "level": 'WARNING', "format": fmt, "rotation": "50 MB", "retention": 5},
            {"sink": sys.stdout, "level": 'DEBUG', "format": fmt},
        ],
    )
