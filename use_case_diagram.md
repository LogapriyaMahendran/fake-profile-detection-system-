# Use Case Diagram

The use case diagram illustrates user interactions, roles, system boundaries, and permission access scopes.

```mermaid
left-to-right-direction
actor User
actor Admin

rectangle SystemBoundaries["Intelligent Fake Profile Detection System"] {
    %% User Cases
    usecase UC_Register["Register Account"]
    usecase UC_Login["Login Portal"]
    usecase UC_Predict["Run Profile Prediction"]
    usecase UC_ViewHistory["View Assessment History"]
    usecase UC_UpdateProfile["Manage Account Profile"]
    usecase UC_Export["Export Predictions Data"]
    
    %% Admin Cases
    usecase UC_AdminLogin["Admin Authenticate"]
    usecase UC_AdminDashboard["Inspect Analytics & Logs"]
    usecase UC_Upload["Upload Datasets"]
    usecase UC_Retrain["Trigger Model Retraining"]
    usecase UC_ExportAll["Export Global Reports"]
    usecase UC_Logout["Sign Out Session"]
}

User --> UC_Register
User --> UC_Login
User --> UC_Predict
User --> UC_ViewHistory
User --> UC_UpdateProfile
User --> UC_Export
User --> UC_Logout

Admin --> UC_AdminLogin
Admin --> UC_AdminDashboard
Admin --> UC_Upload
Admin --> UC_Retrain
Admin --> UC_UpdateProfile
Admin --> UC_ExportAll
Admin --> UC_Logout
```
