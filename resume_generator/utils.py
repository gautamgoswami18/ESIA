import logging
from pathlib import Path
from .config import LOG_FILE


def setup_logger():

    logger = logging.getLogger("ResumeGenerator")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(LOG_FILE)

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

    return logger


logger = setup_logger()


def format_employee_name(first_name, last_name):

    return f"{first_name.strip()} {last_name.strip()}"


def resume_filename(employee_id, full_name):

    safe_name = full_name.replace(" ", "_")

    return f"EMP{employee_id}_{safe_name}.pdf"


def ensure_directory(path):

    Path(path).mkdir(parents=True, exist_ok=True)


def print_banner():

    print("=" * 70)
    print("Employee Skill Intelligence Assistant")
    print("Resume Generator")
    print("=" * 70)