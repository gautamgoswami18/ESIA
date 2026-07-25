from decimal import Decimal
from decimal import InvalidOperation


def format_experience_years(value) -> str:
    """Format PostgreSQL NUMERIC values for employee list displays."""

    if value is None or value == "":
        return "—"

    try:
        years = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return "—"

    return f"{years.normalize():f} yrs"
