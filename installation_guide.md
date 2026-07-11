# Installation Guide

Follow these instructions to install, configure, and execute the **Intelligent Fake Social Media Profile Detection System** locally.

---

## 📋 Prerequisites

Before starting, ensure your system meets the following specifications:
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Version 3.8 to 3.11 installed
- **Database**: MySQL Server 8.0+ (Optional: the system has auto-fallback to SQLite for zero-config testing)

---

## 🛠️ Step-by-Step Installation

### Step 1: Extract Project Code
Extract the codebase into your target workspace directory:
```bash
c:\Users\M.Logapriya\OneDrive\Documents\Desktop\fakeprofile detection 1
```

### Step 2: Establish Virtual Environment (Recommended)
Navigate to the root folder using terminal and create an isolated Python virtual environment:
```powershell
python -m venv venv
```
Activate the environment:
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Core Dependencies
Install all required libraries and database drivers from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Backend

The system supports two database backends: SQLite (zero-config, immediate startup) and MySQL (production standard).

#### Option A: SQLite (Quick Development Setup)
By default, the application is pre-configured to run with SQLite. No configuration is required.
The application will automatically create `fake_profile.db` inside your root folder and seed default admin and user accounts on startup.

#### Option B: MySQL Configuration (Production Standard)
To hook up the system with a local MySQL server:
1. Log in to your MySQL command line client or workbench and run the schema file:
   ```sql
   SOURCE database.sql;
   ```
   This creates the database `fake_profile_db` and seeds sample tables, logs, and accounts.
2. Open [config.py](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/config.py) and change the database configuration details:
   ```python
   DB_USER = 'your_mysql_username'
   DB_PASSWORD = 'your_mysql_password'
   DB_HOST = 'localhost'
   DB_PORT = '3306'
   DB_NAME = 'fake_profile_db'
   USE_SQLITE = False  # Set to False to disable SQLite and connect to MySQL
   ```

### Step 5: Bootstrapping Machine Learning Model
Generate the synthetic profiles dataset, fit data scalers, and train the Random Forest model:
```bash
python train_model.py
```
This script will produce three core files inside a newly created `models/` directory:
- `fake_profile_model.pkl` (The trained Random Forest model binary)
- `scaler.pkl` (Standard Scaler parameters for standardizing input features)
- `model_metadata.json` (System evaluation performance parameters for display on dashboards)

### Step 6: Start Flask Server
Run the Flask server:
```bash
python app.py
```

Upon successful startup, the command prompt will output:
```
 * Running on http://127.0.0.1:8080
```
Open your browser and navigate to `http://127.0.0.1:8080/`.

---

## 🔐 Default Admin and User Test Credentials

You can use the following default profiles seeded inside the database to explore both portals:

* **Regular User Login**:
  - **Username**: `testuser`
  - **Password**: `user123`
* **Admin Portal Login**:
  - **Username**: `admin`
  - **Password**: `admin123`
