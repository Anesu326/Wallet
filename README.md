# Wallet

## Pocket Money 
Django-based web application for sending money abroad with automatic currency conversion, transaction tracking and user friendly interface.

## Features
- User Registration and Login
- Send money to recipients via Name and Email
- Real-time FX rate conversion (USD to GBP/ZAR)
- Fee calculation (10% for GBP and 20% for ZAR)
- Transaction history with pagination
- Receipt and Details confirmation modals
- Bootsrap-styled UI with carousel

## Technology Stack
- Python 3.11.4
- Django
- Bootstrap 5
- SQLite (default)
- HTML
- CSS
- JavaScript

## Installation
1. Clone the repository
git clone https://github.com/Anesu326/Wallet.git

2. Create and activate a virtual environment
Run `python -m venv env` in terminal for windows and `source env/bin/activate` for MacOS/Linux

3. Install dependencies
`pip install -r requirements.txt`

4. Run migrations
`python manage.py migrate`

5. Create a superuser (Administrator)
`python manage.py createsuperuser`

6. Start the server
`python manage.py runserver`

7. Visit `http://127.0.0.1:8000/register/` to run the web app.

## Notes
- Minimum amount to send: $10
- FX rates are dynamic via an API
