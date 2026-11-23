# StrictScheduler

A role-based goal and routine scheduling web application built with Django and PostgreSQL (Supabase).

## Core Feature (Project Development 2): Goal and Routine Creation
StrictScheduler allows authenticated users to create, manage, and organize personal goals alongside chronological daily routines.

### Key Capabilities
- **Goal Management (CRUD):** Create, view, edit, and delete goals with categories, target dates, and status tracking.
- **Routine Scheduling (CRUD):** Link recurring routines (Daily, Weekdays, Weekends, Weekly) with start/end times to specific goals.
- **Chronological Schedule View:** Click any goal to view its assigned routines ordered from earliest to latest.
- **Role-Based Access:** Members manage their own goals and routines; Admins can monitor all users' goals and routines across the system.

## Local Setup
1. Clone the repository and create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Supabase/PostgreSQL database credentials and `SECRET_KEY`.
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
