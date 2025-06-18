# Job Portal Backend API

A comprehensive Django REST Framework based backend for a Job Portal platform that connects recruiters with candidates. Features include role-based authentication, job posting management, and email notifications.

## Core Features

### 1. Role-Based Authentication System

- User roles: Recruiter and Candidate
- JWT-based authentication
- Role-specific permissions and access control
- Secure password hashing
- Email-based password reset

### 2. Email Notifications

- Welcome emails on registration
- Password reset functionality
- Role-specific email templates
- HTML formatted emails
- Secure credential storage in .env

### 3. Job Management

- Complete CRUD operations for job postings
- Role-based access control
- Job status management (Draft, Published, Closed, Archived)
- Comprehensive job details
- Job type categorization
- Salary range specification
- Application tracking

## Technology Stack

- Python 3.12
- Django REST Framework
- JWT Authentication
- SQLite Database
- SMTP Email Integration

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd intern_backend_project
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   Create a `.env` file in the root directory with the following configurations:

   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   ```

   Replace the email credentials with your own.

4. **Database Setup**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Authentication Endpoints

#### 1. User Registration

```http
POST /api/v1/auth/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password",
    "confirm_password": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE",  // or "RECRUITER"
    "username": "user@example.com"
}
```

#### 2. Get JWT Token

```http
POST /api/v1/auth/token/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}
```

#### 3. Password Management

```http
# Request Password Reset
POST /api/v1/auth/password/forgot/
Content-Type: application/json

{
    "email": "user@example.com"
}

# Reset Password
POST /api/v1/auth/password/reset/
Content-Type: application/json

{
    "password": "new_password",
    "confirm_password": "new_password",
    "token": "reset_token",
    "uidb64": "user_id_b64"
}
```

### Job Management Endpoints

#### 1. List Jobs

```http
GET /api/v1/jobs/
Authorization: Bearer <your_token>
```

#### 2. Create Job (Recruiters Only)

```http
POST /api/v1/jobs/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "title": "Senior Python Developer",
    "description": "Job description...",
    "job_type": "FULL_TIME",
    "location": "New York, NY",
    "salary_min": 80000,
    "salary_max": 120000,
    "deadline": "2025-07-18T23:59:59Z",
    "requirements": "Required skills...",
    "responsibilities": "Job responsibilities...",
    "company_name": "Tech Corp",
    "company_description": "About company...",
    "experience_required": 5,
    "skills_required": "Python, Django...",
    "benefits": "Health insurance..."
}
```

#### 3. Get Job Details

```http
GET /api/v1/jobs/{job_uid}/
Authorization: Bearer <your_token>
```

#### 4. Update Job (Recruiters Only)

```http
PATCH /api/v1/jobs/{job_uid}/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "title": "Updated Title",
    ...
}
```

#### 5. Job Status Management (Recruiters Only)

```http
# Publish Job
POST /api/v1/jobs/{job_uid}/publish/
Authorization: Bearer <your_token>

# Close Job
POST /api/v1/jobs/{job_uid}/close/
Authorization: Bearer <your_token>

# Archive Job
POST /api/v1/jobs/{job_uid}/archive/
Authorization: Bearer <your_token>
```

## Models

### User Model

```python
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = CharField(max_length=50, unique=True)
    email = EmailField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    role = CharField(choices=RoleChoices.choices)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
```

### Job Model

```python
class Job(BaseModel):
    title = CharField(max_length=255)
    description = TextField()
    recruiter = ForeignKey(User, related_name='posted_jobs')
    job_type = CharField(choices=JobTypeChoices)
    location = CharField(max_length=255)
    salary_min = DecimalField()
    salary_max = DecimalField()
    deadline = DateTimeField()
    requirements = TextField()
    responsibilities = TextField()
    status = CharField(choices=JobStatusChoices)
    company_name = CharField(max_length=255)
    company_description = TextField()
    experience_required = IntegerField()
    skills_required = TextField()
    benefits = TextField()
    is_featured = BooleanField()
    views_count = IntegerField()
    applications_count = IntegerField()
```

### UserProfile Model

```python
class UserProfile(BaseModel):
    user = OneToOneField(User, related_name="profile")
    photo = ImageField(upload_to="profile_pictures/")
    bio = TextField()
    date_of_birth = DateField(null=True)
    gender = CharField(choices=GenderChoices.choices)
```

## Permissions

The API implements comprehensive role-based access control:

### 1. Public Endpoints (No Authentication Required)

- User registration
- Login (token generation)
- Password reset request
- Password reset confirmation

### 2. Candidate Permissions

- View published jobs
- View job details
- View company information
- Filter and search jobs

### 3. Recruiter Permissions

- Create new job postings
- Edit own job postings
- Delete own job postings
- Manage job status (Draft/Publish/Close/Archive)
- View all own jobs
- View job applications

## Testing

Run the test suite:

```bash
python manage.py test
```

The project includes tests for:

- User registration
- Email functionality
- Role-based authorization
- API endpoints

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
