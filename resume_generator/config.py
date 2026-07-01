"""
===========================================================
Employee Skill Intelligence Assistant (ESIA)
Resume Generator Configuration
===========================================================
"""

from pathlib import Path

# ===========================================================
# PROJECT ROOT
# ===========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

# ===========================================================
# FOLDERS
# ===========================================================

DATA_DIR = ROOT_DIR / "data"

DOCUMENT_DIR = ROOT_DIR / "documents"
RESUME_DIR = DOCUMENT_DIR / "resumes"

OUTPUT_DIR = ROOT_DIR / "output"

LOG_DIR = ROOT_DIR / "logs"

# Create folders automatically
for folder in [DATA_DIR, DOCUMENT_DIR, RESUME_DIR, OUTPUT_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# ===========================================================
# OUTPUT FILES
# ===========================================================

METADATA_FILE = OUTPUT_DIR / "resume_metadata.xlsx"
ZIP_FILE = OUTPUT_DIR / "resumes.zip"
LOG_FILE = LOG_DIR / "resume_generator.log"

# ===========================================================
# POSTGRESQL DATABASE CONFIGURATION
# ===========================================================

# Database Server
DB_HOST = "localhost"
DB_PORT = 5432

# Database Credentials
DB_NAME = "esi"
DB_USER = "postgres"
DB_PASSWORD = "admin"

# Database Schema
DB_SCHEMA = "esia"

# Complete Database Configuration
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "options": f"-c search_path={DB_SCHEMA}"
}

# PostgreSQL Connection String (Optional)
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ===========================================================
# RESUME SETTINGS
# ===========================================================

COMPANY_NAME = "Employee Skill Intelligence Assistant"

DEFAULT_COUNTRY = "India"
DEFAULT_EMAIL_DOMAIN = "@employeeai.com"

DEFAULT_RESUME_VERSION = 1
DEFAULT_STATUS = "Active"

# ===========================================================
# PDF SETTINGS
# ===========================================================

PAGE_WIDTH = 595
PAGE_HEIGHT = 842

LEFT_MARGIN = 40
RIGHT_MARGIN = 40
TOP_MARGIN = 40
BOTTOM_MARGIN = 40

TITLE_FONT = "Helvetica-Bold"
HEADER_FONT = "Helvetica-Bold"
BODY_FONT = "Helvetica"

TITLE_FONT_SIZE = 20
HEADER_FONT_SIZE = 14
SUBHEADER_FONT_SIZE = 12
BODY_FONT_SIZE = 10
SMALL_FONT_SIZE = 8

LINE_SPACING = 16

# ===========================================================
# LOGGING
# ===========================================================

LOG_LEVEL = "INFO"