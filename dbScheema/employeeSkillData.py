import pandas as pd
import psycopg2

# =====================================
# PostgreSQL Configuration
# =====================================

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "esi"
DB_USER = "postgres"
DB_PASSWORD = "admin"

# =====================================
# Excel File Path
# =====================================

EXCEL_FILE = r"C:\Users\gaugoswa1\Desktop\esia\employee_skills.xlsx"

# =====================================
# Read Excel
# =====================================

df = pd.read_excel(EXCEL_FILE)

print(f"Found {len(df)} employee skill records.")

# =====================================
# Connect PostgreSQL
# =====================================

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

# =====================================
# Insert Query
# =====================================

insert_query = """
INSERT INTO esia.employee_skills
(
    employee_id,
    skill_id,
    proficiency_level,
    years_of_experience,
    is_primary,
    last_used
)
VALUES
(
    %s,%s,%s,%s,%s,%s
)
"""

# =====================================
# Insert Records
# =====================================

success = 0
failed = 0

for index, row in df.iterrows():

    try:

        cursor.execute(insert_query, (

            int(row["employee_id"]),
            int(row["skill_id"]),
            row["proficiency_level"],
            float(row["years_of_experience"]),
            bool(row["is_primary"]),
            row["last_used_date"]

        ))

        conn.commit()

        success += 1

    except Exception as e:

        conn.rollback()

        failed += 1

        print("="*60)
        print(f"Error at Row : {index+2}")
        print(f"Employee ID : {row['employee_id']}")
        print(f"Skill ID    : {row['skill_id']}")
        print("Actual Error:", e)
        print("="*60)

        break

conn.commit()

cursor.close()
conn.close()

print("\n")
print("="*50)
print("Import Completed")
print("="*50)
print(f"Inserted : {success}")
print(f"Failed   : {failed}")
print("="*50)