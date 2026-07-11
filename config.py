import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey_for_fakeprofile_detection_system_2026')
    
    # Database Configuration
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '') # Default blank for MySQL root
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'fake_profile_db')
    
    # Set to False to connect to MySQL using credentials above. 
    # Set to True for zero-config SQLite local development fallback.
    USE_SQLITE = os.environ.get('USE_SQLITE', 'True').lower() == 'true'
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'fake_profile.db')}"
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for datasets & profile pics
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MODEL_FOLDER = os.path.join(BASE_DIR, 'models')
    
    # Limit max uploaded file size to 16 Megabytes
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
