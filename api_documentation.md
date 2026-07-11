# API Documentation

This document describes the web service endpoints and APIs exposed by the **Intelligent Fake Profile Detection System**.

---

## 🔒 Authentication Scopes

The system utilizes session-based authentication managed by Flask-Login. Routes are divided into three access scopes:
- **Public**: Accessible without logging in.
- **User Protected**: Requires a valid user session.
- **Admin Protected**: Requires a valid admin session.

---

## 🌐 API Endpoint Registry

### 1. Account Authentication Endpoints

#### `POST /register`
Registers a new user account.
- **Scope**: Public
- **Content-Type**: `application/x-www-form-urlencoded`
- **Parameters**:
  - `username` (string, required): A unique lowercase username.
  - `email` (string, required): A unique email address.
  - `password` (string, required): Chosen user password.
  - `confirm_password` (string, required): Must match `password`.
- **Response**: Redirects to `/login` on success, reload `/register` with flash warning on failure.

#### `POST /login`
Authenticates a user and starts a session.
- **Scope**: Public
- **Content-Type**: `application/x-www-form-urlencoded`
- **Parameters**:
  - `username_or_email` (string, required): Username or email address.
  - `password` (string, required): Password.
- **Response**: Redirects to `/dashboard` on success, reload `/login` on failure.

#### `POST /admin/login`
Authenticates an administrator.
- **Scope**: Public
- **Content-Type**: `application/x-www-form-urlencoded`
- **Parameters**:
  - `username_or_email` (string, required): Admin username/email.
  - `password` (string, required): Admin key password.
- **Response**: Redirects to `/admin/dashboard` on success, reload `/admin/login` on failure.

#### `GET /logout`
Terminates active session.
- **Scope**: User / Admin
- **Response**: Redirects to `/login`.

---

### 🧠 Machine Learning Inference Endpoint

#### `POST /predict`
Executes Random Forest classification on profile statistics and returns prediction scores.
- **Scope**: User Protected
- **Content-Type**: `application/x-www-form-urlencoded`
- **Parameters**:
  - `username` (string, required): Target username handle.
  - `followers` (integer, required): Followers count.
  - `following` (integer, required): Following count.
  - `posts` (integer, required): Total post count.
  - `bio_length` (integer, required): Character length of biography.
  - `has_profile_pic` (integer flag: 0 or 1, required): Whether profile pic exists.
  - `is_verified` (integer flag: 0 or 1, required): Verification badge status.
  - `has_external_url` (integer flag: 0 or 1, required): Website link present.
  - `is_private` (integer flag: 0 or 1, required): Account privacy status.
  - `account_age_days` (integer, required): Days since account creation.
  - `engagement_rate` (float, required): Average engagement percentage.
- **Response Format**: `JSON`
- **Sample Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "prediction": "Fake",
    "confidence": "94.20%",
    "probability": 0.942,
    "reason": "No profile picture uploaded. Suspiciously high following to followers ratio (375.0x). Very few posts published (1)."
  }
  ```
- **Sample Error Response (400 Bad Request)**:
  ```json
  {
    "success": false,
    "error": "ValueError: Could not convert string to float: 'abc'"
  }
  ```

---

### 📊 Admin Analytics Endpoint

#### `GET /api/admin/analytics`
Fetches analytics statistics representing user prediction distributions, feature importances, and registration trends.
- **Scope**: Admin Protected
- **Response Format**: `JSON`
- **Sample Response (200 OK)**:
  ```json
  {
    "pie_data": {
      "labels": ["Fake Profiles", "Genuine Profiles"],
      "data": [124, 88]
    },
    "line_data": {
      "labels": ["February 2026", "March 2026", "April 2026", "May 2026", "June 2026", "July 2026"],
      "fake": [10, 15, 20, 25, 34, 20],
      "genuine": [8, 12, 11, 19, 22, 16]
    },
    "bar_data": {
      "features": ["followers", "following", "account_age_days", "has_profile_pic"],
      "importances": [0.352, 0.281, 0.145, 0.082]
    }
  }
  ```

---

### 💾 Export Reports Endpoints

#### `GET /reports/export/<format_type>`
Downloads database predictions history logs.
- **Scope**: User / Admin (Admins export global logs, Users export personal logs only)
- **URL Parameters**:
  - `format_type` (string, required): Options are `csv` or `json`.
- **Response**: File download stream matching target formatting.
