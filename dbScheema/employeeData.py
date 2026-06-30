import pandas as pd
import psycopg2

# ==========================
# Database Configuration
# ==========================

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "esi"      # Change if different
DB_USER = "postgres"
DB_PASSWORD = "admin"

# ==========================
# Excel File
# ==========================

EXCEL_FILE = r"C:\Users\gaugoswa1\Desktop\esia\employee.xlsx"

# ==========================
# Read Excel
# ==========================

df = pd.read_excel(EXCEL_FILE)

print(f"Found {len(df)} employees")

# ==========================
# Connect Database
# ==========================

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

# ==========================
# Insert Query
# ==========================

sql = """
INSERT INTO esia.employees
(
first_name,
last_name,
email,
designation,
location,
experience_years,
primary_skill_id,
domain,
utilization,
availability,
joining_date,
employment_status
)
VALUES
(
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""

# ==========================
# Insert Records
# ==========================

count = 0

try:

    for _, row in df.iterrows():

        cursor.execute(sql, (

            row["first_name"],
            row["last_name"],
            row["email"],
            row["designation"],
            row["location"],
            float(row["experience_years"]),
            int(row["primary_skill_id"]),
            row["domain"],
            int(row["utilization"]),
            row["availability"],
            row["joining_date"],
            row["employment_status"]

        ))

        count += 1

    conn.commit()

    print("="*50)
    print(f"{count} Employees Imported Successfully")
    print("="*50)

except Exception as e:

    conn.rollback()

    print("Error Found")
    print(e)

finally:

    cursor.close()
    conn.close()