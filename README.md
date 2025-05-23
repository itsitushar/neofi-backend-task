# 🚀 NeoFi Backend Developer Task

A FastAPI-based backend system that supports user authentication, event management, role-based collaboration, and version history tracking.

---

## 📦 Features

### 🔐 Authentication
- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login and receive JWT access + refresh tokens
- `POST /api/auth/refresh`: Refresh the access token
- `POST /api/auth/logout`: Logout the user

### 📅 Event Management
- `POST /api/events`: Create a new event
- `GET /api/events`: List user-accessible events (with pagination)
- `GET /api/events/{id}`: Get a specific event
- `PUT /api/events/{id}`: Update an event
- `DELETE /api/events/{id}`: Delete an event
- `POST /api/events/batch`: Create multiple events

### 🤝 Collaboration
- `POST /api/events/{id}/share`: Share an event with a user
- `GET /api/events/{id}/permissions`: List current permissions
- `PUT /api/events/{id}/permissions/{userId}`: Update user role
- `DELETE /api/events/{id}/permissions/{userId}`: Revoke access

### 🕓 Version History
- `GET /api/events/{id}/history/{versionId}`: View a specific past version
- `POST /api/events/{id}/rollback/{versionId}`: Rollback to a version

### 📘 Changelog & Diff
- `GET /api/events/{id}/changelog`: View change history
- `GET /api/events/{id}/diff/{version1}/{version2}`: Compare two versions

---

## ⚙️ Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Auth:** JWT via `python-jose`, password hashing with `passlib`
- **Schema Validation:** Pydantic v1

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/neofi-backend.git
cd neofi-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the app
```
fastapi dev main.py
```