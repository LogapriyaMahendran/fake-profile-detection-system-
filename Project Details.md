# Intelligent Fake Social Media Profile Detection System

## Project Title

**Intelligent Fake Social Media Profile Detection System**

---

## Problem Statement

Social media platforms are increasingly affected by fake profiles and bot accounts that are used for spam, fraud, identity theft, and spreading misinformation. Detecting such accounts manually is difficult and time-consuming due to the large number of users. Therefore, an intelligent Machine Learning-based system is required to automatically identify and classify fake social media profiles accurately.

---

## Project Objectives

1. To detect fake social media profiles using Machine Learning techniques.
2. To analyze user profile characteristics and activities.
3. To classify profiles as genuine or fake.
4. To improve social media security and user trust.
5. To reduce spam and fraudulent activities on social networking platforms.

---

## Module List

### Module 1: User Input Module

* Collects social media profile details from users.
* Validates the input data.

### Module 2: Data Preprocessing Module

* Cleans the dataset.
* Handles missing values and feature selection.

### Module 3: Machine Learning Module

* Trains and tests the Random Forest model.
* Generates profile predictions.

### Module 4: Fake Profile Detection Module

* Analyzes profile features.
* Classifies profiles as Fake or Genuine.

### Module 5: Database Management Module

* Stores user inputs and prediction results.
* Maintains prediction history.

### Module 6: Result Display Module

* Displays prediction results to users.
* Shows classification output.

---

## Database Table List

### Table 1: user_profiles

| Field Name    | Data Type         |
| ------------- | ----------------- |
| id            | INT (Primary Key) |
| username      | VARCHAR(100)      |
| followers     | INT               |
| following     | INT               |
| posts         | INT               |
| profile_photo | VARCHAR(10)       |
| prediction    | VARCHAR(20)       |
| created_at    | DATETIME          |

### Table 2: prediction_history

| Field Name       | Data Type         |
| ---------------- | ----------------- |
| prediction_id    | INT (Primary Key) |
| user_id          | INT               |
| result           | VARCHAR(20)       |
| confidence_score | FLOAT             |
| prediction_date  | DATETIME          |

---

## Technologies Used

* Frontend: HTML, CSS, Bootstrap
* Backend: Python Flask
* Database: MySQL
* Machine Learning: Random Forest
* Dataset: Bots vs Users Dataset

---

## Expected Outcome

The system analyzes social media profile information and predicts whether the account is Fake or Genuine. This helps reduce spam, fraud, and misinformation while improving trust and security on social media platforms.
