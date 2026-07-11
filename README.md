# Intelligent Fake Social Media Profile Detection System

This repository contains the complete production-ready source code and technical documentation for the **Intelligent Fake Social Media Profile Detection System Using Machine Learning**.

The application utilizes a **Random Forest Classifier** trained on account behavior parameters to classify profiles as **Fake** or **Genuine** in real time. It is built using Python Flask, Bootstrap 5, Chart.js, and SQLAlchemy (supporting MySQL/SQLite).

---

## 📂 Project Directory Structure

```
├── app.py                      # Main Flask server entry point (routes, Auth, APIs)
├── config.py                   # Configuration parameters (Database, Upload folders)
├── database.sql                # Production MySQL tables schema and sample records
├── train_model.py              # Script to generate synthetic dataset & train initial Random Forest
├── requirements.txt            # Python environment dependencies list
├── social_media_profiles.csv   # Dataset used for initial training and testing
├── models/
│   ├── fake_profile_model.pkl  # Serialized Random Forest Classifier binary
│   ├── scaler.pkl              # Scaler parameters for numeric input normalization
│   └── model_metadata.json     # Accuracy rates, confusion matrix & feature importances
├── static/
│   ├── css/
│   │   └── style.css           # Premium custom stylesheets (Dark Mode, glassmorphism, animations)
│   └── js/
│       └── main.js             # Form validation, predictions Ajax, and Chart.js rendering
├── templates/
│   ├── base.html               # Base layout shell (Includes sidebar navigation and top bar)
│   ├── index.html              # Landing home page
│   ├── login.html              # User login screen
│   ├── register.html           # User registration screen
│   ├── admin_login.html        # Separate admin portal login
│   ├── user_dashboard.html     # Predict profile inputs form and user prediction log
│   ├── admin_dashboard.html    # Admin management panel (charts, retraining logs, logins log)
│   ├── profile.html            # Settings (Manage profile credentials & passwords)
│   └── reports.html            # System analytical reports & logs exports
└── docs/                       # Project Documentation Folder
    ├── README.md               # Main documentation router
    ├── installation_guide.md   # Step-by-step local workspace setup instructions
    ├── user_manual.md          # Guides for operating the application features
    ├── api_documentation.md    # Restful web services details
    ├── testing_report.md       # Quality assurance results and test cases matrix
    ├── deployment_guide.md      # Deployment guidelines for cloud servers
    ├── project_documentation.md # Detailed college project report document
    └── diagrams/               # Software Engineering Mermaid flow diagrams
```

---

## 📖 Complete Documentation Suite

For comprehensive project guides, refer to the following documentation files:

1. ⚙️ **[Installation Guide](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/docs/installation_guide.md)** - Learn how to set up Python, install dependencies, load databases, and run the server.
2. 📘 **[User Manual](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/docs/user_manual.md)** - High-level operational walk-throughs for users and admins.
3. 🌐 **[API Documentation](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/docs/api_documentation.md)** - Details on routes, requests, responses, and parameters.
4. 🧪 **[Testing Report](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/docs/testing_report.md)** - Review unit, integration, and black/white box verification reports.
5. 🚀 **[Deployment Guide](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/docs/deployment_guide.md)** - How to deploy the application on production-grade systems.
6. 📝 **[Project Documentation](file:///c:/Users/M.Logapriya/OneDrive/Documents/Desktop/fakeprofile%20detection%201/docs/project_documentation.md)** - Academic documentation (Abstract, Introduction, Scope, Methodology, Diagrams, and Conclusion).
