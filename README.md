# Cartoons Boys — Loan Management System
Django web app with role-based access, SQLite database, and full CRUD.

## Setup & Run

```bash
# 1. Install Django
pip install django

# 2. Run migrations
python manage.py migrate

# 3. Seed data + create users
python manage.py seed_data

# 4. Start server
python manage.py runserver
```

Then open: http://127.0.0.1:8000

## Login Credentials

| Username | Password   | Role   | Access                          |
|----------|------------|--------|---------------------------------|
| admin    | admin123   | Admin  | Add, Edit, Delete, View, Users  |
| viewer   | viewer123  | Viewer | View dashboard & pending only   |

## User Roles

- **Admin (is_staff=True)** — Full access: add/edit/delete loans, manage users
- **Viewer (is_staff=False)** — Read-only: dashboard + pending summary

## Pages

- `/` — Dashboard with metrics, table, search, filter
- `/pending/` — Pending amounts summary
- `/add/` — Add new loan (admin only)
- `/edit/<id>/` — Edit loan (admin only)
- `/delete/<id>/` — Delete loan (admin only)
- `/users/` — User management (admin only)
- `/users/add/` — Create new user (admin only)

## Project Structure

```
cartoons_boys/         Django project settings
loans/
  models.py            LoanRecord model
  views.py             All views (auth, CRUD, users)
  forms.py             LoanRecordForm
  urls.py              URL routing
  admin.py             Django admin config
  templates/loans/     All HTML templates
    base.html           Shared layout + nav
    login.html          Login page
    dashboard.html      Main dashboard
    loan_form.html      Add/Edit form
    pending.html        Pending summary
    manage_users.html   User list (admin)
    add_user.html       Create user (admin)
  management/commands/
    seed_data.py        Data seeder command
db.sqlite3             SQLite database (auto-created)
```
