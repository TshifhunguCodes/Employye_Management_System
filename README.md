# 🏢 Employee Management System

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3+-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue?logo=postgresql)
![bcrypt](https://img.shields.io/badge/bcrypt-4.0+-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A full-stack **Employee Management System** built with **Flask** (Python) and **PostgreSQL**, featuring role-based access (admin + employee), complete CRUD operations on 4 database tables, bcrypt password hashing, and a rich modern UI.

---

## 🎥 Live Demo

[![Employee Management System Demo](https://img.youtube.com/vi/L-6g4ur9ohM/0.jpg)](https://www.youtube.com/watch?v=L-6g4ur9ohM)

Watch the full walkthrough of the Employee Management System on YouTube — including employee login, registration, admin dashboard navigation, CRUD operations on all tables, and system statistics.

---

## 📋 Overview

This system provides a complete employee data management platform with:

- **Employee Portal** — Employees log in to view their personal info, salary, tenure, and company-wide statistics (total employees, average salary).
- **Admin Panel** — Administrators can manage all records across 4 database tables with full Create, Read, Update, Delete operations, pagination, search, and filtering.
- **Security** — bcrypt password hashing with automatic plaintext-to-bcrypt upgrade for legacy passwords.
- **Preloaded Demo Data** — 30 sample employees, 10 departments, 15 job positions, and 15 office locations.

---

## ✨ Features

| Feature | Description |
|---|---|
| ✅ **Employee Registration & Login** | Sign up with name, email, password, gender, birth date |
| ✅ **Admin Login (Hardcoded)** | Separate admin authentication bypassing the database |
| ✅ **Role-Based Access** | Regular users vs. admin with different dashboards |
| ✅ **bcrypt Password Hashing** | Passwords hashed with automatic plaintext upgrade |
| ✅ **Employee Dashboard** | View personal profile, salary, tenure, age, company stats |
| ✅ **Admin Dashboard** | Overview of all 4 tables with counts and quick actions |
| ✅ **Full CRUD Operations** | Create, Read, Update, Delete on all tables |
| ✅ **Paginated Tables** | 10 records per page with navigation |
| ✅ **Search & Filter** | Live search and column-based filtering |
| ✅ **Sortable Columns** | Click column headers to sort data |
| ✅ **PostgreSQL Money Type** | Handles `MONEY` column type with custom parsing |
| ✅ **Sticky Navigation Header** | Always-accessible nav with role-aware links |
| ✅ **Flash Messages** | Animated success/error/info/warning notifications |
| ✅ **Responsive Design** | Mobile-friendly layouts for all screen sizes |
| ✅ **Animated UI** | Number counters, progress bars, hover effects, fade-in animations |
| ✅ **Preloaded Seed Data** | 30 employees with bcrypt-hashed passwords, 15 locations, 10 departments, 15 jobs |

---

## 📁 Project Structure

```
Employye_Management_System/
│
├── app.py                        # Main Flask application (784 lines — routes, auth, CRUD, DB logic)
├── database.py                   # Legacy/alternative app file (older version, not the active one)
├── Raw_data.txt                  # SQL seed data for all 4 tables (30 employees, 10 depts, 15 jobs, 15 locations)
├── README.md                     # This file
│
├── static/
│   └── css/
│       └── (style files — referenced by templates)
│
├── templates/
│   ├── layout.html               # Base template (nav header, flash messages, responsive container)
│   ├── login.html                # Login page (email + password, demo credentials box, JS validation)
│   ├── register.html             # Registration form (6 fields, password strength meter, age check)
│   ├── user_dashboard.html       # Employee dashboard (profile info grid, stats cards, quick actions)
│   ├── admin_dashboard.html      # Admin overview (4 stat cards, nav tabs, actions grid, activity feed)
│   ├── admin_tables.html         # Data table view (paginated, sortable, searchable, CRUD buttons)
│   ├── admin_add.html            # Add record form (dynamic fields per table)
│   └── admin_edit.html           # Edit record form (pre-populated fields)
│
└── Database_Schema/
    └── employee-management-schema.pgerd  # Visual database schema (pgAdmin ERD file)
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+ / Flask 2.3+ |
| **Database** | PostgreSQL 16+ |
| **Password Hashing** | bcrypt 4.0+ (with plaintext backward compatibility) |
| **Frontend** | HTML5, CSS3 (vanilla — no JS frameworks) |
| **Icons** | Font Awesome 6.0+ |
| **Database Driver** | psycopg2 (with `DictCursor` for named columns) |

---

## 🗄 Database Schema

The system uses **4 tables** with a star-schema-like design (`dim` prefix suggests a dimensional modelling approach).

### Table: `dimemployee`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `employee_id` | `INTEGER` | `PRIMARY KEY` | Auto-incrementing employee ID |
| `firstname` | `VARCHAR(50)` | — | Employee's first name |
| `lastname` | `VARCHAR(50)` | — | Employee's last name |
| `gender` | `VARCHAR(10)` | — | Male / Female / Other |
| `email` | `VARCHAR(50)` | — | Email address (used as login) |
| `birthdate` | `DATE` | — | Date of birth |
| `hire` | `DATE` | — | Hire date |
| `salary` | `MONEY` | — | Salary in PostgreSQL money format (`$XX,XXX.XX`) |
| `passwords` | `VARCHAR(100)` | — | bcrypt-hashed password |

### Table: `dimdepartment`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `departmentid` | `BIGINT` | `PRIMARY KEY` | Department ID |
| `departmentname` | `VARCHAR` | — | Name of the department |
| `departmentrole` | `VARCHAR` | — | Role / description of the department |

### Table: `dimjob`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `jobid` | `INTEGER` | `PRIMARY KEY` | Job ID |
| `jobtitle` | `VARCHAR(50)` | — | Job title / position name |
| `hiredate` | `DATE` | — | Date the position was created |

### Table: `dimlocation`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `locationid` | `BIGINT` | `PRIMARY KEY` | Location ID |
| `city` | `VARCHAR` | — | City name |
| `state` | `VARCHAR` | — | State abbreviation |
| `province` | `VARCHAR` | — | Province / region name |

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/TshifhunguCodes/Employye_Management_System.git
cd Employye_Management_System
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install flask psycopg2-binary bcrypt
```

### 4. Set Up PostgreSQL Database

Open your PostgreSQL client and run:

```sql
CREATE DATABASE "EmployeeDB";
```

### 5. Run the Auto-Initialization

Start the Flask app and visit the **database initialization** endpoint to create all tables and seed data automatically:

```bash
python app.py
```

Then open your browser and navigate to:

```
http://localhost:5000/init-db
```

This will:
- Create all 4 tables (`dimemployee`, `dimdepartment`, `dimjob`, `dimlocation`) with the exact schema
- Create an **admin user** (email: `admin@example.com`, password: `admin123`) with a bcrypt-hashed password
- You can also manually insert seed data from `Raw_data.txt` for sample employees, departments, jobs, and locations

### 6. (Optional) Load Seed Data

For a fully populated system, run the SQL in `Raw_data.txt` via `psql` or pgAdmin. This inserts:
- **30 employees** with realistic data and bcrypt-hashed passwords
- **10 departments**
- **15 job positions**
- **15 office locations**

Each employee's password is the bcrypt hash of `password123`:
```sql
-- bcrypt hash used: $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
```

### 7. Configure Database Credentials

Edit **`app.py`** and update the `DB_CONFIG` dictionary:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'EmployeeDB',
    'user': 'postgres',
    'password': 'your_password_here',
    'port': '5432'
}
```

### 8. Run the Application

```bash
python app.py
```

The server starts at `http://0.0.0.0:5000` → open `http://localhost:5000`.

---

## 🌐 Application Routes

| Method | Route | Description | Auth Required |
|---|---|---|---|
| `GET` | `/` | Root — redirects to dashboard or login | No |
| `GET`/`POST` | `/login` | Login form and authentication | No |
| `GET`/`POST` | `/register` | Registration form and new user creation | No |
| `GET` | `/dashboard` | Employee personal dashboard (profile + stats) | **Yes (user)** |
| `GET` | `/admin` | Admin dashboard (4-table overview + quick actions) | **Yes (admin)** |
| `GET` | `/admin/tables/<table_name>` | Paginated data table for a specific table | **Yes (admin)** |
| `GET`/`POST` | `/admin/add/<table_name>` | Add a new record to a table | **Yes (admin)** |
| `GET`/`POST` | `/admin/edit/<table_name>/<id>` | Edit an existing record | **Yes (admin)** |
| `GET` | `/admin/delete/<table_name>/<id>` | Delete a record (with confirmation modal) | **Yes (admin)** |
| `GET` | `/logout` | Clear session and log out | No |
| `GET` | `/test-db` | Test database connection and verify tables exist | No |
| `GET` | `/init-db` | Auto-create tables and admin user | No |

---

## 👥 User Roles

### Employee (Regular User)
- Register via the registration form (`/register`)
- Log in with email and password
- View personal profile: name, email, gender, birthdate, age, hire date, tenure, salary
- View company-wide statistics: total employees, average salary
- Quick action placeholders (Update Profile, Change Password, View Colleagues, Export Data)
- Cannot access any `/admin/` routes

### Administrator
- Log in with **hardcoded credentials** bypassing the database:
  - **Email:** `admin@company.com`
  - **Password:** `admin123`
- Access the admin dashboard with statistics for all 4 tables
- Navigate between table management views via tab navigation
- Perform **Create, Read, Update, Delete** on any table record
- Each table view supports pagination (10/25/50/100 per page), search, and column sorting

---

## 🔒 Security Features

| Security Measure | Implementation |
|---|---|
| **Password Hashing** | `bcrypt.gensalt()` + `bcrypt.hashpw()` on registration and admin-initiated password changes |
| **Password Verification** | `bcrypt.checkpw()` for bcrypt hashes; plaintext comparison fallback |
| **Auto-Upgrade** | Plaintext passwords are automatically re-hashed with bcrypt on successful login |
| **Session Authentication** | Flask signed cookies with `login_required` and `admin_required` decorators |
| **Protected Routes** | All `/dashboard` and `/admin/*` routes protected by decorators |
| **SQL Injection Protection** | Parameterised queries (`%s` placeholders) throughout |

---

## 💰 PostgreSQL Money Type Handling

The `salary` column uses PostgreSQL's `MONEY` type, which renders as strings like `$85,000.00`. A `parse_money()` helper function **safely converts** these strings to floats:

```python
def parse_money(money_str):
    # Handles: "$50,000.00", "50000.00", None, int, float
    cleaned = money_str.replace('$', '').replace(',', '').strip()
    return float(cleaned)
```

This is used across admin tables, employee dashboard, and statistics calculations. The app also provides a custom Jinja2 filter `format_currency` for displaying formatted values in templates.

---

## 📊 Key Functionality Details

### Password Transition Logic (`app.py` lines 242-260)
The login system supports **backward compatibility** with plaintext passwords:
1. If stored password starts with `$2b$` → verify with bcrypt
2. If stored password is plaintext → compare directly
3. If plaintext matches → auto-upgrade to bcrypt hash in the database

### Table Structure Dictionary (`app.py` lines 22-66)
All 4 tables are defined in a `TABLE_STRUCTURE` dictionary with:
- Column names
- Primary key field
- PostgreSQL data types
This drives all dynamic CRUD queries — no hardcoded SQL per table.

### Admin Table Statistics (`app.py` lines 416-461)
Each table view calculates context-specific stats:
- **dimemployee**: Active employees count, department count, average salary
- **dimdepartment**: Total employees, total budget
- **dimjob**: Total jobs, average salary range
- **dimlocation**: Total locations, distinct provinces/countries

---

## 🎨 UI / UX Highlights

- **Gradient-based design** — purple-blue gradients (`#667eea → #764ba2`) throughout
- **Sticky header** — always-visible navigation with role-appropriate links
- **Animated flash messages** — slide-down success (green), error (red), info (blue), warning (orange)
- **Employee dashboard** — split into profile info grid (left) and stats cards (right), with quick actions below
- **Admin dashboard** — 4 stat cards with progress bars, tab navigation, action cards, recent activity feed
- **Data tables** — responsive with hover effects, colour-coded badges (gender, active status), currency formatting
- **Password strength meter** — real-time feedback on registration form
- **Age validation** — checks that registrants are 18+ based on birth date
- **Password visibility toggle** — eye icon to show/hide password on both login and register forms
- **Number animations** — stats count up on page load for visual polish
- **Responsive breakpoints** — 1200px, 768px, 480px for tablets and mobile

---

## 📦 Seed Data Summary

| Entity | Count | Details |
|---|---|---|
| **Employees** | 30 | Realistic names, emails, ages, salaries (59K–112K), bcrypt-hashed passwords |
| **Departments** | 10 | HR, IT, Finance, Marketing, Sales, Operations, R&D, Customer Service, Legal, Admin |
| **Job Positions** | 15 | Engineer, Manager, Analyst, Director, Executive, Specialist, etc. |
| **Locations** | 15 | Major US cities across different states and regions |

All sample employees use the password `password123` (already bcrypt-hashed in the seed data).

---

## 🔮 Future Enhancements

- [ ] **Password Reset Flow** — Forgot password with email token
- [ ] **Profile Editing** — Allow employees to update their own info from the dashboard
- [ ] **Role Management** — Dynamic roles instead of hardcoded admin email check
- [ ] **Department Assignment** — Link employees to departments via foreign keys
- [ ] **File Upload** — Profile pictures, documents
- [ ] **Export to CSV/PDF** — Download table data from admin panel
- [ ] **Audit Logging** — Track who created/edited/deleted records
- [ ] **CSRF Protection** — Flask-WTF tokens on all forms
- [ ] **Database Migrations** — Alembic/Flask-Migrate for schema versioning
- [ ] **REST API** — Expose endpoints for external integrations

---

## ⚠️ Known Notes

1. **Hardcoded Admin** — The admin login uses hardcoded credentials (`admin@company.com` / `admin123`) and does **not** check the database. The session email is overridden to `admin@example.com` for the `admin_required` decorator check.
2. **Two Versions of `app.py`** — The root `app.py` is the **active, feature-rich version** (784 lines). The `database.py` file is an older/alternative version (367 lines) that imports from a `database` module and does not include bcrypt or pagination.
3. **`MONEY` Data Type** — PostgreSQL's `MONEY` type is locale-dependent and may behave differently across database configurations. The `parse_money()` function strips `$` and commas, which assumes USD format.
4. **No Foreign Keys** — Despite the relational-looking structure, there are **no foreign key constraints** between the `dim` tables. Relationships are conceptual rather than enforced at the database level.

---

## 👨‍💻 Author

**TshifhunguCodes**  
[GitHub Profile](https://github.com/TshifhunguCodes)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using Flask, PostgreSQL & bcrypt
</p>