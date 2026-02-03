Interior Design Studio Portal

A professional full-stack web application designed for interior design studios to manage client inquiries (leads) through a secure, high-performance architecture.

Features

Lead Generation: Modern, responsive landing page with an asynchronous contact form.

Admin Dashboard: Secure area to view and manage project inquiries.

JWT Authentication: Robust security using JSON Web Tokens and password hashing (Bcrypt).

Async Architecture: Powered by FastAPI and SQLAlchemy 2.0 for high concurrency.

PostgreSQL Integration: Reliable data persistence for all client leads and user data.

Tech Stack

Backend: Python (FastAPI)

Database: PostgreSQL + SQLAlchemy (Async)

Security: OAuth2 with Password Bearer, JWT

Frontend: HTML5, CSS3, JavaScript (Fetch API)

Installation & Setup

Clone the repository:

git clone [https://github.com/Mohamed-shaaker/interior-design-backend.git](https://github.com/Mohamed-shaaker/interior-design-backend.git)

Setup Virtual Environment:

python -m venv .venv
source .venv/Scripts/activate

Install Dependencies:

pip install -r requirements.txt

Environment Configuration:

Update DATABASE_URL in src/database.py with your credentials.

Run the Server:

python -m uvicorn src.main:app --reload

Security Note

This project uses industry-standard hashing. Ensure you change the SECRET_KEY in src/core/security.py before deploying to a production environment.
