import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """
    Connects to MySQL and creates the database if it does not exist.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            port=int(os.getenv("DB_PORT", 3306))
        )
        cursor = connection.cursor()
        db_name = os.getenv("DB_NAME", "ids_db")

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ Database '{db_name}' is ready!")

        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"❌ Database creation error: {e}")

def create_connection():
    """
    Connects to the specified database in MySQL.
    """
    try:
        create_database()  # Ensure database exists before connecting

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWOSRD", ""),
            database=os.getenv("DB_NAME", "ids_db"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        if connection.is_connected():
            print("✅ Database connection successful!")

        create_tables(connection)  # Ensure tables exist
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Database connection error: {e}")
        return None

def create_tables(connection):
    """
    Creates necessary tables in the database if they do not exist.
    """
    try:
        cursor = connection.cursor()
        
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(15) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(users_table)
        print("✅ Table 'users' is ready!")

        cursor.close()
    except mysql.connector.Error as e:
        print(f"❌ Table creation error: {e}")

# Run the script directly to create DB & table
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()
