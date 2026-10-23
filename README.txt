SMART SHOP MANAGEMENT SYSTEM — FULL-STACK MINI PROJECT

WHAT IS INCLUDED
- Professional responsive dashboard and inventory UI
- Django REST API backend
- SQLite database (created locally on first migration)
- Product create/list/delete, inventory search and category filter
- Sales recording with payment method and automatic stock deduction
- Dashboard metrics, low-stock alerts, category breakdown, recent sales
- CSV export for inventory
- Optional demo seeder with 15 sample products and sample transactions

REQUIREMENTS
- Python 3.10 or newer
- Internet is needed only if pip has to download Django and Django REST Framework

RUN ON WINDOWS (VS CODE TERMINAL)
1. Extract this ZIP to a folder, for example Desktop\Smart_Shop_Management_System.
2. Open that extracted folder in VS Code.
3. Open Terminal > New Terminal.
4. Run these commands one by one:

   cd backend
   py -m venv .venv
   .venv\Scripts\activate
   py -m pip install -r requirements.txt
   py manage.py makemigrations inventory
   py manage.py migrate
   py manage.py runserver

   If the command `py` is not recognised, use `python` instead.

5. Keep the terminal running. Open this in Chrome:
   http://127.0.0.1:8000/
6. Click Store settings > Load demo data to populate the dashboard. The demo seeder only runs on an empty database; it will not overwrite existing data.
7. Try Add product, Record sale, search, category filter and Export CSV.

API ENDPOINTS
- GET /api/dashboard/
- GET, POST /api/products/
- PATCH, DELETE /api/products/<id>/
- GET, POST /api/sales/
- POST /api/demo-data/
- Django admin: /admin/ (create an admin user with `py manage.py createsuperuser` if needed)

IMPORTANT
This is a local academic learning project. It does not include user login or production security. Do not expose it publicly or use it for real business records without adding authentication, permissions, backups, validation and production security settings. Sample sales and prices are fictional; replace them with your own test data as appropriate.
