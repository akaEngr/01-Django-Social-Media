# 01-Django-Social-Media

# SocialMedia

A simple social media web application built using **Python and Django**. The project allows users to create and manage posts, interact with posts through likes and comments, and manage their accounts.

## 🚀 Features

### Account App

* User Sign Up
* User Login
* User Authentication

### Content App

* Create Post
* View Posts
* Update Post
* Delete Post
* Like Post
* Comment on Post

## 🛠️ Technologies Used

* **Python**
* **Django**
* **SQLite**
* **HTML**
* **CSS**
* **Django Templates**

## 📁 Project Structure

```text
SocialMedia/
│
├── account/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── content/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── socialmedia/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd socialmedia
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

### 4. Install Django

```bash
pip install django
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## 🔐 Authentication

Users can create an account through the **Sign Up** page and log in through the **Login** page.

After authentication, users can access the social media features provided by the application.

## 📌 Main Functionality

```text
User
 │
 ├── Sign Up
 ├── Login
 │
 └── Content
      ├── Create Post
      ├── View Post
      ├── Update Post
      ├── Delete Post
      ├── Like Post
      └── Comment on Post
```

## 🗄️ Database

The project uses **Django's default SQLite database** for storing application data.

Django ORM is used to interact with the database.

## 🎯 Project Objective

The main objective of this project was to understand and implement core Django concepts such as:

* Django project and app structure
* URL routing
* Views
* Templates
* Models
* Django ORM
* Authentication
* CRUD operations
* Database relationships
* User interaction through likes and comments

## 👨‍💻 Author

**Anshul Gupta**

Python / Django Developer
