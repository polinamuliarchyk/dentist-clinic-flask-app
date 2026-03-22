# DentalCare - Dental Management System

**Author:** Palina Muliarchyk  
**Project Type:** Pet project

A modern web application for a dental clinic, developed using the Flask framework. The system fully automates the patient appointment process: from selecting services to managing visit history.

## Key Features
* Secure Authentication: Registration and login with password hashing via Werkzeug.
* Multiple Service Selection: Ability to choose multiple services for a single visit (Many-to-Many relationship).
* Smart Booking: Selection of a specific dentist and real-time date availability check.
* User Dashboard: Complete visit history with filtering by doctor/date and sorting capabilities.
* Visit Management: Functionality to cancel upcoming appointments and delete past records.
* Premium Design: Navy Blue themed interface using the Inria Serif font.

## Tech Stack
* Backend: Python 3.x, Flask (Blueprints)
* Database: SQLite + SQLAlchemy (ORM)
* Security: PBKDF2 password hashing
* Frontend: Jinja2, HTML5, CSS3 (Grid & Flexbox), Vanilla JS

## Installation & Local Setup

### 1. Clone the repository
Extract the project files into your chosen directory or clone the repo.

### 2.  Create a virtual environment (Recommended)
``` bash
python -m venv venv
```

#### Activation:
* Windows: venv\Scripts\activate
* Linux/Mac: source venv/bin/activate

### 3. Install dependencies
``` bash 
pip install -r requirements.txt
```

### 4. Run the server
``` bash
python manage.py runserver
```

Visit http://127.0.0.1:5000/ to see the DentalCare in action!

## Data Architecture
Advanced database concepts implemented in the project:

1. Many-to-Many: Relationship between Visit and Service via the visit_services association table.

2. Inheritance: Polymorphic inheritance (Dentist inherits from the Person base class).

3. Enums: Strict contract types (FULLTIME, PARTTIME, B2B).
