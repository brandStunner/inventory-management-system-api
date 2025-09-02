# 📦 Inventory Management API (Flask + PostgreSQL)

A simple **Inventory Management System API** built using **Flask** and **SQLAlchemy**, with PostgreSQL as the database.  
The API supports user authentication (registration, login, logout) and secure CRUD operations for inventory items.

---

## 🚀 Features
- 👤 **User Authentication**
  - Register with a unique username
  - Secure password storage (hashed using Werkzeug)
  - Login & logout with session-based authentication
- 📦 **Inventory Management**
  - Add new items
  - View all items
  - Retrieve specific items by ID
  - Update item details
  - Delete items
- 🔒 **Protected Routes**
  - Only authenticated users can add, update, or delete inventory items
  - Viewing is open to all users

---

## 🛠️ Tech Stack
- **Backend Framework:** Flask (Python)
- **Database ORM:** SQLAlchemy
- **Database:** PostgreSQL (local or cloud-based, e.g., ElephantSQL)
- **Environment Management:** python-dotenv
- **Security:** Werkzeug password hashing, Flask session cookies

---

## 📂 Project Structure
```
│── app.py # Main Flask app
│── requirements.txt # Dependencies
│── .env # Environment variables
│── README.md # Documentation
```
## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

git clone https://github.com/brandStunner/inventory-management-system-api.git
cd inventory-api

2️⃣ Create Virtual Environment
python -m venv venv
source venv/Scripts/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the project root:

SESSION_SECRET_KEY=your_secret_key_here

DB_USER=postgres #use your actual user set on your postgres if it's different
DB_PASSWORD=your_db_password #use actual password that you set when installing postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=inventory

(🔑 Replace values with your actual PostgreSQL credentials)

---
## Run the App
python app.py

## API Endpoints
🔐 Authentication

POST /register  # Register a new user

{"username": "john", "password": "mypassword"}

POST /login  #Login a user

Inventory
GET /inventory → Get all items (requires login)

GET /inventory/<id> → Get a single item

POST /inventory → Add new item (requires login)

PUT /inventory/<id> → Update an item (requires login)

DELETE /inventory/<id> → Delete an item (requires login)

Example request body for POST /inventory:

{
  "name": "Laptop",
  "sku": "LAP123",
  "quantity": 10,
  "price": 1200.50,
  "description": "High-performance laptop"
}

# 🌍 Deployment

Local: Use PostgreSQL installed on your machine

Cloud: Use ElephantSQL
 (free Postgres hosting)

Hosting options: Render
 or Railway

 👨‍💻 Author

Built by Built by [Kofi Brandful] (https://x.com/pointbrandrange)
