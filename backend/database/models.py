from .db_connection import create_connection

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(255) UNIQUE,
            phone VARCHAR(15),
            password_hash VARCHAR(255)
        )
    ''')

    # Create Alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            alert_type VARCHAR(50),
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

# Run to create tables when this module is executed
if __name__ == "__main__":
    create_tables()
