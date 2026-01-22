from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os
import psycopg2
import psycopg2.extras
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this-in-production'

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'EmployeeDB',
    'user': 'postgres',
    'password': 'Tshifhungu12@',
    'port': '5432'
}

# Exact Table Structure
TABLE_STRUCTURE = {
    'dimemployee': {
        'columns': ['employee_id', 'firstname', 'lastname', 'gender', 'email', 'birthdate', 'hire', 'salary', 'passwords'],
        'pk': 'employee_id',
        'types': {
            'employee_id': 'integer',
            'firstname': 'character varying(50)',
            'lastname': 'character varying(50)',
            'gender': 'character varying(10)',
            'email': 'character varying(50)',
            'birthdate': 'date',
            'hire': 'date',
            'salary': 'money',
            'passwords': 'character varying(100)'
        }
    },
    'dimdepartment': {
        'columns': ['departmentid', 'departmentname', 'departmentrole'],
        'pk': 'departmentid',
        'types': {
            'departmentid': 'bigint',
            'departmentname': 'character varying',
            'departmentrole': 'character varying'
        }
    },
    'dimjob': {
        'columns': ['jobid', 'jobtitle', 'hiredate'],
        'pk': 'jobid',
        'types': {
            'jobid': 'integer',
            'jobtitle': 'character varying(50)',
            'hiredate': 'date'
        }
    },
    'dimlocation': {
        'columns': ['locationid', 'city', 'state', 'province'],
        'pk': 'locationid',
        'types': {
            'locationid': 'bigint',
            'city': 'character varying',
            'state': 'character varying',
            'province': 'character varying'
        }
    }
}

# Database Connection Functions
def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch=False, fetch_one=False):
    """Execute SQL query and return results"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch:
            result = cursor.fetchall()
        else:
            result = None
        
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        print(f"Query execution error: {e}")
        return None

def get_table_columns(table_name):
    """Get column names for a table using our predefined structure"""
    if table_name in TABLE_STRUCTURE:
        return TABLE_STRUCTURE[table_name]['columns']
    return []

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

def get_table_data(table_name, id=None, page=1, per_page=10):
    """Get data from table - all records or specific ID with pagination"""
    if table_name not in TABLE_STRUCTURE:
        return None
    
    pk_column = TABLE_STRUCTURE[table_name]['pk']
    
    if id:
        query = f"SELECT * FROM {table_name} WHERE {pk_column} = %s"
        return execute_query(query, (id,), fetch_one=True)
    else:
        offset = (page - 1) * per_page
        query = f"SELECT * FROM {table_name} ORDER BY {pk_column} LIMIT %s OFFSET %s"
        return execute_query(query, (per_page, offset), fetch=True)

def get_table_counts():
    """Get counts for all tables"""
    counts = {}
    
    for table_name in TABLE_STRUCTURE.keys():
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = execute_query(query, fetch_one=True)
        counts[table_name] = result[0] if result else 0
    
    return counts

def get_table_count(table_name):
    """Get count for a specific table"""
    query = f"SELECT COUNT(*) FROM {table_name}"
    result = execute_query(query, fetch_one=True)
    return result[0] if result else 0

# Helper function to parse PostgreSQL money string to float
def parse_money(money_str):
    """Convert PostgreSQL money string to float"""
    if money_str is None:
        return 0.0
    try:
        # If it's already a float, return it
        if isinstance(money_str, (int, float)):
            return float(money_str)
        
        # If it's a string like "$50,000.00" or "50000.00"
        money_str = str(money_str).strip()
        
        # Remove currency symbols, commas, and whitespace
        cleaned = money_str.replace('$', '').replace(',', '').strip()
        
        # Convert to float
        return float(cleaned)
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Error parsing money value '{money_str}': {e}")
        return 0.0

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
        user = execute_query(query, (email, password), fetch_one=True)
        
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
        existing_user = execute_query(check_query, (email,), fetch_one=True)
        
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('register'))
        
        # Get next employee ID
        id_query = "SELECT COALESCE(MAX(employee_id), 0) + 1 FROM dimemployee"
        next_id = execute_query(id_query, fetch_one=True)
        employee_id = next_id[0] if next_id else 1
        
        # Insert new employee
        insert_query = """
        INSERT INTO dimemployee (employee_id, firstname, lastname, gender, email, 
                                birthdate, hire, salary, passwords)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            execute_query(insert_query, (
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
    user = execute_query(user_query, (session['user_id'],), fetch_one=True)
    
    if not user:
        flash('User not found')
        return redirect(url_for('logout'))
    
    # Parse user salary safely
    user_salary = parse_money(user.get('salary'))
    
    # Get predefined data tasks
    # Task 1: Count total employees
    count_query = "SELECT COUNT(*) FROM dimemployee"
    total_result = execute_query(count_query, fetch_one=True)
    total_employees = total_result[0] if total_result else 0
    
    # Task 2: Get average salary (excluding 0) - FIXED for MONEY type
    # Use numeric casting in the query
    avg_query = """
    SELECT AVG(CAST(REPLACE(REPLACE(salary::text, '$', ''), ',', '') AS NUMERIC)) 
    FROM dimemployee 
    WHERE CAST(REPLACE(REPLACE(salary::text, '$', ''), ',', '') AS NUMERIC) > 0
    """
    avg_result = execute_query(avg_query, fetch_one=True)
    avg_salary = 0.0
    if avg_result and avg_result[0]:
        try:
            avg_salary = float(avg_result[0])
        except (ValueError, TypeError):
            avg_salary = 0.0
    
    # Get current year for calculations
    now = datetime.now()
    
    return render_template('user_dashboard.html', 
                         user=user, 
                         user_salary=user_salary,  # Pass parsed salary
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
    if table_name not in TABLE_STRUCTURE:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    # Get page from query parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get total records count
    total_records = get_table_count(table_name)
    
    # Calculate total pages
    total_pages = (total_records + per_page - 1) // per_page if per_page > 0 else 1
    
    # Get paginated data
    data = get_table_data(table_name, page=page, per_page=per_page)
    
    # Get column names from our structure
    columns = TABLE_STRUCTURE[table_name]['columns']
    
    return render_template('admin_tables.html',
                         table_name=table_name,
                         data=data,
                         columns=columns,
                         page=page,
                         total_pages=total_pages,
                         total_records=total_records,
                         parse_money=parse_money)  # Pass helper function

@app.route('/admin/edit/<table_name>/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(table_name, id):
    if table_name not in TABLE_STRUCTURE:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    # Get existing record
    item = get_table_data(table_name, id)
    
    if not item:
        flash('Record not found')
        return redirect(url_for('admin_tables', table_name=table_name))
    
    if request.method == 'POST':
        # Get columns for this table
        columns = TABLE_STRUCTURE[table_name]['columns']
        pk_column = TABLE_STRUCTURE[table_name]['pk']
        
        # Build UPDATE query
        set_clauses = []
        values = []
        
        for column in columns:
            if column in request.form and column != pk_column and column != 'passwords':
                set_clauses.append(f"{column} = %s")
                values.append(request.form[column])
        
        if set_clauses:
            # Add the ID value at the end
            values.append(id)
            
            update_query = f"""
            UPDATE {table_name} 
            SET {', '.join(set_clauses)}
            WHERE {pk_column} = %s
            """
            
            try:
                execute_query(update_query, tuple(values))
                flash('Update successful!')
                return redirect(url_for('admin_tables', table_name=table_name))
            except Exception as e:
                flash(f'Error updating record: {str(e)}')
    
    # Get columns for display
    columns = TABLE_STRUCTURE[table_name]['columns']
    
    return render_template('admin_edit.html',
                         table_name=table_name,
                         item=item,
                         columns=columns,
                         parse_money=parse_money)

@app.route('/admin/delete/<table_name>/<int:id>')
@admin_required
def admin_delete(table_name, id):
    if table_name not in TABLE_STRUCTURE:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    pk_column = TABLE_STRUCTURE[table_name]['pk']
    delete_query = f"DELETE FROM {table_name} WHERE {pk_column} = %s"
    
    try:
        execute_query(delete_query, (id,))
        flash('Record deleted successfully!')
    except Exception as e:
        flash(f'Error deleting record: {str(e)}')
    
    return redirect(url_for('admin_tables', table_name=table_name))

@app.route('/admin/add/<table_name>', methods=['GET', 'POST'])
@admin_required
def admin_add(table_name):
    if table_name not in TABLE_STRUCTURE:
        flash('Invalid table name')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        columns = TABLE_STRUCTURE[table_name]['columns']
        pk_column = TABLE_STRUCTURE[table_name]['pk']
        
        # Build INSERT query
        placeholders = []
        values = []
        insert_columns = []
        
        for column in columns:
            if column in request.form and request.form[column]:
                insert_columns.append(column)
                placeholders.append('%s')
                values.append(request.form[column])
            elif column == 'hire' and table_name == 'dimemployee':
                insert_columns.append(column)
                placeholders.append('%s')
                values.append(datetime.now().date())
            elif column == 'hiredate' and table_name == 'dimjob':
                insert_columns.append(column)
                placeholders.append('%s')
                values.append(datetime.now().date())
        
        # Get next ID if not provided
        if column == pk_column and pk_column not in request.form:
            id_query = f"SELECT COALESCE(MAX({pk_column}), 0) + 1 FROM {table_name}"
            next_id = execute_query(id_query, fetch_one=True)
            if next_id:
                insert_columns.insert(0, pk_column)
                placeholders.insert(0, '%s')
                values.insert(0, next_id[0])
        
        insert_query = f"""
        INSERT INTO {table_name} ({', '.join(insert_columns)})
        VALUES ({', '.join(placeholders)})
        """
        
        try:
            execute_query(insert_query, tuple(values))
            flash('Record added successfully!')
            return redirect(url_for('admin_tables', table_name=table_name))
        except Exception as e:
            flash(f'Error adding record: {str(e)}')
    
    # Get columns for display
    columns = TABLE_STRUCTURE[table_name]['columns']
    
    return render_template('admin_add.html',
                         table_name=table_name,
                         columns=columns)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/test-db')
def test_db():
    """Test database connection"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            
            # Check if tables exist
            tables_exist = []
            for table_name in TABLE_STRUCTURE.keys():
                cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')")
                exists = cursor.fetchone()[0]
                tables_exist.append(f"{table_name}: {'✓' if exists else '✗'}")
            
            cursor.close()
            conn.close()
            
            return f"""
            <h2>Database Connection Test</h2>
            <p><strong>PostgreSQL version:</strong> {db_version[0]}</p>
            <p><strong>Database:</strong> {DB_CONFIG['database']}</p>
            <p><strong>Tables check:</strong></p>
            <ul>
                {''.join([f'<li>{table}</li>' for table in tables_exist])}
            </ul>
            <p><a href="/">Back to Home</a></p>
            """
        else:
            return "<h2>Failed to connect to database</h2><p><a href='/'>Back to Home</a></p>"
    except Exception as e:
        return f"""
        <h2>Database connection error</h2>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><strong>Current DB Config:</strong></p>
        <ul>
            <li>Host: {DB_CONFIG['host']}</li>
            <li>Database: {DB_CONFIG['database']}</li>
            <li>User: {DB_CONFIG['user']}</li>
            <li>Port: {DB_CONFIG['port']}</li>
        </ul>
        <p><a href="/">Back to Home</a></p>
        """

@app.route('/init-db')
def init_db():
    """Create tables if they don't exist (EXACTLY matching your schema)"""
    conn = get_db_connection()
    if not conn:
        return "Failed to connect to database"
    
    try:
        cursor = conn.cursor()
        
        # Create dimemployee table (EXACTLY as in your screenshot)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dimemployee (
            employee_id INTEGER PRIMARY KEY,
            firstname CHARACTER VARYING(50),
            lastname CHARACTER VARYING(50),
            gender CHARACTER VARYING(10),
            email CHARACTER VARYING(50),
            birthdate DATE,
            hire DATE,
            salary MONEY,
            passwords CHARACTER VARYING(100)
        )
        """)
        
        # Create dimdepartment table (EXACTLY as in your screenshot)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dimdepartment (
            departmentid BIGINT PRIMARY KEY,
            departmentname CHARACTER VARYING,
            departmentrole CHARACTER VARYING
        )
        """)
        
        # Create dimjob table (EXACTLY as in your screenshot)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dimjob (
            jobid INTEGER PRIMARY KEY,
            jobtitle CHARACTER VARYING(50),
            hiredate DATE
        )
        """)
        
        # Create dimlocation table (EXACTLY as in your screenshot)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dimlocation (
            locationid BIGINT PRIMARY KEY,
            city CHARACTER VARYING,
            state CHARACTER VARYING,
            province CHARACTER VARYING
        )
        """)
        
        # Add admin user if not exists
        cursor.execute("SELECT COUNT(*) FROM dimemployee WHERE email = 'admin@example.com'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            cursor.execute("""
            INSERT INTO dimemployee (employee_id, firstname, lastname, email, passwords, gender, hire, salary)
            VALUES (9999, 'Admin', 'User', 'admin@example.com', 'admin123', 'Other', CURRENT_DATE, 0)
            """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return """
        <h2>Database Initialized Successfully!</h2>
        <p>All tables have been created with the exact structure from your screenshots.</p>
        <p><strong>Tables created:</strong></p>
        <ul>
            <li>dimemployee (with columns: employee_id, firstname, lastname, gender, email, birthdate, hire, salary, passwords)</li>
            <li>dimdepartment (with columns: departmentid, departmentname, departmentrole)</li>
            <li>dimjob (with columns: jobid, jobtitle, hiredate)</li>
            <li>dimlocation (with columns: locationid, city, state, province)</li>
        </ul>
        <p><strong>Admin user created:</strong> admin@example.com / admin123</p>
        <p><a href="/">Go to Login</a></p>
        """
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return f"Error initializing database: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)