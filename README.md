## Overview

This repository contains the source code for a logo selling website built using Django, a high-level web framework for Python. The website allows users to browse, purchase, and manage logo products. This README provides instructions on setting up and running the project.

## Prerequisites
- Python installed on your machine.
- Git installed on your machine.
- Stripe account for handling payments.

## Setup

Clone the repository: 
 
```bash
git clone https://github.com/your-username/django-logo-shop.git
cd django-logo-shop
```

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```
Create a .env file in the project root directory:
```bash
SECRET_KEY=your_secret_key
STRIPE_SECRET_KEY=your_stripe_key
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run migrations:
```bash
python manage.py migrate
```
Create a superuser (admin):
```bash
python manage.py createsuperuser
```
Start the development server:
```bash
python manage.py runserver
```
Access the admin panel:

- Open a web browser and go to http://127.0.0.1:8000/admin/
- Log in with the superuser credentials created.

Post Products:

- Log in to the admin panel.
- Navigate to "Products" and add new products with relevant information.

Visit the Website:
- Open a web browser and go to http://127.0.0.1:8000/ to explore and purchase logo products.

## Important Notes
- Ensure your Stripe account is set up, and the provided Stripe secret key in the .env file is accurate for processing payments.
- This project is intended for educational purposes, and sensitive information like secret keys and passwords should be kept secure.
