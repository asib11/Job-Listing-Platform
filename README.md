# Django Backend Project

A Django REST API backend project for an Job Listing platform that connects recruiters with candidates.

## Features

- **Role-Based Authentication System**

  - User roles: Recruiter and Candidate
  - Role-specific permissions and access control
  - JWT-based authentication

- **Email Notifications**
  - Welcome emails on registration
  - Role-specific email content
  - HTML formatted emails

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

#### Register User

- **URL**: `/api/v1/auth/register`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password",
    "confirm_password": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "role": "CANDIDATE", // or "RECRUITER"
    "username": "user@example.com"
  }
  ```
- **Response**: 201 Created
  ```json
  {
    "username": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "role": "CANDIDATE"
  }
  ```

#### Get Token

- **URL**: `/api/v1/auth/token`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "username": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "token": "your.jwt.token"
  }
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

The API implements role-based access control:

- `IsRecruiter`: Allows access only to users with the Recruiter role
- `IsCandidate`: Allows access only to users with the Candidate role
- `IsOwnerOrRecruiter`: Allows access to the owner of an object or any recruiter

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
