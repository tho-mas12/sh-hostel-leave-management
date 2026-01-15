from app import app, db, User

# Create application context
with app.app_context():
    # Clear existing data
    db.session.query(User).delete()
    db.session.commit()
    
    # Add admin user
    admin = User(username='admin', password='admin123', role='admin')
    
    # Add student user
    student = User(username='123456', password='student123', role='student')
    
    db.session.add(admin)
    db.session.add(student)
    db.session.commit()
    
    print("Database seeded successfully!")
    print("\nSample Credentials:")
    print("Admin - Username: admin, Password: admin123")
    print("Student - Username: 123456, Password: student123")
