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
# Excel File Path
# ======================================================

EXCEL_FILE = r"C:\Users\gaugoswa1\Desktop\esia\employee_training.xlsx"

# ======================================================
# Read Excel
# ======================================================

try:
    df = pd.read_excel(EXCEL_FILE)
    print(f"Found {len(df)} employee training records.")
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
INSERT INTO esia.employee_training
(
    employee_id,
    training_id,
    training_status,
    completion_date,
    score,
    feedback_rating,
    certificate_earned
)
VALUES
(
    %s,%s,%s,%s,%s,%s,%s
)
"""

# ======================================================
# Import Data
# ======================================================

success = 0
failed = 0

for index, row in df.iterrows():

    try:

        # Handle blank values
        completion_date = None if pd.isna(row["completion_date"]) or row["completion_date"] == "" else row["completion_date"]
        score = None if pd.isna(row["score"]) else float(row["score"])
        feedback_rating = None if pd.isna(row["feedback_rating"]) else float(row["feedback_rating"])

        certificate_earned = row["certificate_earned"]

        # Convert Excel TRUE/FALSE safely
        if isinstance(certificate_earned, str):
            certificate_earned = certificate_earned.strip().lower() == "true"

        cursor.execute(
            insert_query,
            (
                int(row["employee_id"]),
                int(row["training_id"]),
                row["training_status"],
                completion_date,
                score,
                feedback_rating,
                certificate_earned
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
        print(f"Employee ID : {row['employee_id']}")
        print(f"Training ID : {row['training_id']}")
        print(f"Error       : {e}")
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