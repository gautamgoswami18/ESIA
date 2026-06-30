import pandas as pd
import psycopg2

# ============================================
# PostgreSQL Configuration
# ============================================

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "esi"
DB_USER = "postgres"
DB_PASSWORD = "admin"

# ============================================
# Excel File
# ============================================

EXCEL_FILE = r"C:\Users\gaugoswa1\Desktop\esia\employee_projects.xlsx"

# ============================================
# Read Excel
# ============================================

df = pd.read_excel(EXCEL_FILE)

print(f"Found {len(df)} employee project records.")

# ============================================
# Connect PostgreSQL
# ============================================

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

# ============================================
# Insert Query
# ============================================

insert_query = """
INSERT INTO esia.employee_projects
(
    employee_id,
    project_id,
    role_name,
    allocation_percentage,
    billing_status,
    start_date,
    end_date
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s
)
"""

# ============================================
# Insert Records
# ============================================

success = 0
failed = 0

for index, row in df.iterrows():

    try:

        cursor.execute(insert_query, (

            int(row["employee_id"]),
            int(row["project_id"]),
            row["role_name"],
            int(row["allocation_percentage"]),
            row["billing_status"],
            row["start_date"],
            row["end_date"]

        ))

        conn.commit()

        success += 1

        print(f"Inserted : {success}", end="\r")

    except Exception as e:

        conn.rollback()

        failed += 1

        print("\n" + "=" * 70)
        print(f"Error at Excel Row : {index + 2}")
        print(f"Employee ID : {row['employee_id']}")
        print(f"Project ID  : {row['project_id']}")
        print(f"Error       : {e}")
        print("=" * 70)

print("\n")

cursor.close()
conn.close()

print("=" * 50)
print("Import Completed")
print("=" * 50)
print(f"Inserted : {success}")
print(f"Failed   : {failed}")
print("=" * 50)