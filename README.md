# 📋 Task Management Web App
<img width="1878" height="922" alt="image" src="https://github.com/user-attachments/assets/cc51ee8a-d970-4b87-afaf-d4aef98cb5ea" />



A modern, full-featured task management system built with **Flask**, **HTML/CSS/JS**, and **SQLite**. Designed for administrators to assign, track, and manage employee tasks through a sleek dark-mode dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Admin Authentication** | Secure login/logout with hashed passwords via Flask-Login |
| 📊 **Dashboard Stats** | Real-time counters for total, completed, and pending tasks |
| ➕ **Add Tasks** | Create tasks with employee name, task title (dropdown), and status |
| ✏️ **Edit Tasks** | Update any task via a modal dialog |
| 🗑️ **Delete Tasks** | Remove tasks with a confirmation prompt |
| 🔄 **Toggle Status** | Click the status badge to toggle completion via AJAX |
| 📱 **Responsive Design** | Fully responsive — works on desktop, tablet, and mobile |
| 🌙 **Dark Mode UI** | Premium glassmorphism design with smooth animations |

---

## 🏗️ Architecture

```
Task Management App
├── Admin Login ──────────► Session-based authentication
│
└── Dashboard
    ├── Stats Cards ──────► Total | Completed | Pending
    │
    ├── Add Task Form
    │   ├── Task ID ──────► Auto-increment Primary Key
    │   ├── Employee Name ► Text input
    │   ├── Task Title ───► Dropdown (Task 1, Task 2, Task 3)
    │   ├── Completed ────► Dropdown (True / False)
    │   └── Submit ───────► Saves to SQLite database
    │
    └── Task Table ───────► View, Edit, Delete, Toggle status
```

---

## 📁 Project Structure

```
MP-online task management/
│
├── app.py                    # Flask application (routes, models, auth)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── instance/
│   └── tasks.db              # SQLite database (auto-created on first run)
│
├── templates/
│   ├── base.html             # Shared layout with flash messages
│   ├── login.html            # Login page with animated background
│   └── dashboard.html        # Dashboard with form, table, and edit modal
│
└── static/
    ├── css/
    │   └── style.css         # Complete design system (dark mode)
    └── js/
        └── app.js            # Client-side interactivity (AJAX, modals)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system

### Installation

1. **Clone or download** the project:
   ```bash
   cd "MP-online task management"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

### Default Credentials

| Field    | Value   |
|----------|---------|
| Username | `admin` |
| Password | `admin` |

> ⚠️ **Note:** Change the default password in production by updating the `init_db()` function in `app.py`.

---

## 🛠️ Tech Stack

| Layer      | Technology |
|------------|------------|
| **Backend**   | Flask 3.1, Flask-Login, Flask-SQLAlchemy |
| **Database**  | SQLite (via SQLAlchemy ORM) |
| **Frontend**  | HTML5, CSS3, Vanilla JavaScript |
| **Auth**      | Werkzeug password hashing + Flask-Login sessions |
| **Typography**| Google Fonts (Inter) |

---

## 📖 API Routes

| Method | Route | Description | Auth Required |
|--------|-------|-------------|:---:|
| `GET`  | `/` | Redirect to login or dashboard | ❌ |
| `GET/POST` | `/login` | Admin login page | ❌ |
| `GET`  | `/logout` | Logout and redirect | ✅ |
| `GET`  | `/dashboard` | Main dashboard view | ✅ |
| `POST` | `/tasks/add` | Create a new task | ✅ |
| `POST` | `/tasks/edit/<id>` | Update an existing task | ✅ |
| `POST` | `/tasks/delete/<id>` | Delete a task | ✅ |
| `POST` | `/tasks/toggle/<id>` | Toggle task completion (AJAX) | ✅ |

---

## 📝 Database Schema

### Admin Table

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | Primary Key, Auto-increment |
| `username` | String(80) | Unique, Not Null |
| `password_hash` | String(256) | Not Null |

### Task Table

| Column | Type | Constraints |
|--------|------|-------------|
| `task_id` | Integer | Primary Key, Auto-increment |
| `employee_name` | String(120) | Not Null |
| `task_title` | String(200) | Not Null |
| `completed` | Boolean | Default: False |
| `created_at` | DateTime | Default: UTC now |
| `updated_at` | DateTime | Auto-updates on change |

---

## 📜 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
#
