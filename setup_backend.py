"""
=========================================================
ESIA Backend Project Structure Generator
=========================================================
Creates the complete FastAPI backend folder structure.
"""

from pathlib import Path

ROOT = Path(__file__).parent

folders = [

    # Application
    "app",

    # API
    "app/api",

    # Business Layer
    "app/services",

    # Repository Layer
    "app/repository",

    # Database Models
    "app/models",

    # Pydantic Schemas
    "app/schemas",

    # Utilities
    "app/utils",

    # Middleware
    "app/middleware",

    # Authentication
    "app/auth",

    # Configuration
    "app/core",

    # Static Files
    "app/static",

    # Templates
    "app/templates",

    # AI Modules (Future)
    "app/ai",

    # Tests
    "tests",

    # Documentation
    "docs",

    # Scripts
    "scripts",

    # Logs
    "logs",

    # Output
    "output"
]

files = [

    # Root
    "requirements.txt",
    ".env",
    ".gitignore",
    "README.md",

    # App
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/database.py",
    "app/dependencies.py",

    # API
    "app/api/__init__.py",
    "app/api/employee.py",
    "app/api/skill.py",
    "app/api/project.py",
    "app/api/certification.py",
    "app/api/training.py",
    "app/api/resume.py",
    "app/api/search.py",

    # Services
    "app/services/__init__.py",
    "app/services/employee_service.py",
    "app/services/skill_service.py",
    "app/services/project_service.py",
    "app/services/certification_service.py",
    "app/services/training_service.py",
    "app/services/resume_service.py",
    "app/services/search_service.py",

    # Repository
    "app/repository/__init__.py",
    "app/repository/employee_repository.py",
    "app/repository/skill_repository.py",
    "app/repository/project_repository.py",
    "app/repository/certification_repository.py",
    "app/repository/training_repository.py",
    "app/repository/resume_repository.py",

    # Models
    "app/models/__init__.py",
    "app/models/employee.py",
    "app/models/skill.py",
    "app/models/project.py",
    "app/models/certification.py",
    "app/models/training.py",
    "app/models/resume.py",

    # Schemas
    "app/schemas/__init__.py",
    "app/schemas/employee.py",
    "app/schemas/skill.py",
    "app/schemas/project.py",
    "app/schemas/certification.py",
    "app/schemas/training.py",
    "app/schemas/resume.py",

    # Utils
    "app/utils/__init__.py",
    "app/utils/logger.py",
    "app/utils/constants.py",
    "app/utils/helpers.py",

    # Middleware
    "app/middleware/__init__.py",
    "app/middleware/error_handler.py",
    "app/middleware/request_logger.py",

    # Auth
    "app/auth/__init__.py",
    "app/auth/jwt_handler.py",
    "app/auth/security.py",

    # Core
    "app/core/__init__.py",

    # AI
    "app/ai/__init__.py",

    # Tests
    "tests/__init__.py",
    "tests/test_employee.py",
    "tests/test_skill.py",

    # Docs
    "docs/API.md",

    # Scripts
    "scripts/init_db.py",
]

print("=" * 60)
print("Creating ESIA Backend Structure")
print("=" * 60)

for folder in folders:
    path = ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    print(f"[DIR ] {folder}")

for file in files:
    path = ROOT / file

    if not path.exists():
        path.touch()
        print(f"[FILE] {file}")

print("\nBackend structure created successfully!")