-- Create database
CREATE DATABASE IF NOT EXISTS swachh_shala;
USE swachh_shala;

-- Users table (admins & schools)
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  institution_name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  address TEXT,
  password VARCHAR(255),
  role ENUM('admin', 'school') NOT NULL
);

-- Registration requests table (for schools pending approval)
CREATE TABLE registration_requests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  institution_name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  address TEXT,
  password VARCHAR(255),
  status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending'
);

-- Complaints table (image uploads and predictions)
CREATE TABLE complaints (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  image_path VARCHAR(500),
  predicted_class VARCHAR(255),
  probability FLOAT,
  status ENUM('Pending', 'Resolved') DEFAULT 'Pending',
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert default admin user
INSERT INTO users (institution_name, email, address, password, role)
VALUES ('Admin User', 'admin@swachhshala.com', 'Head Office', 'admin123', 'admin');

