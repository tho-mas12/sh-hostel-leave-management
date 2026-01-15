import sqlite3
from tabulate import tabulate

# Connect to the database
conn = sqlite3.connect('instance/leave_management.db')
cursor = conn.cursor()

print("=" * 100)
print("HOSTEL STUDENT LEAVE MANAGEMENT SYSTEM - DATABASE VIEW")
print("=" * 100)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"\n📋 Total Tables: {len(tables)}\n")

for table_name in tables:
    table = table_name[0]
    print(f"\n{'='*100}")
    print(f"📊 TABLE: {table.upper()}")
    print(f"{'='*100}\n")
    
    # Get column info
    cursor.execute(f"PRAGMA table_info({table})")
    columns_info = cursor.fetchall()
    
    # Display column info
    print("Columns:")
    for col_info in columns_info:
        col_id, col_name, col_type, notnull, default, pk = col_info
        pk_mark = " [PRIMARY KEY]" if pk else ""
        print(f"  • {col_name} ({col_type}){pk_mark}")
    
    # Get data
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    
    if rows:
        column_names = [description[0] for description in cursor.description]
        print(f"\nRecords ({len(rows)} total):\n")
        print(tabulate(rows, headers=column_names, tablefmt="grid"))
    else:
        print(f"\nNo records found in {table}")
    
    print()

# Summary Statistics
print(f"\n{'='*100}")
print("📈 DATABASE STATISTICS")
print(f"{'='*100}\n")

cursor.execute("SELECT COUNT(*) FROM user WHERE role='student'")
student_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
admin_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM leaveapplication")
total_leaves = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM leaveapplication WHERE status='Approved'")
approved = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM leaveapplication WHERE status='Pending'")
pending = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM leaveapplication WHERE status='Rejected'")
rejected = cursor.fetchone()[0]

stats = [
    ["Total Students", student_count],
    ["Total Admins", admin_count],
    ["Total Leave Applications", total_leaves],
    ["  - Approved", approved],
    ["  - Pending", pending],
    ["  - Rejected", rejected],
]

print(tabulate(stats, headers=["Metric", "Count"], tablefmt="fancy_grid"))

conn.close()
print("\n" + "=" * 100 + "\n")
