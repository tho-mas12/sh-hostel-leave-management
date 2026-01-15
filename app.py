from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leave_management.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'student' or 'admin'

class LeaveApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    leave_reason = db.Column(db.String(200), nullable=False)
    leave_start = db.Column(db.Date, nullable=False)
    leave_end = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), default='Pending')  # 'Pending', 'Approved', 'Rejected'

@app.route('/')
def home():
    return render_template('student_login.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['register_number']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user and user.role == 'student':
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('student_dashboard'))
        else:
            return render_template('student_login.html', error='Invalid username or password')
    return render_template('student_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('student_register.html', error='Passwords do not match')
        
        if User.query.filter_by(username=username).first():
            return render_template('student_register.html', error='Username already exists')
        
        try:
            new_user = User(username=username, password=password, role='student')
            db.session.add(new_user)
            db.session.commit()
            return render_template('student_register.html', success='Registration successful! You can now login.')
        except Exception as e:
            return render_template('student_register.html', error=f'Registration failed: {str(e)}')
    
    return render_template('student_register.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user and user.role == 'admin':
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    leaves = LeaveApplication.query.all()
    return render_template('admin_dashboard.html', leaves=leaves)

@app.route('/admin_statistics')
def admin_statistics():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    # Get filter parameters
    filter_start_date = request.args.get('start_date')
    filter_end_date = request.args.get('end_date')
    
    # Convert filter dates to date objects if provided
    start_date = None
    end_date = None
    if filter_start_date:
        start_date = datetime.strptime(filter_start_date, '%Y-%m-%d').date()
    if filter_end_date:
        end_date = datetime.strptime(filter_end_date, '%Y-%m-%d').date()
    
    # Get leaves with optional date filter
    if start_date and end_date:
        leaves = LeaveApplication.query.filter(
            LeaveApplication.leave_start >= start_date,
            LeaveApplication.leave_start <= end_date
        ).all()
    elif start_date:
        leaves = LeaveApplication.query.filter(LeaveApplication.leave_start >= start_date).all()
    elif end_date:
        leaves = LeaveApplication.query.filter(LeaveApplication.leave_start <= end_date).all()
    else:
        leaves = LeaveApplication.query.all()
    
    # Get total counts based on filtered data
    total_students = User.query.filter_by(role='student').count()
    total_leaves = len(leaves)
    approved_leaves = sum(1 for leave in leaves if leave.status == 'Approved')
    pending_leaves = sum(1 for leave in leaves if leave.status == 'Pending')
    rejected_leaves = sum(1 for leave in leaves if leave.status == 'Rejected')
    
    # Get student-wise statistics from filtered leaves
    student_stats = []
    students = User.query.filter_by(role='student').all()
    
    for student in students:
        student_leaves = [leave for leave in leaves if leave.student_id == student.id]
        total = len(student_leaves)
        approved = sum(1 for leave in student_leaves if leave.status == 'Approved')
        pending = sum(1 for leave in student_leaves if leave.status == 'Pending')
        rejected = sum(1 for leave in student_leaves if leave.status == 'Rejected')
        
        if total > 0:  # Only show students with leaves in filtered range
            student_stats.append({
                'student_id': student.id,
                'username': student.username,
                'total': total,
                'approved': approved,
                'pending': pending,
                'rejected': rejected
            })
    
    # Get date-wise statistics from filtered leaves
    date_stats_dict = defaultdict(lambda: {'total': 0, 'approved': 0, 'pending': 0, 'rejected': 0})
    
    for leave in leaves:
        date_key = str(leave.leave_start)
        date_stats_dict[date_key]['total'] += 1
        if leave.status == 'Approved':
            date_stats_dict[date_key]['approved'] += 1
        elif leave.status == 'Pending':
            date_stats_dict[date_key]['pending'] += 1
        elif leave.status == 'Rejected':
            date_stats_dict[date_key]['rejected'] += 1
    
    # Convert to list and sort by date
    date_wise_stats = []
    for date_key in sorted(date_stats_dict.keys(), reverse=True):
        stats = date_stats_dict[date_key]
        date_wise_stats.append({
            'date': date_key,
            'total': stats['total'],
            'approved': stats['approved'],
            'pending': stats['pending'],
            'rejected': stats['rejected']
        })
    
    # Get students info with leave count from filtered data
    students_info = []
    for student in students:
        leave_count = len([leave for leave in leaves if leave.student_id == student.id])
        if leave_count > 0:  # Only show students with leaves
            students_info.append({
                'id': student.id,
                'username': student.username,
                'leave_count': leave_count
            })
    
    return render_template('admin_statistics.html',
                         total_students=total_students,
                         total_leaves=total_leaves,
                         approved_leaves=approved_leaves,
                         pending_leaves=pending_leaves,
                         rejected_leaves=rejected_leaves,
                         student_stats=student_stats,
                         date_wise_stats=date_wise_stats,
                         students=students_info,
                         filter_start_date=filter_start_date,
                         filter_end_date=filter_end_date)

@app.route('/database_viewer')
def database_viewer():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    
    # Get all users
    all_users = User.query.all()
    
    # Get all leave applications
    all_leaves = LeaveApplication.query.all()
    
    # Format data for display
    users_data = []
    for user in all_users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'role': user.role
        })
    
    leaves_data = []
    for leave in all_leaves:
        leaves_data.append({
            'id': leave.id,
            'student_id': leave.student_id,
            'student_username': User.query.get(leave.student_id).username if User.query.get(leave.student_id) else 'N/A',
            'leave_reason': leave.leave_reason,
            'leave_start': leave.leave_start,
            'leave_end': leave.leave_end,
            'status': leave.status
        })
    
    return render_template('database_viewer.html',
                         users=users_data,
                         leaves=leaves_data,
                         total_users=len(users_data),
                         total_leaves=len(leaves_data))

@app.route('/approve_leave/<int:leave_id>')
def approve_leave(leave_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    leave = LeaveApplication.query.get(leave_id)
    if leave:
        leave.status = 'Approved'
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_leave/<int:leave_id>')
def reject_leave(leave_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    leave = LeaveApplication.query.get(leave_id)
    if leave:
        leave.status = 'Rejected'
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))
    leaves = LeaveApplication.query.filter_by(student_id=session['user_id']).all()
    return render_template('student_dashboard.html', leaves=leaves)

@app.route('/dashboard')
def dashboard():
    return render_template('admin_dashboard.html')

@app.route('/leave_application', methods=['GET', 'POST'])
def leave_application():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('student_login'))
    if request.method == 'POST':
        try:
            leave_reason = request.form['leave_reason']
            leave_start_str = request.form['leave_start']
            leave_end_str = request.form['leave_end']
            
            # Convert strings to date objects
            leave_start = datetime.strptime(leave_start_str, '%Y-%m-%d').date()
            leave_end = datetime.strptime(leave_end_str, '%Y-%m-%d').date()
            
            if leave_end >= leave_start:
                new_leave = LeaveApplication(
                    student_id=session['user_id'], 
                    leave_reason=leave_reason, 
                    leave_start=leave_start, 
                    leave_end=leave_end
                )
                db.session.add(new_leave)
                db.session.commit()
                return redirect(url_for('student_dashboard'))
            else:
                return render_template('leave_application.html', error='End date must be after or equal to start date')
        except Exception as e:
            return render_template('leave_application.html', error=f'Error: {str(e)}')
    return render_template('leave_application.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

       
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password='admin123',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin / admin123")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

