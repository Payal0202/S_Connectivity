CREATE DATABASE flask_app_db;

CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'flask_password';

GRANT ALL PRIVILEGES ON flask_app_db.* TO 'flask_user'@'localhost';

FLUSH PRIVILEGES;

USE flask_app_db;

CREATE TABLE CapturedImages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    image LONGBLOB NOT NULL
);

-- SELECT id, timestamp AS captured_at, LENGTH(image) AS image_size FROM CapturedImages;-- 

select * from CapturedImages;

