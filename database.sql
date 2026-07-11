-- ==========================================
-- Database Schema for Intelligent Fake Profile Detection System
-- Database Engine: MySQL
-- ==========================================

CREATE DATABASE IF NOT EXISTS `fake_profile_db`;
USE `fake_profile_db`;

-- 1. Table: users
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Table: admin
CREATE TABLE IF NOT EXISTS `admin` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Table: uploaded_dataset
CREATE TABLE IF NOT EXISTS `uploaded_dataset` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_id` INT NULL,
    `file_name` VARCHAR(255) NOT NULL,
    `row_count` INT NOT NULL,
    `model_accuracy` FLOAT NOT NULL,
    `uploaded_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`admin_id`) REFERENCES `admin`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Table: prediction_history
CREATE TABLE IF NOT EXISTS `prediction_history` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `username` VARCHAR(100) NOT NULL,
    `followers` INT NOT NULL,
    `following` INT NOT NULL,
    `posts` INT NOT NULL,
    `bio_length` INT NOT NULL,
    `has_profile_pic` BOOLEAN NOT NULL,
    `is_verified` BOOLEAN NOT NULL,
    `has_external_url` BOOLEAN NOT NULL,
    `is_private` BOOLEAN NOT NULL,
    `account_age_days` INT NOT NULL,
    `engagement_rate` FLOAT NOT NULL,
    `prediction_result` VARCHAR(20) NOT NULL, -- 'Fake' or 'Genuine'
    `confidence_score` FLOAT NOT NULL,        -- e.g. 0.89 (89%)
    `reason` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Table: reports
CREATE TABLE IF NOT EXISTS `reports` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_id` INT NULL,
    `title` VARCHAR(255) NOT NULL,
    `file_path` VARCHAR(255) NOT NULL,
    `generated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`admin_id`) REFERENCES `admin`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Table: login_logs
CREATE TABLE IF NOT EXISTS `login_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL,
    `user_type` VARCHAR(20) NOT NULL,         -- 'User' or 'Admin'
    `ip_address` VARCHAR(45) NOT NULL,
    `status` VARCHAR(20) NOT NULL,            -- 'Success' or 'Failed'
    `login_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==========================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ==========================================
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_admin_username ON admin(username);
CREATE INDEX idx_predictions_user_id ON prediction_history(user_id);
CREATE INDEX idx_predictions_username ON prediction_history(username);
CREATE INDEX idx_login_logs_time ON login_logs(login_time);

-- ==========================================
-- SAMPLE DATA INSERTION (Passwords: admin123 and user123)
-- PBKDF2 Hashed values for Werkzeug integration
-- ==========================================

-- Insert Default Admin (Password: admin123)
INSERT INTO `admin` (`id`, `username`, `email`, `password_hash`) VALUES
(1, 'admin', 'admin@example.com', 'scrypt:32768:8:1$uD64yq4c7Y1v6H6J$4e71239c8ba2a7f5a9b7cf53fbf5b0c79fbe4a8d052a3928a3f8a005080c98ea')
ON DUPLICATE KEY UPDATE id=id;

-- Insert Default Test User (Password: user123)
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`) VALUES
(1, 'testuser', 'user@example.com', 'scrypt:32768:8:1$K5zQWb169p6M7B5S$2f15598687ba1fb5d336fe6704cdfa4dfbe87332a688b560ab9e47cb1cf2984a')
ON DUPLICATE KEY UPDATE id=id;

-- Insert Sample Prediction History
INSERT INTO `prediction_history` (`id`, `user_id`, `username`, `followers`, `following`, `posts`, `bio_length`, `has_profile_pic`, `is_verified`, `has_external_url`, `is_private`, `account_age_days`, `engagement_rate`, `prediction_result`, `confidence_score`, `reason`, `created_at`) VALUES
(1, 1, 'spammer_bot_99', 12, 4500, 1, 0, 0, 0, 1, 0, 5, 0.0, 'Fake', 0.94, 'High ratio of following to followers, zero profile picture, and account is very new with no user engagement.', '2026-07-01 10:15:30'),
(2, 1, 'john_doe_official', 24500, 310, 142, 45, 1, 1, 1, 0, 730, 4.2, 'Genuine', 0.98, 'Strong engagement rate, verified badge, high follower count, and mature account age.', '2026-07-02 11:20:45'),
(3, 1, 'anonymous_user_x', 3, 12, 0, 5, 0, 0, 0, 1, 1, 0.0, 'Fake', 0.88, 'Zero profile picture, zero posts, and very low followers count indicating an inactive bot profile.', '2026-07-03 14:05:00'),
(4, 1, 'creative_artist', 890, 400, 89, 120, 1, 0, 1, 0, 365, 5.5, 'Genuine', 0.96, 'Normal follower-to-following ratio, custom biography description, and consistent user engagement.', '2026-07-04 09:30:00');

-- Insert Sample Dataset Log
INSERT INTO `uploaded_dataset` (`id`, `admin_id`, `file_name`, `row_count`, `model_accuracy`) VALUES
(1, 1, 'social_media_profiles.csv', 1000, 0.965);

-- Insert Sample Logs
INSERT INTO `login_logs` (`username`, `user_type`, `ip_address`, `status`, `login_time`) VALUES
('admin', 'Admin', '127.0.0.1', 'Success', '2026-07-06 16:30:00'),
('testuser', 'User', '127.0.0.1', 'Success', '2026-07-06 16:45:00');
