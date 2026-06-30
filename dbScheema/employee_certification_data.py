import pandas as pd
import psycopg2

# ======================================================
# PostgreSQL Configuration
# ======================================================

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "esi"
DB_USER = "postgres"
DB_PASSWORD = "admin"

# ======================================================
# Excel File
# ======================================================

EXCEL_FILE = r"C:\Users\gaugoswa1\Desktop\esia\employee_certifications.xlsx"

# ======================================================
# Read Excel
# ======================================================

try:
    df = pd.read_excel(EXCEL_FILE)
    print(f"Found {len(df)} certification records.")
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

# ======================================================
# Connect PostgreSQL
# ======================================================

try:

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = conn.cursor()

except Exception as e:

    print("Database Connection Failed")
    print(e)
    exit()

# ======================================================
# Insert Query
# ======================================================

insert_query = """
INSERT INTO esia.employee_certifications
(
    employee_id,
    certification_id,
    certification_status,
    issue_date,
    expiry_date,
    certification_score
)
VALUES
(
    %s,%s,%s,%s,%s,%s
)
"""

# ======================================================
# Insert Records
# ======================================================

success = 0
failed = 0

for index, row in df.iterrows():

    try:

        cursor.execute(
            insert_query,
            (
                int(row["employee_id"]),
                int(row["certification_id"]),
                row["certification_status"],
                row["issue_date"],
                row["expiry_date"],
                float(row["certification_score"])
            )
        )

        conn.commit()

        success += 1

        print(f"Inserted : {success}", end="\r")

    except Exception as e:

        conn.rollback()

        failed += 1

        print("\n" + "=" * 70)
        print(f"Row : {index + 2}")
        print(f"Employee ID      : {row['employee_id']}")
        print(f"Certification ID : {row['certification_id']}")
        print(f"Error            : {e}")
        print("=" * 70)

# ======================================================
# Close Connection
# ======================================================

cursor.close()
conn.close()

print("\n")
print("=" * 50)
print("Import Completed")
print("=" * 50)
print(f"Inserted : {success}")
print(f"Failed   : {failed}")
print("=" * 50)