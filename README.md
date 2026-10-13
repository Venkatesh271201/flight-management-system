# Flight Management System

A Django-based flight reservation application for managing flights, bookings, and user bookings.

## Features
- User registration and login
- Flight listing and details
- Flight booking with seat validation
- My Bookings page for logged-in users
- Admin support for managing flights and bookings

## Prerequisites
- Python 3.11+
- pip
- Git
- A terminal such as PowerShell, Command Prompt, or Bash

## Tech Stack
- Python
- Django 5.2.1
- SQLite (default local database)

## Clone the project

```bash
git clone <your-repository-url>
cd flight_mgmt
```

## Local Setup

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open the app at:
- http://127.0.0.1:8000/

## Create an admin user

```bash
python manage.py createsuperuser
```

Then open:
- http://127.0.0.1:8000/admin/

## Project Structure

- `manage.py` - Django entry point
- `flight_mgmt/` - project settings and URL configuration
- `reservation/` - app logic for flights and bookings
- `templates/` - HTML templates for the app
- `static/` - static assets
- `requirements.txt` - project dependencies
- `.gitignore` - ignores environment and local DB files

## Notes
- The project uses SQLite by default, so no external database server is required for local development.
- Local database files and virtual environments are ignored via `.gitignore`.
- Do not commit your local `db.sqlite3`, `venv/`, or `.env` files.
