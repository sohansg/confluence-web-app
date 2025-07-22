
# 🌀 Confluence Web App

A full-stack collaborative document sharing and editing platform built with **React.js** (frontend) and **Django REST Framework** (backend). The app supports user authentication, private/public document control, versioning, and real-time collaboration.

---

## 🔧 Tech Stack

### 🚀 Frontend
- React.js
- Axios
- Tailwind CSS (or your CSS framework)
- React Router

### 🛠️ Backend
- Django
- Django REST Framework (DRF)
- MySQL (or PostgreSQL/SQLite depending on your DB)
- JWT Authentication (djangorestframework-simplejwt)

---

## ✨ Key Features

- 🔐 **User Authentication** (Login/Signup using JWT)
- 📝 **Create, Edit, Delete Documents**
- 🔗 **Share Documents Privately/Publicly**
- 👥 **Collaborative Editing with Version Control**
- 📂 **View Documents Shared With You**
- 📜 **Document Timestamping and History Tracking**

---

## 📁 Folder Structure

confluence-web-app/
├── backend/ # Django project
│ └── friggaproject/
│ └── users/
├── frontend/ # React app
│ └── src/
│ └── components/
│ └── pages/
└── README.md

yaml
Copy
Edit

---

## 🚀 Getting Started

### 📦 Backend Setup

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate   # On Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
🌐 Frontend Setup
bash
Copy
Edit
cd frontend
npm install
npm start
🔗 API Endpoints
Method	Endpoint	Description
POST	/api/register/	Register a new user
POST	/api/login/	User login (returns JWT)
GET	/api/documents/	Get all user-created documents
POST	/api/documents/	Create a new document
GET	/api/shared/	View documents shared with user
PUT	/api/documents/:id/	Update document
DELETE	/api/documents/:id/	Delete document
