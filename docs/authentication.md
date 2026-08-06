# Authentication Module Specification

## Feature Branch

```
feature/auth
```

---

# Objective

Implement a secure authentication system where users **cannot register themselves**.

Only the Teacher (Administrator) can create student accounts and assign login credentials.

---

# Authentication Flow

```
Teacher
    │
    │ Creates Student
    ▼
Database
    │
    │ Stores username and hashed password
    ▼
Student
    │
    │ Login
    ▼
Dashboard
```

There is **no public registration page**.

---

# User Types

Initially the system supports two roles.

* Teacher (Admin)
* Student

The architecture should allow additional roles in the future.

Examples:

* Assistant Teacher
* Parent

---

# Login Requirements

Students authenticate using:

* Username
* Password

Email authentication is **not required**.

---

# Registration

Registration is disabled.

The following pages should NOT exist.

* Sign Up
* Create Account
* Register

Only administrators may create users through the Django Admin panel.

---

# User Creation

Teacher creates users from Django Admin.

Required fields:

* First Name
* Last Name
* Username
* Temporary Password
* Active Status

Optional fields:

* Phone Number
* Avatar

---

# Password Handling

Passwords must never be stored as plain text.

Use Django's built-in password hashing system.

Never create a custom password hashing implementation.

---

# Authentication Backend

Use Django Authentication Framework.

Do not implement custom authentication unless a future requirement demands it.

---

# Login Process

1. User opens Login page.
2. User enters username and password.
3. Validate credentials.
4. If valid:

   * Create authenticated session.
   * Redirect to Dashboard.
5. If invalid:

   * Show generic error message.

Do not reveal whether the username or password is incorrect.

---

# Logout Process

1. User clicks Logout.
2. Session is destroyed.
3. Redirect to Login page.

---

# Access Control

Unauthenticated users cannot access protected pages.

Protected pages include:

* Dashboard
* Reading
* Listening
* Assignments
* Notes
* Videos

Unauthorized users must always be redirected to Login.

---

# Session Management

Authenticated users remain logged in using Django Sessions.

Future enhancement:

* Remember Me
* Session timeout
* Multiple device management

---

# Authorization

Teacher permissions:

* Create students
* Update students
* Delete students
* Assign homework
* View analytics

Student permissions:

* Login
* View assignments
* Submit answers
* Create notes
* Highlight text
* View personal progress

Students cannot:

* Access Django Admin
* Create users
* Delete users
* Edit assignments

---

# Security Requirements

* CSRF protection enabled.
* Session authentication enabled.
* HTTPS required in production.
* Secure cookies in production.
* HttpOnly cookies enabled.
* Strong password policy.
* Password hashing handled by Django.
* Never expose sensitive error messages.

---

# Future Improvements

* Password reset by Teacher
* Force password change on first login
* Two-factor authentication
* Login history
* Account lock after repeated failed attempts
* Device management

---

# Acceptance Criteria

Authentication is complete when:

* Teacher can create student accounts.
* Students can log in.
* Students can log out.
* Registration does not exist.
* Passwords are securely hashed.
* Protected pages require authentication.
* Students cannot access admin pages.
* Sessions work correctly.
