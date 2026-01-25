# Employye_Management_System
A full-stack web application for managing employees, departments, jobs, and locations with secure authentication and role-based access control.



📋 Table of Contents
Features
Tech Stack
Installation
Database Setup
Running the Application
Project Structure
Screenshots
API Endpoints
Security Features
Contributing
License

✨ Features
👥 User Features
User Registration & Login with secure password hashing
Personal Dashboard with employee information
Profile Management (view and update personal details)
Role-based access (Admin vs Regular Employee)

👑 Admin Features
Complete CRUD Operations for all entities
Admin Dashboard with system statistics
Employee Management (Add, Edit, Delete, View)
Department Management
Job Position Management
Location Management
Data Filtering & Search capabilities
Pagination for large datasets
Export Data functionality

🔒 Security Features
Password Hashing using bcrypt
Session-based Authentication
Protected Routes with decorators
SQL Injection Prevention via parameterized queries
Role-based Access Control (RBAC)
🛠 Tech Stack
Backend
Python 3.8+ - Programming language
flask - Web framework
Flask-Session - Session management
psycopg2 - PostgreSQL database adapter
bcrypt - Password hashing

Database
PostgreSQL 15+ - Relational database
Database Schema with 4 main tables:
dimemployee - Employee information
dimdepartment - Department details
dimjob - Job positions
dimlocation - Office locations

Frontend
HTML5 - Markup
CSS3 - Styling with modern CSS
JavaScript - Client-side interactivity
Jinja2 - Templating engine
Font Awesome - Icons

🚀 Installation
Prerequisites
Python 3.8 or higher
PostgreSQL 15 or higher
pip (Python package manager)
