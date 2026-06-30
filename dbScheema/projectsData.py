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
# Excel File
# =====================================

EXCEL_FILE = r"C:\Users\gaugoswa1\Desktop\esia\projects.xlsx"

# =====================================
# Read Excel
# =====================================

df = pd.read_excel(EXCEL_FILE)

print(f"Found {len(df)} project records.")

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
INSERT INTO esia.projects
(
    project_code,
    project_name,
    client_name,
    domain,
    technology_stack,
    start_date,
    end_date,
    project_status
)
VALUES
(
    %s,%s,%s,%s,%s,%s,%s,%s
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

            row["project_code"],
            row["project_name"],
            row["client_name"],
            row["domain"],
            row["technology_stack"],
            row["start_date"],
            row["end_date"],
            row["project_status"]

        ))

        conn.commit()

        success += 1

        print(f"Inserted : {success}", end="\r")

    except Exception as e:

        conn.rollback()

        failed += 1

        print("\n" + "="*60)
        print(f"Error at Excel Row : {index+2}")
        print(f"Project Code : {row['project_code']}")
        print(f"Actual Error : {e}")
        print("="*60)

print("\n")

cursor.close()
conn.close()

print("="*50)
print("Import Completed")
print("="*50)
print(f"Inserted : {success}")
print(f"Failed   : {failed}")
print("="*50)