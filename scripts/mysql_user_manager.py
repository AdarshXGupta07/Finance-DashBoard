#!/usr/bin/env python3
"""
MySQL User Management Script for Personal Finance Dashboard
This script manages MySQL users with secure password handling
"""

import os
import sys
import getpass
import secrets
import string
import hashlib
from sqlalchemy import create_engine, text
import pymysql

class MySQLUserManager:
    def __init__(self, host='localhost', port='3306'):
        self.host = host
        self.port = port
        self.root_engine = None
        
    def get_root_connection(self):
        """Get MySQL root connection"""
        print("🔐 MySQL Root Authentication Required")
        print("=" * 40)
        
        root_user = input("Enter MySQL root username (default: root): ") or "root"
        root_password = getpass.getpass("Enter MySQL root password: ")
        
        try:
            connection_string = f"mysql+pymysql://{root_user}:{root_password}@{self.host}:{self.port}/mysql"
            self.root_engine = create_engine(connection_string)
            with self.root_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Root authentication successful!")
            return True
        except Exception as e:
            print(f"❌ Root authentication failed: {e}")
            return False
    
    def generate_secure_password(self, length=16):
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def hash_password(self, password):
        """Create a hash of the password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_finance_user(self, username='finance_user', password=None):
        """Create the finance application user"""
        if not self.root_engine:
            if not self.get_root_connection():
                return None, None
        
        if not password:
            password = self.generate_secure_password()
            print(f"🔑 Generated secure password: {password}")
        
        db_name = "personal_finance_dashboard"
        
        try:
            with self.root_engine.connect() as conn:
                # Drop user if exists
                conn.execute(text(f"DROP USER IF EXISTS '{username}'@'localhost'"))
                conn.execute(text(f"DROP USER IF EXISTS '{username}'@'%'"))
                
                # Create user
                conn.execute(text(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'"))
                conn.execute(text(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'"))
                
                # Grant privileges
                conn.execute(text(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'localhost'"))
                conn.execute(text(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{username}'@'%'"))
                
                # Grant usage for connection testing
                conn.execute(text(f"GRANT USAGE ON *.* TO '{username}'@'localhost'"))
                conn.execute(text(f"GRANT USAGE ON *.* TO '{username}'@'%'"))
                
                conn.execute(text("FLUSH PRIVILEGES"))
                
                print(f"✅ User '{username}' created successfully!")
                print(f"📝 User has full access to '{db_name}' database")
                
                return username, password
                
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return None, None
    
    def create_readonly_user(self, username='finance_reader', password=None):
        """Create a read-only user for reporting"""
        if not self.root_engine:
            if not self.get_root_connection():
                return None, None
        
        if not password:
            password = self.generate_secure_password()
            print(f"🔑 Generated secure password: {password}")
        
        db_name = "personal_finance_dashboard"
        
        try:
            with self.root_engine.connect() as conn:
                # Drop user if exists
                conn.execute(text(f"DROP USER IF EXISTS '{username}'@'localhost'"))
                conn.execute(text(f"DROP USER IF EXISTS '{username}'@'%'"))
                
                # Create user
                conn.execute(text(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'"))
                conn.execute(text(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'"))
                
                # Grant read-only privileges
                conn.execute(text(f"GRANT SELECT ON {db_name}.* TO '{username}'@'localhost'"))
                conn.execute(text(f"GRANT SELECT ON {db_name}.* TO '{username}'@'%'"))
                conn.execute(text(f"GRANT SHOW VIEW ON {db_name}.* TO '{username}'@'localhost'"))
                conn.execute(text(f"GRANT SHOW VIEW ON {db_name}.* TO '{username}'@'%'"))
                
                conn.execute(text("FLUSH PRIVILEGES"))
                
                print(f"✅ Read-only user '{username}' created successfully!")
                print(f"📝 User has read-only access to '{db_name}' database")
                
                return username, password
                
        except Exception as e:
            print(f"❌ Error creating read-only user: {e}")
            return None, None
    
    def update_user_password(self, username, new_password=None):
        """Update password for existing user"""
        if not self.root_engine:
            if not self.get_root_connection():
                return False
        
        if not new_password:
            new_password = self.generate_secure_password()
            print(f"🔑 Generated new secure password: {new_password}")
        
        try:
            with self.root_engine.connect() as conn:
                # Update password for both host patterns
                conn.execute(text(f"ALTER USER '{username}'@'localhost' IDENTIFIED BY '{new_password}'"))
                conn.execute(text(f"ALTER USER '{username}'@'%' IDENTIFIED BY '{new_password}'"))
                conn.execute(text("FLUSH PRIVILEGES"))
                
                print(f"✅ Password updated for user '{username}'!")
                return new_password
                
        except Exception as e:
            print(f"❌ Error updating password: {e}")
            return None
    
    def list_users(self):
        """List all users related to the finance dashboard"""
        if not self.root_engine:
            if not self.get_root_connection():
                return
        
        try:
            with self.root_engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT user, host 
                    FROM mysql.user 
                    WHERE user LIKE '%finance%' OR user LIKE '%dashboard%'
                    ORDER BY user, host
                """))
                
                users = result.fetchall()
                
                if users:
                    print("\n📋 Finance Dashboard Users:")
                    print("-" * 40)
                    for user, host in users:
                        print(f"  👤 {user}@{host}")
                else:
                    print("\n📭 No finance dashboard users found")
                    
        except Exception as e:
            print(f"❌ Error listing users: {e}")
    
    def delete_user(self, username):
        """Delete a user"""
        if not self.root_engine:
            if not self.get_root_connection():
                return False
        
        confirm = input(f"⚠️  Are you sure you want to delete user '{username}'? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ User deletion cancelled")
            return False
        
        try:
            with self.root_engine.connect() as conn:
                conn.execute(text(f"DROP USER IF EXISTS '{username}'@'localhost'"))
                conn.execute(text(f"DROP USER IF EXISTS '{username}'@'%'"))
                conn.execute(text("FLUSH PRIVILEGES"))
                
                print(f"✅ User '{username}' deleted successfully!")
                return True
                
        except Exception as e:
            print(f"❌ Error deleting user: {e}")
            return False
    
    def test_user_connection(self, username, password):
        """Test connection with user credentials"""
        try:
            connection_string = f"mysql+pymysql://{username}:{password}@{self.host}:{self.port}/personal_finance_dashboard"
            engine = create_engine(connection_string)
            
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                test_value = result.fetchone()[0]
                
            if test_value == 1:
                print(f"✅ Connection test successful for user '{username}'!")
                return True
            else:
                print(f"❌ Connection test failed for user '{username}'")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed for user '{username}': {e}")
            return False
    
    def create_env_file(self, username, password, filename='.env'):
        """Create .env file with user credentials"""
        env_content = f"""# MySQL Database Configuration
MYSQL_USER={username}
MYSQL_PASSWORD={password}
MYSQL_HOST={self.host}
MYSQL_PORT={self.port}
MYSQL_DATABASE=personal_finance_dashboard

# Application Settings
APP_ENV=production
DEBUG=False

# Security
SECRET_KEY={self.generate_secure_password(32)}
"""
        
        try:
            with open(filename, 'w') as f:
                f.write(env_content)
            print(f"✅ Environment file '{filename}' created successfully!")
            print("🔒 Keep this file secure and do not commit to version control")
            return True
        except Exception as e:
            print(f"❌ Error creating environment file: {e}")
            return False

def main():
    print("Personal Finance Dashboard - MySQL User Manager")
    print("=" * 50)
    
    manager = MySQLUserManager()
    
    while True:
        print("\n🔧 User Management Options:")
        print("1. Create main finance user")
        print("2. Create read-only user")
        print("3. Update user password")
        print("4. List finance users")
        print("5. Delete user")
        print("6. Test user connection")
        print("7. Create .env file")
        print("8. Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            username = input("Enter username (default: finance_user): ") or "finance_user"
            password = getpass.getpass("Enter password (leave empty for auto-generated): ") or None
            user, passw = manager.create_finance_user(username, password)
            if user and passw:
                manager.create_env_file(user, passw)
        
        elif choice == '2':
            username = input("Enter username (default: finance_reader): ") or "finance_reader"
            password = getpass.getpass("Enter password (leave empty for auto-generated): ") or None
            manager.create_readonly_user(username, password)
        
        elif choice == '3':
            username = input("Enter username: ")
            if username:
                password = getpass.getpass("Enter new password (leave empty for auto-generated): ") or None
                manager.update_user_password(username, password)
        
        elif choice == '4':
            manager.list_users()
        
        elif choice == '5':
            username = input("Enter username to delete: ")
            if username:
                manager.delete_user(username)
        
        elif choice == '6':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            if username and password:
                manager.test_user_connection(username, password)
        
        elif choice == '7':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            filename = input("Enter filename (default: .env): ") or ".env"
            if username and password:
                manager.create_env_file(username, password, filename)
        
        elif choice == '8':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
