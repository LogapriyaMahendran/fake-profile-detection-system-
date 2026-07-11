import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Import configuration
from config import Config
# Import training pipeline functions
from train_model import train_and_save_model

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database and Login Manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

@app.context_processor
def inject_now():
    return {'datetime': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)

# ==========================================
# DATABASE MODELS (SQLAlchemy)
# ==========================================

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('PredictionHistory', backref='user_rel', lazy=True)

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UploadedDataset(db.Model):
    __tablename__ = 'uploaded_dataset'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete='SET NULL'), nullable=True)
    file_name = db.Column(db.String(255), nullable=False)
    row_count = db.Column(db.Integer, nullable=False)
    model_accuracy = db.Column(db.Float, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    username = db.Column(db.String(100), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    following = db.Column(db.Integer, nullable=False)
    posts = db.Column(db.Integer, nullable=False)
    bio_length = db.Column(db.Integer, nullable=False)
    has_profile_pic = db.Column(db.Boolean, nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False)
    has_external_url = db.Column(db.Boolean, nullable=False)
    is_private = db.Column(db.Boolean, nullable=False)
    account_age_days = db.Column(db.Integer, nullable=False)
    engagement_rate = db.Column(db.Float, nullable=False)
    prediction_result = db.Column(db.String(20), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoginLog(db.Model):
    __tablename__ = 'login_logs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False) # 'User' or 'Admin'
    ip_address = db.Column(db.String(45), nullable=False)
    status = db.Column(db.String(20), nullable=False)     # 'Success' or 'Failed'
    login_time = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    """Loads current logged-in user based on dual-role stored in flask session."""
    role = session.get('role')
    if role == 'admin':
        return Admin.query.get(int(user_id))
    else:
        return User.query.get(int(user_id))

# Helper to automatically seed default data in SQLite/MySQL if empty
def seed_default_accounts():
    if Admin.query.first() is None:
        # Default Admin (Password: admin123)
        admin = Admin(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("Default Admin seeded.")
        
    if User.query.first() is None:
        # Default User (Password: user123)
        user = User(
            username='testuser',
            email='user@example.com',
            password_hash=generate_password_hash('user123')
        )
        db.session.add(user)
        db.session.commit()
        print("Default User seeded.")

# ==========================================
# MACHINE LEARNING HELPER FUNCTIONS
# ==========================================

def get_ml_model():
    """Loads the model & scaler; trains them on synthetic data if missing."""
    model_path = os.path.join(app.config['MODEL_FOLDER'], 'fake_profile_model.pkl')
    scaler_path = os.path.join(app.config['MODEL_FOLDER'], 'scaler.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        print("Model or scaler not found. Running training script first...")
        train_and_save_model()
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def run_model_inference(features):
    """
    Runs prediction and returns probability, result and prediction explanation.
    features format: [username_length, username_has_digits, followers, following, posts,
                      bio_length, has_profile_pic, is_verified, has_external_url, is_private,
                      account_age_days, engagement_rate]
    """
    model, scaler = get_ml_model()
    
    # Feature columns for reference
    feature_cols = [
        'username_length', 'username_has_digits', 'followers', 'following', 
        'posts', 'bio_length', 'has_profile_pic', 'is_verified', 
        'has_external_url', 'is_private', 'account_age_days', 'engagement_rate'
    ]
    
    df_features = pd.DataFrame([features], columns=feature_cols)
    
    # Preprocess
    scaled_features = scaler.transform(df_features)
    
    # Run prediction
    pred = model.predict(scaled_features)[0]
    probs = model.predict_proba(scaled_features)[0]
    
    is_fake = bool(pred == 1)
    confidence = float(probs[1] if is_fake else probs[0])
    
    # Formulate Reasoning based on feature rules
    reasons = []
    
    followers = features[2]
    following = features[3]
    posts = features[4]
    has_profile_pic = features[6]
    is_verified = features[7]
    account_age = features[10]
    engagement_rate = features[11]
    
    ratio = following / max(followers, 1)
    
    if is_fake:
        if not has_profile_pic:
            reasons.append("No profile picture uploaded.")
        if ratio > 15:
            reasons.append(f"Suspiciously high following to followers ratio ({ratio:.1f}x).")
        if posts <= 3:
            reasons.append(f"Very few posts published ({posts}).")
        if account_age <= 30:
            reasons.append(f"Account is brand new ({account_age} days old).")
        if engagement_rate < 0.2:
            reasons.append(f"Very low or non-existent engagement rate ({engagement_rate}%).")
        if not reasons:
            reasons.append("Algorithmic classification matches bot patterns.")
    else:
        if is_verified:
            reasons.append("Account is verified by the platform.")
        if followers > 2000:
            reasons.append(f"Solid follower base ({followers} users).")
        if ratio < 3:
            reasons.append("Healthy follower-to-following ratio.")
        if account_age > 180:
            reasons.append(f"Mature account age ({account_age} days old).")
        if engagement_rate >= 1.0:
            reasons.append(f"Consistent engagement rate ({engagement_rate}%).")
        if not reasons:
            reasons.append("Profile details indicate standard human interaction patterns.")
            
    reason_str = " ".join(reasons)
    
    return {
        'prediction': 'Fake' if is_fake else 'Genuine',
        'confidence': confidence,
        'reason': reason_str
    }

# ==========================================
# CONTROLLERS / ROUTING
# ==========================================

# 1. Home Page
@app.route('/')
def index():
    return render_template('index.html')

# 2. Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('register'))
            
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))
            
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for('register'))
            
        # Create User
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
        
    return render_template('register.html')

# 3. User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email').strip().lower()
        password = request.form.get('password')
        ip_addr = request.remote_addr or '127.0.0.1'
        
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['role'] = 'user'
            login_user(user)
            
            # Log successful login
            log = LoginLog(username=user.username, user_type='User', ip_address=ip_addr, status='Success')
            db.session.add(log)
            db.session.commit()
            
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('dashboard'))
        else:
            # Log failed login
            username_log = username_or_email if username_or_email else 'Unknown'
            log = LoginLog(username=username_log, user_type='User', ip_address=ip_addr, status='Failed')
            db.session.add(log)
            db.session.commit()
            
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))
            
    return render_template('login.html')

# 4. Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email').strip().lower()
        password = request.form.get('password')
        ip_addr = request.remote_addr or '127.0.0.1'
        
        admin = Admin.query.filter((Admin.username == username_or_email) | (Admin.email == username_or_email)).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            session['role'] = 'admin'
            login_user(admin)
            
            # Log successful login
            log = LoginLog(username=admin.username, user_type='Admin', ip_address=ip_addr, status='Success')
            db.session.add(log)
            db.session.commit()
            
            flash("Admin login successful. Welcome to Admin Control Panel.", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            username_log = username_or_email if username_or_email else 'Unknown'
            log = LoginLog(username=username_log, user_type='Admin', ip_address=ip_addr, status='Failed')
            db.session.add(log)
            db.session.commit()
            
            flash("Invalid admin credentials.", "danger")
            return redirect(url_for('admin_login'))
            
    return render_template('admin_login.html')

# 5. Logout
@app.route('/logout')
def logout():
    logout_user()
    session.pop('role', None)
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('login'))

# 6. User Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
        
    # Get user predictions
    recent_predictions = PredictionHistory.query.filter_by(user_id=current_user.id).order_by(PredictionHistory.id.desc()).limit(10).all()
    
    # Calculate simple stats
    total_preds = PredictionHistory.query.filter_by(user_id=current_user.id).count()
    fake_count = PredictionHistory.query.filter_by(user_id=current_user.id, prediction_result='Fake').count()
    genuine_count = PredictionHistory.query.filter_by(user_id=current_user.id, prediction_result='Genuine').count()
    
    return render_template(
        'user_dashboard.html',
        recent_predictions=recent_predictions,
        total_preds=total_preds,
        fake_count=fake_count,
        genuine_count=genuine_count
    )

# 7. Predict API
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if session.get('role') == 'admin':
        return jsonify({'error': 'Admins are not authorized to save prediction history.'}), 403
        
    try:
        username = request.form.get('username', '').strip()
        followers = int(request.form.get('followers', 0))
        following = int(request.form.get('following', 0))
        posts = int(request.form.get('posts', 0))
        bio_length = int(request.form.get('bio_length', 0))
        has_profile_pic = int(request.form.get('has_profile_pic', 0))
        is_verified = int(request.form.get('is_verified', 0))
        has_external_url = int(request.form.get('has_external_url', 0))
        is_private = int(request.form.get('is_private', 0))
        account_age_days = int(request.form.get('account_age_days', 0))
        engagement_rate = float(request.form.get('engagement_rate', 0.0))
        
        # Preprocessing flag inputs
        username_has_digits = 1 if any(char.isdigit() for char in username) else 0
        username_length = len(username)
        
        # Build features array
        features = [
            username_length, username_has_digits, followers, following, posts,
            bio_length, has_profile_pic, is_verified, has_external_url, is_private,
            account_age_days, engagement_rate
        ]
        
        # Inference
        result = run_model_inference(features)
        
        # Store Result in database
        prediction_record = PredictionHistory(
            user_id=current_user.id,
            username=username,
            followers=followers,
            following=following,
            posts=posts,
            bio_length=bio_length,
            has_profile_pic=bool(has_profile_pic),
            is_verified=bool(is_verified),
            has_external_url=bool(has_external_url),
            is_private=bool(is_private),
            account_age_days=account_age_days,
            engagement_rate=engagement_rate,
            prediction_result=result['prediction'],
            confidence_score=result['confidence'],
            reason=result['reason']
        )
        
        db.session.add(prediction_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'prediction': result['prediction'],
            'confidence': f"{result['confidence'] * 100:.2f}%",
            'probability': result['confidence'],
            'reason': result['reason']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# 8. User Profile Settings
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    role = session.get('role')
    
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if role == 'admin':
            user_obj = Admin.query.get(current_user.id)
        else:
            user_obj = User.query.get(current_user.id)
            
        # Email update validation
        if email != user_obj.email:
            if role == 'admin' and Admin.query.filter_by(email=email).first():
                flash("Email already in use.", "danger")
                return redirect(url_for('profile'))
            elif role == 'user' and User.query.filter_by(email=email).first():
                flash("Email already in use.", "danger")
                return redirect(url_for('profile'))
            user_obj.email = email
            
        # Password update validation
        if new_password:
            if new_password != confirm_password:
                flash("Passwords do not match.", "danger")
                return redirect(url_for('profile'))
            user_obj.password_hash = generate_password_hash(new_password)
            
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('profile'))
        
    return render_template('profile.html', role=role)

# 9. Admin Dashboard
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('dashboard'))
        
    # Model Metadata
    metadata_path = os.path.join(app.config['MODEL_FOLDER'], 'model_metadata.json')
    accuracy = 0.0
    features_importance = {}
    dataset_size = 0
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            meta = json.load(f)
            accuracy = meta.get('accuracy', 0.0)
            features_importance = meta.get('feature_importances', {})
            dataset_size = meta.get('dataset_size', 0)
            
    # System statistics
    total_users = User.query.count()
    total_predictions = PredictionHistory.query.count()
    fake_count = PredictionHistory.query.filter_by(prediction_result='Fake').count()
    genuine_count = PredictionHistory.query.filter_by(prediction_result='Genuine').count()
    
    # Recent Activities
    recent_predictions = PredictionHistory.query.order_by(PredictionHistory.id.desc()).limit(5).all()
    recent_logins = LoginLog.query.order_by(LoginLog.id.desc()).limit(5).all()
    recent_datasets = UploadedDataset.query.order_by(UploadedDataset.id.desc()).limit(5).all()
    
    return render_template(
        'admin_dashboard.html',
        accuracy=f"{accuracy * 100:.2f}%",
        total_users=total_users,
        total_predictions=total_predictions,
        fake_count=fake_count,
        genuine_count=genuine_count,
        dataset_size=dataset_size,
        features_importance=features_importance,
        recent_predictions=recent_predictions,
        recent_logins=recent_logins,
        recent_datasets=recent_datasets
    )

# 10. Admin Dataset Upload & Retrain
@app.route('/admin/upload_dataset', methods=['POST'])
@login_required
def admin_upload_dataset():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access.'}), 403
        
    if 'dataset_file' not in request.files:
        flash("No file part uploaded.", "danger")
        return redirect(url_for('admin_dashboard'))
        
    file = request.files['dataset_file']
    
    if file.filename == '':
        flash("No file selected.", "danger")
        return redirect(url_for('admin_dashboard'))
        
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        try:
            # Basic validation
            df = pd.read_csv(save_path)
            required_cols = [
                'username_length', 'username_has_digits', 'followers', 'following', 
                'posts', 'bio_length', 'has_profile_pic', 'is_verified', 
                'has_external_url', 'is_private', 'account_age_days', 'engagement_rate',
                'is_fake'
            ]
            
            # Check for column match
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                flash(f"Invalid dataset structure. Missing columns: {', '.join(missing_cols)}", "danger")
                os.remove(save_path)
                return redirect(url_for('admin_dashboard'))
                
            # Retrain model using the new uploaded dataset
            metadata = train_and_save_model(dataset_path=save_path)
            
            # Save upload log in DB
            new_upload = UploadedDataset(
                admin_id=current_user.id,
                file_name=filename,
                row_count=len(df),
                model_accuracy=metadata['accuracy']
            )
            db.session.add(new_upload)
            db.session.commit()
            
            flash(f"Dataset uploaded successfully! Model retrained with {len(df)} rows. Accuracy: {metadata['accuracy']*100:.2f}%", "success")
        except Exception as e:
            flash(f"Error during preprocessing: {str(e)}", "danger")
            if os.path.exists(save_path):
                os.remove(save_path)
        
        return redirect(url_for('admin_dashboard'))
    else:
        flash("Only CSV files are supported.", "danger")
        return redirect(url_for('admin_dashboard'))

# 11. API for Admin Dashboard Charts JSON Data
@app.route('/api/admin/analytics')
@login_required
def admin_analytics_api():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized.'}), 403
        
    # Pie chart data
    fake_count = PredictionHistory.query.filter_by(prediction_result='Fake').count()
    genuine_count = PredictionHistory.query.filter_by(prediction_result='Genuine').count()
    
    # Monthly Analytics Data (Predictions over past 6 months)
    today = datetime.utcnow()
    monthly_labels = []
    monthly_fake = []
    monthly_genuine = []
    
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=i*30)
        month_name = month_date.strftime('%B %Y')
        monthly_labels.append(month_name)
        
        # Calculate counts for that month
        start_date = datetime(month_date.year, month_date.month, 1)
        if month_date.month == 12:
            end_date = datetime(month_date.year + 1, 1, 1)
        else:
            end_date = datetime(month_date.year, month_date.month + 1, 1)
            
        f_count = PredictionHistory.query.filter(
            PredictionHistory.prediction_result == 'Fake',
            PredictionHistory.created_at >= start_date,
            PredictionHistory.created_at < end_date
        ).count()
        
        g_count = PredictionHistory.query.filter(
            PredictionHistory.prediction_result == 'Genuine',
            PredictionHistory.created_at >= start_date,
            PredictionHistory.created_at < end_date
        ).count()
        
        monthly_fake.append(f_count)
        monthly_genuine.append(g_count)
        
    # Feature importances from metadata
    metadata_path = os.path.join(app.config['MODEL_FOLDER'], 'model_metadata.json')
    features = []
    importances = []
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            meta = json.load(f)
            feat_imp = meta.get('feature_importances', {})
            features = list(feat_imp.keys())
            importances = list(feat_imp.values())
            
    return jsonify({
        'pie_data': {
            'labels': ['Fake Profiles', 'Genuine Profiles'],
            'data': [fake_count, genuine_count]
        },
        'line_data': {
            'labels': monthly_labels,
            'fake': monthly_fake,
            'genuine': monthly_genuine
        },
        'bar_data': {
            'features': features,
            'importances': importances
        }
    })

# 12. Reports Page (User & Admin)
@app.route('/reports')
@login_required
def reports():
    role = session.get('role')
    
    if role == 'admin':
        predictions = PredictionHistory.query.order_by(PredictionHistory.id.desc()).all()
        logins = LoginLog.query.order_by(LoginLog.id.desc()).all()
    else:
        predictions = PredictionHistory.query.filter_by(user_id=current_user.id).order_by(PredictionHistory.id.desc()).all()
        logins = LoginLog.query.filter_by(username=current_user.username).order_by(LoginLog.id.desc()).all()
        
    return render_template('reports.html', role=role, predictions=predictions, logins=logins)

# 13. Export Prediction History (JSON/CSV)
@app.route('/reports/export/<format_type>')
@login_required
def export_report(format_type):
    role = session.get('role')
    
    if role == 'admin':
        records = PredictionHistory.query.all()
    else:
        records = PredictionHistory.query.filter_by(user_id=current_user.id).all()
        
    data = []
    for r in records:
        data.append({
            'ID': r.id,
            'Target Username': r.username,
            'Followers': r.followers,
            'Following': r.following,
            'Posts': r.posts,
            'Bio Length': r.bio_length,
            'Has Profile Pic': r.has_profile_pic,
            'Is Verified': r.is_verified,
            'Has External URL': r.has_external_url,
            'Is Private': r.is_private,
            'Account Age Days': r.account_age_days,
            'Engagement Rate': r.engagement_rate,
            'Prediction Result': r.prediction_result,
            'Confidence Score': r.confidence_score,
            'Reason': r.reason,
            'Timestamp': r.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    if format_type == 'json':
        response = jsonify(data)
        response.headers.set('Content-Disposition', 'attachment', filename='prediction_report.json')
        return response
    elif format_type == 'csv':
        df = pd.DataFrame(data)
        csv_data = df.to_csv(index=False)
        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=prediction_report.csv'
        }
    else:
        flash("Invalid export format requested.", "danger")
        return redirect(url_for('reports'))

# ==========================================
# APP INITIALIZATION
# ==========================================

if __name__ == '__main__':
    with app.app_context():
        # Setup tables if needed
        db.create_all()
        seed_default_accounts()
        
    # Start local server
    app.run(debug=True, host='0.0.0.0', port=8080)
