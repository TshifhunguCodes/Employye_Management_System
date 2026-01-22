from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os
from functools import wraps
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here-change-this')

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin Only Decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('email') != 'admin@example.com':
            flash('Admin access required')
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_table_data(table_name, id=None):
    """Get data from table - all records or specific ID"""
    if id:
        # Use the correct primary key column based on table
        if table_name == 'dimemployee':
            pk_column = 'employee_id'
        elif table_name == 'dimdepartment':
            pk_column = 'departmentid'
        elif table_name == 'dimjob':
            pk_column = 'jobid'
        elif table_name == 'dimlocation':
            pk_column = 'locationid'
        else:
            pk_column = 'id'
        
        query = f"SELECT * FROM {table_name} WHERE {pk_column} = %s"
        return db.execute_query(query, (id,), fetch_one=True)
    else:
        query = f"SELECT * FROM {table_name} ORDER BY 1"
        return db.execute_query(query, fetch=True)

def get_table_counts():
    """Get counts for all tables"""
    counts = {}
    tables = ['dimemployee', 'dimdepartment', 'dimjob', 'dimlocation']
    
    for table in tables:
        query = f"SELECT COUNT(*) FROM {table}"
        result = db.execute_query(query, fetch_one=True)
        counts[table] = result[0] if result else 0
    
    return counts

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        if session.get('email') == 'admin@example.com':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check for admin login
        if email == 'admin@example.com' and password == 'admin123':
            session['user_id'] = 0
            session['email'] = email
            session['name'] = 'Administrator'
            return redirect(url_for('admin_dashboard'))
        
        # Regular user login
        query = """
        SELECT employee_id, firstname, lastname, email, passwords 
        FROM dimemployee 
        WHERE email = %s AND passwords = %s
        """
        user = db.execute_query(query, (email, password), fetch_one=True)
        
        if user:
            session['user_id'] = user['employee_id']
            session['email'] = user['email']
            session['name'] = f"{user['firstname']} {user['lastname']}"
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        
        # Check if user exists
        check_query = "SELECT email FROM dimemployee WHERE email = %s"
        existing_user = db.execute_query(check_query, (email,), fetch_one=True)
        
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('register'))
        
        # Get next employee ID
        id_query = "SELECT COALESCE(MAX(employee_id), 0) + 1 FROM dimemployee"
        next_id = db.execute_query(id_query, fetch_one=True)
        employee_id = next_id[0] if next_id else 1
        
        # Insert new employee
        insert_query = """
        INSERT INTO dimemployee (employee_id, firstname, lastname, gender, email, 
                                birthdate, hire, salary, passwords)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            db.execute_query(insert_query, (
                employee_id, firstname, lastname, gender, email,
                birthdate, datetime.now().date(), 0, password
            ))
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error during registration: {str(e)}')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def user_dashboard():
    if session.get('email') == 'admin@example.com':
        return redirect(url_for('admin_dashboard'))
    
    # Get user data
    user_query = "SELECT * FROM dimemployee WHERE employee_id = %s"
    user = db.execute_query(user_query, (session['user_id'],), fetch_one=True)
    
    if not user:
        flash('User not found')
        return redirect(url_for('logout'))
    
    # Get predefined data tasks
    # Task 1: Count total employees
    count_query = "SELECT COUNT(*) FROM dimemployee"
    total_result = db.execute_query(count_query, fetch_one=True)
    total_employees = total_result[0] if total_result else 0
    
    # Task 2: Get average salary (excluding 0)
    avg_query = "SELECT AVG(salary) FROM dimemployee WHERE salary > 0"
    avg_result = db.execute_query(avg_query, fetch_one=True)
    avg_salary = float(avg_result[0]) if avg_result and avg_result[0] else 0
    
    # Get current year for calculations
    from datetime import datetime
    now = datetime.now()
    
    return render_template('user_dashboard.html', 
                         user=user, 
                         total_employees=total_employees,
                         avg_salary=avg_salary,
                         now=now)

@app.route('/admin')
@admin_required
def admin_dashboard():
    counts = get_table_counts()
    
    return render_template('admin_dashboard.html',
                         total_employees=counts.get('dimemployee', 0),
                         total_departments=counts.get('dimdepartment', 0),
                         total_jobs=counts.get('dimjob', 0),
                         total_locations=counts.get('dimlocation', 0))

@app.route('/admin/tables/<table_name>')
@admin_required
def admin_tables(table_name):
    valid_tables = ['dimemployee', 'dimdepartment', 'dimjob', 'dimlocation']
    
    if table_name not in valid_tables:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    # Get table data
    data = get_table_data(table_name)
    
    # Get column names
    columns = db.get_table_columns(table_name)
    
    return render_template('admin_tables.html',
                         table_name=table_name,
                         data=data,
                         columns=columns)

@app.route('/admin/edit/<table_name>/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(table_name, id):
    valid_tables = ['dimemployee', 'dimdepartment', 'dimjob', 'dimlocation']
    
    if table_name not in valid_tables:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    # Get existing record
    item = get_table_data(table_name, id)
    
    if not item:
        flash('Record not found')
        return redirect(url_for('admin_tables', table_name=table_name))
    
    if request.method == 'POST':
        # Get columns for this table
        columns = db.get_table_columns(table_name)
        
        # Build UPDATE query
        set_clauses = []
        values = []
        
        for column in columns:
            if column in request.form and column not in ['employee_id', 'passwords', 'departmentid', 'jobid', 'locationid']:
                set_clauses.append(f"{column} = %s")
                values.append(request.form[column])
        
        if set_clauses:
            # Add the ID value at the end
            values.append(id)
            
            # Determine primary key column
            if table_name == 'dimemployee':
                pk_column = 'employee_id'
            elif table_name == 'dimdepartment':
                pk_column = 'departmentid'
            elif table_name == 'dimjob':
                pk_column = 'jobid'
            elif table_name == 'dimlocation':
                pk_column = 'locationid'
            
            update_query = f"""
            UPDATE {table_name} 
            SET {', '.join(set_clauses)}
            WHERE {pk_column} = %s
            """
            
            try:
                db.execute_query(update_query, tuple(values))
                flash('Update successful!')
                return redirect(url_for('admin_tables', table_name=table_name))
            except Exception as e:
                flash(f'Error updating record: {str(e)}')
    
    # Get columns for display
    columns = db.get_table_columns(table_name)
    
    return render_template('admin_edit.html',
                         table_name=table_name,
                         item=item,
                         columns=columns)

@app.route('/admin/delete/<table_name>/<int:id>')
@admin_required
def admin_delete(table_name, id):
    valid_tables = ['dimemployee', 'dimdepartment', 'dimjob', 'dimlocation']
    
    if table_name not in valid_tables:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    # Determine primary key column
    if table_name == 'dimemployee':
        pk_column = 'employee_id'
    elif table_name == 'dimdepartment':
        pk_column = 'departmentid'
    elif table_name == 'dimjob':
        pk_column = 'jobid'
    elif table_name == 'dimlocation':
        pk_column = 'locationid'
    
    delete_query = f"DELETE FROM {table_name} WHERE {pk_column} = %s"
    
    try:
        db.execute_query(delete_query, (id,))
        flash('Record deleted successfully!')
    except Exception as e:
        flash(f'Error deleting record: {str(e)}')
    
    return redirect(url_for('admin_tables', table_name=table_name))

@app.route('/admin/add/<table_name>', methods=['GET', 'POST'])
@admin_required
def admin_add(table_name):
    valid_tables = ['dimemployee', 'dimdepartment', 'dimjob', 'dimlocation']
    
    if table_name not in valid_tables:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        # Get columns for this table
        columns = db.get_table_columns(table_name)
        
        # Build INSERT query
        placeholders = []
        values = []
        
        for column in columns:
            if column in request.form:
                placeholders.append('%s')
                values.append(request.form[column])
            elif column == 'hire' and table_name == 'dimemployee':
                placeholders.append('%s')
                values.append(datetime.now().date())
            elif column == 'hiredate' and table_name == 'dimjob':
                placeholders.append('%s')
                values.append(datetime.now().date())
        
        # Get next ID if not provided
        if table_name == 'dimemployee' and 'employee_id' not in request.form:
            id_query = "SELECT COALESCE(MAX(employee_id), 0) + 1 FROM dimemployee"
            next_id = db.execute_query(id_query, fetch_one=True)
            if next_id:
                placeholders.insert(0, '%s')
                values.insert(0, next_id[0])
                # Adjust columns list
                if 'employee_id' not in columns[0]:
                    columns.insert(0, 'employee_id')
        
        insert_query = f"""
        INSERT INTO {table_name} ({', '.join([col for col in columns if col in request.form or col in ['employee_id', 'hire', 'hiredate']])})
        VALUES ({', '.join(placeholders)})
        """
        
        try:
            db.execute_query(insert_query, tuple(values))
            flash('Record added successfully!')
            return redirect(url_for('admin_tables', table_name=table_name))
        except Exception as e:
            flash(f'Error adding record: {str(e)}')
    
    # Get columns for display
    columns = db.get_table_columns(table_name)
    
    return render_template('admin_add.html',
                         table_name=table_name,
                         columns=columns)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)