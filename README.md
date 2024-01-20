Django Logo Shop
Overview
This repository contains the source code for a logo selling website built using Django, a high-level web framework for Python. The website allows users to browse, purchase, and manage logo products. This README provides instructions on setting up and running the project.

Getting Started
Prerequisites
1. Python installed on your machine.
   git clone https://github.com/your-username/django-logo-shop.git
   cd django-logo-shop
3. Git installed on your machine.
   python -m venv venv
5. Stripe account for handling payments.

Setup
1. Clone the repository:
2. Create a virtual environment:
3. Activate the virtual environment:
   a. On Windows:
     venv\Scripts\activate
   b. On Mac:
     source venv/bin/activate
4. Create a .env file in the project root directory:
   SECRET_KEY=your_secret_key
   STRIPE_SECRET_KEY=your_stripe_key
   EMAIL_HOST_USER=your_email
   EMAIL_HOST_PASSWORD=your_email_password
5. Install dependencies:
   pip install -r requirements.txt
6. Run migrations:
   python manage.py migrate
7. Create a superuser (admin):
   python manage.py createsuperuser
8. Stat the development server:
   python manage.py runserver
9. Access the admin panel:
   Open a web browser and go to http://127.0.0.1:8000/admin/. Log in with the superuser credentials created in step 7.
10. Post Products:
    Log in to the admin panel.
    Navigate to "Products" and add new products with relevant information.
11. Visit the Website:
    Open a web browser and go to http://127.0.0.1:8000/ to explore and purchase logo products.

Important Notes
Ensure your Stripe account is set up, and the provided Stripe secret key in the .env file is accurate for processing payments.
This project is intended for educational purposes, and sensitive information like secret keys and passwords should be kept secure.
Feel free to customize the project as needed, and happy coding!
