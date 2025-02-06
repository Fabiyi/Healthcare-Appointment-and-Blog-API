# Healthcare Appointment and Blog API

## Overview
This API manages healthcare appointments and blogs. Users can register as patients or doctors. 
- Patients: Book appointments.
- Doctors: Accept/decline appointments and write health-related blogs.

---

## Features
### User Authentication
- Register/Login with role-based access control.

### Doctor Management
- Create/update doctor profiles.
- View/search for doctors.

### Appointment Management
- Book appointments (patients).
- Manage appointments (doctors).

### Blog Management
- Write/update/delete blogs (doctors).
- View blogs (all users).

---

## API Endpoints
### Authentication
- **POST /auth/register/**: Register user.
- **POST /auth/login/**: Login user.

### Doctor Management
- **POST /users/doctors/manage/**: Create/Update doctor profile.
- **GET /users/doctors/**: List all doctors.
- **GET /users/doctors/search/**: Search for doctors.

### Appointment Management
- **POST /appointments/**: Book an appointment (patients only).
- **GET /appointments/list/**: View appointments.
- **PATCH /appointments/<id>/**: Update appointment status (doctors only).

### Blog Management
- **POST /blogs/create/**: Create a blog (doctors only).
- **GET /blogs/**: View all blogs.
- **GET /blogs/<id>/**: View a blog.
- **PATCH /blogs/<id>/update/**: Update a blog (authors only).
- **DELETE /blogs/<id>/delete/**: Delete a blog (authors only).

---

## Local Setup
1. Clone the repository:
   ```bash
   git clone <repo_url>

2. Install dependencies:

pip install -r requirements.txt


3. Run migrations:

python manage.py migrate


4. Start the server:

python manage.py runserver



---
