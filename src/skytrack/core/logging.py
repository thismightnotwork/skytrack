"""Logging configuration: loguru with rotating file output."""
from __future__ import annotations

from pathlib import Path

from loguru import logger


def configure_logging() -> None:
    """Initialise loguru sinks. Call once at application startup."""
    log_dir = Path.home() / ".skytrack" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.remove()  # Remove default stderr sink

    # Rotating file log
    logger.add(
        log_dir / "skytrack.log",
        rotation="2 MB",
        retention=5,
        enqueue=True,
        backtrace=True,
        diagnose=False,
        level="DEBUG",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | "
            "{name}:{function}:{line} - {message}"
        ),
    )

    # Console sink (INFO+ only, uncoloured for clean subprocess output)
    logger.add(
        lambda msg: print(msg, end=""),
        level="INFO",
        colorize=False,
    )
