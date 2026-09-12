USE userdb;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_country (country)
);

CREATE TABLE IF NOT EXISTS user_metadata (
    metadata_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    last_login TIMESTAMP NULL,
    login_count INT DEFAULT 0,
    subscription_tier VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);