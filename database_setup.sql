-- Database setup for Landing Page Registration System
-- Run this script in MySQL to create the database and table

-- Create database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS Ciber_Vault_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE Ciber_Vault_db;

-- Create usuarios table
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Add indexes for better performance
    INDEX idx_correo (correo),
    INDEX idx_fecha_registro (fecha_registro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample data (optional)
-- Note: These are just examples, passwords are hashed
-- INSERT INTO usuarios (nombre, correo, password_hash, fecha_nacimiento) VALUES
-- ('Juan Pérez', 'juan@example.com', '$2y$10$example_hash_here', '1995-05-15'),
-- ('María García', 'maria@example.com', '$2y$10$example_hash_here', '1988-12-03');

-- Show table structure
DESCRIBE usuarios;

-- Show table status
SELECT 
    'Table created successfully' as status,
    COUNT(*) as user_count 
FROM usuarios;