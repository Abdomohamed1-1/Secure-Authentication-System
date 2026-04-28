# 🛡️ Secure Authentication System (RBAC & 2FA)

This project is a robust and secure web-based authentication system built with **Flask**. It implements high-level security standards to ensure **Data Integrity**, **Confidentiality**, and **Accountability**.

## 🌟 Key Features

* **Secure Authentication**: Passwords are never stored in plain text. We use **Bcrypt** for strong password hashing and salting.
* **Two-Factor Authentication (2FA)**: Extra security layer using **TOTP** (Time-based One-Time Password) compatible with Google/Microsoft Authenticator.
* **Role-Based Access Control (RBAC)**: Secure routing based on user roles (`Admin`, `Manager`, `User`).
* **JWT Security**: Session management using **JSON Web Tokens (JWT)** stored in secure, HTTP-only cookies.
* **Data Integrity**: Built-in protection against common vulnerabilities and unauthorized data modification.

## 🛠️ Tech Stack

* **Backend**: Python / Flask
* **Security**: Flask-JWT-Extended, Flask-Bcrypt, PyOTP
* **Database**: SQLite (Relational Database)
* **Frontend**: HTML5, CSS3 (Modern Responsive UI)

## 🚀 Getting Started

### 1. Prerequisites
Make sure you have Python installed, then install the dependencies:
```bash
pip install -r requirements.txt

SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_key
DATABASE_NAME=database.db

python init_db.py

python app.py