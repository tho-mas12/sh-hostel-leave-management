import sqlite3

db_path = 'd:/project/leave takes/instance/leave_management.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\n" + "="*80)
print("DATABASE CONTENTS")
print("="*80 + "\n")

for table in tables:
    table_name = table[0]
    print(f"\n{'='*80}")
    print(f"TABLE: {table_name.upper()}")
    print(f"{'='*80}\n")
    
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    col_names = [col[1] for col in columns]
    
    # Print header
    print(" | ".join(col_names))
    print("-" * 80)
    
    # Print rows
    for row in rows:
        print(" | ".join(str(x) for x in row))
    
    print(f"\nTotal Records: {len(rows)}\n")

conn.close()
print("\n" + "="*80)
