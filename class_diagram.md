# Class Diagram

The class diagram maps the OOP entities, database tables classes, config parameters, and machine learning methods.

```mermaid
classDiagram
    class Config {
        +String SECRET_KEY
        +String SQLALCHEMY_DATABASE_URI
        +String UPLOAD_FOLDER
        +String MODEL_FOLDER
    }

    class UserMixin {
        <<Interface>>
        +is_authenticated()
        +is_active()
        +is_anonymous()
        +get_id()
    }

    class User {
        +int id
        +String username
        +String email
        +String password_hash
        +datetime created_at
        +predictions relationship
    }

    class Admin {
        +int id
        +String username
        +String email
        +String password_hash
        +datetime created_at
    }

    class PredictionHistory {
        +int id
        +int user_id
        +String username
        +int followers
        +int following
        +int posts
        +int bio_length
        +boolean has_profile_pic
        +boolean is_verified
        +boolean has_external_url
        +boolean is_private
        +int account_age_days
        +float engagement_rate
        +String prediction_result
        +float confidence_score
        +String reason
        +datetime created_at
    }

    class UploadedDataset {
        +int id
        +int admin_id
        +String file_name
        +int row_count
        +float model_accuracy
        +datetime uploaded_at
    }

    class LoginLog {
        +int id
        +String username
        +String user_type
        +String ip_address
        +String status
        +datetime login_time
    }

    class ModelPipeline {
        +generate_synthetic_dataset(num_samples) DataFrame
        +train_and_save_model(dataset_path, model_dir) dict
    }

    class FlaskController {
        +index() HTML
        +register() HTML/Redirect
        +login() HTML/Redirect
        +admin_login() HTML/Redirect
        +logout() Redirect
        +dashboard() HTML
        +predict() JSON
        +admin_dashboard() HTML
        +admin_upload_dataset() Redirect
        +admin_analytics_api() JSON
        +profile() HTML/Redirect
        +reports() HTML
        +export_report(format_type) fileStream
    }

    UserMixin <|-- User
    UserMixin <|-- Admin
    User "1" --> "many" PredictionHistory : makes
    Admin "1" --> "many" UploadedDataset : uploads
    FlaskController --> Config : reads
    FlaskController --> User : authenticates
    FlaskController --> Admin : authenticates
    FlaskController --> ModelPipeline : triggers
    FlaskController --> PredictionHistory : queries
    FlaskController --> LoginLog : logs
