# User Manual

This manual explains how to interact with the different portals and features of the **Intelligent Fake Profile Detection System**.

---

## 🔑 Authentication & Entry

### 1. User Registration
New users can register an account from the Home page.
1. Click **Get Started** or **Register Account** on the homepage.
2. Fill in the unique **Username**, **Email Address**, and choose a strong password.
3. Submit the registration form. You will be redirected to the sign-in screen upon success.

### 2. User Sign In
1. Go to the User Login page.
2. Enter your registered username/email and password.
3. Submit. On successful authentication, you will be redirected to the **User Dashboard**.

### 3. Admin Portal Access
1. Go to the Home page and click **Admin Portal** in the navigation bar.
2. Enter the admin credentials (Default: `admin` / `admin123`).
3. Submit. You will be redirected to the **Admin Control Panel**.

---

## 📊 User Dashboard Operations

Once logged in as a regular user, you have access to three main functions:

### 1. Evaluate Profile Integrity (Prediction Form)
Use this form to assess whether a social media account is Fake or Genuine:
- **Target Username**: Enter the username of the account to analyze.
- **Account Age (Days)**: Specify how many days have passed since the account was created.
- **Followers & Following**: Input the numeric values of followers and following. The system uses these values to calculate follower-following ratios.
- **Number of Posts**: Enter total posts published by this account.
- **Biography Length**: Character count of the account description.
- **Engagement Rate (%)**: Enter average likes/comments ratio per post.
- **Toggles**: Toggle settings for Profile Picture, Verification Badge, External Website Links, and Account Visibility (Private/Public).

Click **Evaluate Profile Integrity**. The system runs the ML model and reveals:
- **Prediction Badge**: Displays `FAKE PROFILE` (Red pulse) or `GENUINE PROFILE` (Green).
- **Confidence score**: Displays the probability calculated by the Random Forest model.
- **Key Justification Notes**: Explains why the model classified the account as such (e.g. followers-following ratio discrepancy, lack of profile picture, account age).

### 2. View and Filter Assessment History
At the bottom of the User Dashboard, you will find your prediction logs:
- **Search bar**: Type a username to dynamically filter prediction rows.
- **Show Select**: Dropdown filter to display *Show All*, *Fake Only*, or *Genuine Only*.

---

## ⚙️ Admin Control Panel Operations

Admins can manage the platform using the following controls:

### 1. Visualizing Analytics Charts
The Admin Dashboard renders three key charts using Chart.js:
- **Inference Distribution (Doughnut Chart)**: Shows the total ratio of fake profiles to genuine profiles detected by the system.
- **Monthly Inferences Analytics (Line Chart)**: Represents the trend of fake vs genuine detections month-over-month.
- **Feature Importance Metrics (Horizontal Bar Chart)**: Displays the relative weight the Random Forest classifier assigns to each feature (e.g., following count, followers count, account age).

### 2. Monitoring Logs
Review lists of:
- **Recent User Inferences**: Audit target usernames evaluated by platform users.
- **Recent Login Logs**: View successful and failed login attempts with associated IP addresses.
- **Dataset Training Logs**: Records of custom datasets uploaded for training.

### 3. Upload & Retrain Model
To update the classifier model with new patterns:
1. Locate the **Retrain Classifier Model** card on the right-hand side of the Admin Dashboard.
2. Select a valid CSV dataset file containing matching column structures.
3. Click **Upload & Retrain**.
4. The system validates the CSV layout, retrains the Random Forest classifier, updates the saved pickle model, and prints the updated accuracy metrics on the dashboard.

---

## 📄 Analytical Reports & Exporting

Users and administrators can access the **Analytics Reports** page:
1. Toggle between **Prediction History Logs** and **Login Audit Logs**.
2. Click **Export CSV** to download a CSV format spreadsheet of the logs.
3. Click **Export JSON** to download a structured JSON layout of the logs.
