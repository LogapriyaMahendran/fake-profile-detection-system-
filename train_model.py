import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

def generate_synthetic_dataset(num_samples=1200):
    """Generates a realistic synthetic dataset for fake/genuine social media profiles."""
    np.random.seed(42)
    
    # 50% fake, 50% genuine
    half_samples = num_samples // 2
    
    # --- Fake Profiles Generation ---
    fake_data = {
        'username_length': np.random.randint(5, 25, half_samples),
        'username_has_digits': np.random.choice([0, 1], half_samples, p=[0.3, 0.7]),
        'followers': np.random.randint(0, 150, half_samples),
        'following': np.random.randint(100, 4500, half_samples),
        'posts': np.random.randint(0, 12, half_samples),
        'bio_length': np.random.randint(0, 15, half_samples),
        'has_profile_pic': np.random.choice([0, 1], half_samples, p=[0.7, 0.3]),
        'is_verified': np.zeros(half_samples, dtype=int),
        'has_external_url': np.random.choice([0, 1], half_samples, p=[0.6, 0.4]),
        'is_private': np.random.choice([0, 1], half_samples, p=[0.7, 0.3]),
        'account_age_days': np.random.randint(1, 90, half_samples),
        'engagement_rate': np.random.uniform(0.0, 0.5, half_samples),
        'is_fake': np.ones(half_samples, dtype=int)
    }
    
    # --- Genuine Profiles Generation ---
    genuine_data = {
        'username_length': np.random.randint(6, 16, half_samples),
        'username_has_digits': np.random.choice([0, 1], half_samples, p=[0.8, 0.2]),
        'followers': np.random.randint(150, 65000, half_samples),
        'following': np.random.randint(50, 1200, half_samples),
        'posts': np.random.randint(15, 650, half_samples),
        'bio_length': np.random.randint(15, 150, half_samples),
        'has_profile_pic': np.random.choice([0, 1], half_samples, p=[0.02, 0.98]),
        'is_verified': np.random.choice([0, 1], half_samples, p=[0.95, 0.05]),
        'has_external_url': np.random.choice([0, 1], half_samples, p=[0.75, 0.25]),
        'is_private': np.random.choice([0, 1], half_samples, p=[0.45, 0.55]),
        'account_age_days': np.random.randint(100, 3650, half_samples),
        'engagement_rate': np.random.uniform(1.2, 12.5, half_samples),
        'is_fake': np.zeros(half_samples, dtype=int)
    }
    
    df_fake = pd.DataFrame(fake_data)
    df_genuine = pd.DataFrame(genuine_data)
    
    df = pd.concat([df_fake, df_genuine], ignore_index=True)
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df

def train_and_save_model(dataset_path=None, model_dir='models'):
    print("Starting Machine Learning Model Training Pipeline...")
    
    # 1. Load or Generate Dataset
    if dataset_path and os.path.exists(dataset_path):
        print(f"Loading user dataset from: {dataset_path}")
        df = pd.read_csv(dataset_path)
    else:
        print("Generating synthetic profile dataset...")
        df = generate_synthetic_dataset()
        df.to_csv('social_media_profiles.csv', index=False)
        print("Initial dataset saved to 'social_media_profiles.csv'")
    
    # 2. Features and Target split
    feature_cols = [
        'username_length', 'username_has_digits', 'followers', 'following', 
        'posts', 'bio_length', 'has_profile_pic', 'is_verified', 
        'has_external_url', 'is_private', 'account_age_days', 'engagement_rate'
    ]
    
    X = df[feature_cols]
    y = df['is_fake']
    
    # 3. Handling Missing Values (Just in case)
    X = X.fillna(X.median())
    
    # 4. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 5. Feature Scaling (Numeric features only to prevent scaling flags)
    scaler = StandardScaler()
    scaler.fit(X_train)
    
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 6. Train Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    # 7. Evaluate Model
    y_pred = rf_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist() # Convert to list for JSON compatibility
    class_report = classification_report(y_test, y_pred, output_dict=True)
    
    # Feature Importances
    importances = rf_model.feature_importances_
    feature_importances = {feature_cols[i]: float(importances[i]) for i in range(len(feature_cols))}
    feature_importances = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))
    
    print(f"Model Training Completed. Accuracy: {accuracy:.4f}")
    
    # 8. Save binaries
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, 'fake_profile_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    metadata_path = os.path.join(model_dir, 'model_metadata.json')
    
    joblib.dump(rf_model, model_path)
    joblib.dump(scaler, scaler_path)
    
    metadata = {
        'accuracy': float(accuracy),
        'confusion_matrix': conf_matrix,
        'classification_report': class_report,
        'feature_importances': feature_importances,
        'dataset_size': len(df),
        'fake_count': int(df['is_fake'].sum()),
        'genuine_count': int(len(df) - df['is_fake'].sum())
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Model saved to: {model_path}")
    print(f"Scaler saved to: {scaler_path}")
    print(f"Metadata saved to: {metadata_path}")
    
    return metadata

if __name__ == '__main__':
    train_and_save_model()
