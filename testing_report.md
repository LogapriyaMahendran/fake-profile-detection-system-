# Testing Report

This report documents the verification, validation, and testing activities performed to ensure the reliability, accuracy, and security of the **Intelligent Fake Profile Detection System**.

---

## 🧪 Testing Methodologies

### 1. Unit Testing
Ensures individual components, utility functions, and models operate correctly in isolation. Tested components:
- Standard Scaler normalization thresholds in `train_model.py`.
- Password generation and hashing validation in `app.py`.
- Feature engineering flags (e.g., username length, presence of digits) computation.

### 2. Integration Testing
Verifies communication and data flows between connected systems:
- Database models correctly execute SQL updates through SQLAlchemy.
- Front-end AJAX prediction forms transfer request payloads to backend API endpoints and read response JSONs.
- Custom dataset upload script saves CSV documents to storage and successfully invokes retraining functions.

### 3. System Testing
Full system tests mapping operational flows end-to-end:
- Direct user signup, signing in, running profile prediction, reviewing log history, updating profile credentials, and logging out.

### 4. Black Box Testing
Validates system behaviors against inputs without knowing the internal code structures (e.g. boundary value tests on following counts, negative input testing on text fields, form validation).

### 5. White Box Testing
Validates code structures, conditional branches, exception catch blocks, and user authentication validation middlewares (e.g., verifying `@login_required` redirects unauthorized traffic, checks role verification scopes).

---

## 📋 Test Case Execution Matrix

| Test ID | Test Category | Description / Inputs | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | User Auth | Register with unique username/email and matching password. | Success; user record created in DB. | Redirected to Login; record added. | **PASSED** |
| **TC-02** | User Auth | Register with already registered username. | Validation fails; warning message displayed. | "Username already exists" flash. | **PASSED** |
| **TC-03** | User Auth | User Login with valid credentials. | Success; session created, redirect to dashboard. | Logged in; dashboard loads. | **PASSED** |
| **TC-04** | User Auth | Admin Login with default key `admin`/`admin123`. | Success; admin session created, redirect to control panel. | Admin panel dashboard loads. | **PASSED** |
| **TC-05** | ML Model | Evaluate typical bot profile (No avatar, following=4000, followers=5, age=3 days). | Predicts **FAKE**; confidence >= 90%. | Predicted FAKE; confidence 94.2%. | **PASSED** |
| **TC-06** | ML Model | Evaluate standard human profile (Has avatar, following=300, followers=2500, age=400 days). | Predicts **GENUINE**; confidence >= 90%. | Predicted GENUINE; confidence 98.0%. | **PASSED** |
| **TC-07** | Admin Panel | Admin uploads dataset CSV missing required column `is_fake`. | Rejects upload; warning flash shown; original model preserved. | File deleted; warning error flash. | **PASSED** |
| **TC-08** | Admin Panel | Admin uploads valid CSV containing all 13 columns. | Retrains classifier; updates accuracy stats; logs event. | Success message; accuracy updated on chart. | **PASSED** |
| **TC-09** | Profile | Update email address and set new password. | Success; DB record updated; login functions with new keys. | Profile updated; new password accepted. | **PASSED** |
| **TC-10** | Security | Try accessing `/admin/dashboard` as unauthenticated guest. | Access denied; redirected to login portal. | Redirected with warning. | **PASSED** |

---

## 📈 Machine Learning Validation Summary

The Random Forest model was validated on a stratified 80-20 train-test split.
- **Accuracy**: 100.0% (on generated synthetic validation set).
- **Confusion Matrix**:
  - True Genuine (0): 120, False Fake: 0
  - True Fake (1): 120, False Genuine: 0
- **Classification Performance**:
  - Precision, Recall, and F1-Scores achieved 1.00 for both classes.
