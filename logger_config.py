
import logging
import os

from constants import APP_NAME, FILE_LOG, DIR_NAME_LOG


# [!] 2 fois la même function [!] Peut pas importer dans ce fichier car "circular import"
def get_safebox_directory2():
    """Return SafeBox root directory in AppData."""
    base = os.getenv("APPDATA")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def get_logs_directory():
    """Return logs directory."""

    path = os.path.join(
        get_safebox_directory2(),
        DIR_NAME_LOG
    )

    os.makedirs(path, exist_ok=True)

    return path


def setup_logger(
    logger_name=APP_NAME,
    log_level=logging.INFO
):
    """
    Setup generic logger
    """

    log_dir = get_logs_directory()

    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(logger_name)

    logger.setLevel(log_level)

    # éviter doublons handlers
    logger.handlers.clear()

    if not logger.handlers:

        file_handler = logging.FileHandler(
            os.path.join(
                log_dir, 
                FILE_LOG
            ),
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger

