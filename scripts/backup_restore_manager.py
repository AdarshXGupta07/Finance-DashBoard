#!/usr/bin/env python3
"""
Backup and Restore Manager for Personal Finance Dashboard
This script handles database backups and restoration
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from sqlalchemy import create_engine, text
from database_mysql import get_mysql_connection
import gzip
import json

class BackupRestoreManager:
    def __init__(self):
        self.engine = None
        self.backup_dir = "backups"
        self.db_name = "personal_finance_dashboard"
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def connect_to_database(self):
        """Establish database connection"""
        try:
            connection_uri = get_mysql_connection()
            self.engine = create_engine(connection_uri)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print("✅ Database connection successful!")
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def get_mysql_credentials(self):
        """Get MySQL credentials from environment or connection string"""
        try:
            connection_uri = get_mysql_connection()
            # Parse connection string to extract credentials
            # Format: mysql+pymysql://user:password@host:port/database
            if "mysql+pymysql://" in connection_uri:
                uri_parts = connection_uri.replace("mysql+pymysql://", "").split("/")
                conn_part = uri_parts[0]
                
                if "@" in conn_part:
                    credentials_part = conn_part.split("@")[0]
                    host_port = conn_part.split("@")[1]
                    
                    if ":" in credentials_part:
                        user, password = credentials_part.split(":", 1)
                    else:
                        user = credentials_part
                        password = ""
                    
                    if ":" in host_port:
                        host, port = host_port.split(":")
                    else:
                        host = host_port
                        port = "3306"
                    
                    return user, password, host, port
        except Exception as e:
            print(f"❌ Error parsing credentials: {e}")
        
        return None, None, None, None
    
    def create_full_backup(self, compress=True):
        """Create full database backup using mysqldump"""
        try:
            user, password, host, port = self.get_mysql_credentials()
            if not all([user, host]):
                print("❌ Could not retrieve MySQL credentials")
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"full_backup_{timestamp}.sql")
            
            if compress:
                backup_file += ".gz"
            
            print(f"🔄 Creating full backup...")
            
            # Build mysqldump command
            cmd = [
                "mysqldump",
                f"--user={user}",
                f"--host={host}",
                f"--port={port}",
                "--single-transaction",
                "--routines",
                "--triggers",
                "--events",
                "--hex-blob",
                "--set-gtid-purged=OFF",
                self.db_name
            ]
            
            if password:
                cmd.insert(1, f"--password={password}")
            
            # Execute backup
            if compress:
                with open(backup_file, 'wb') as f_out:
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    with gzip.GzipFile(fileobj=f_out, mode='wb') as gz_file:
                        for chunk in process.stdout:
                            gz_file.write(chunk)
                    
                    _, stderr = process.communicate()
                    if process.returncode != 0:
                        print(f"❌ Backup failed: {stderr.decode()}")
                        return False
            else:
                with open(backup_file, 'w') as f_out:
                    process = subprocess.Popen(cmd, stdout=f_out, stderr=subprocess.PIPE)
                    _, stderr = process.communicate()
                    if process.returncode != 0:
                        print(f"❌ Backup failed: {stderr.decode()}")
                        return False
            
            # Get file size
            file_size = os.path.getsize(backup_file) / (1024 * 1024)  # MB
            
            print(f"✅ Full backup created successfully!")
            print(f"📁 File: {backup_file}")
            print(f"📊 Size: {file_size:.2f} MB")
            
            return backup_file
            
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def create_data_backup(self):
        """Create data-only backup (excluding structure)"""
        try:
            if not self.connect_to_database():
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"data_backup_{timestamp}.json")
            
            print(f"🔄 Creating data backup...")
            
            # Get all table data
            backup_data = {}
            tables = ['transactions', 'raw_transactions', 'categories', 'accounts']
            
            with self.engine.connect() as conn:
                for table in tables:
                    try:
                        result = conn.execute(text(f"SELECT * FROM {table}"))
                        rows = result.fetchall()
                        columns = result.keys()
                        
                        # Convert to list of dictionaries
                        table_data = []
                        for row in rows:
                            row_dict = dict(zip(columns, row))
                            # Convert datetime objects to strings
                            for key, value in row_dict.items():
                                if isinstance(value, datetime):
                                    row_dict[key] = value.isoformat()
                            table_data.append(row_dict)
                        
                        backup_data[table] = table_data
                        print(f"  📊 Backed up {len(table_data)} rows from {table}")
                        
                    except Exception as e:
                        print(f"⚠️  Warning: Could not backup table {table}: {e}")
            
            # Save to JSON file
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2, default=str)
            
            # Get file size
            file_size = os.path.getsize(backup_file) / (1024 * 1024)  # MB
            
            print(f"✅ Data backup created successfully!")
            print(f"📁 File: {backup_file}")
            print(f"📊 Size: {file_size:.2f} MB")
            
            return backup_file
            
        except Exception as e:
            print(f"❌ Error creating data backup: {e}")
            return False
    
    def restore_full_backup(self, backup_file):
        """Restore database from full backup"""
        try:
            if not os.path.exists(backup_file):
                print(f"❌ Backup file not found: {backup_file}")
                return False
            
            user, password, host, port = self.get_mysql_credentials()
            if not all([user, host]):
                print("❌ Could not retrieve MySQL credentials")
                return False
            
            print(f"🔄 Restoring from backup: {backup_file}")
            
            confirm = input("⚠️  This will replace all existing data. Continue? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("❌ Restore cancelled")
                return False
            
            # Build mysql command
            cmd = [
                "mysql",
                f"--user={user}",
                f"--host={host}",
                f"--port={port}",
                self.db_name
            ]
            
            if password:
                cmd.insert(1, f"--password={password}")
            
            # Execute restore
            if backup_file.endswith('.gz'):
                # Handle compressed backup
                with gzip.open(backup_file, 'rt') as f_in:
                    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    _, stderr = process.communicate(input=f_in.read())
            else:
                # Handle uncompressed backup
                with open(backup_file, 'r') as f_in:
                    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    _, stderr = process.communicate(input=f_in.read())
            
            if process.returncode != 0:
                print(f"❌ Restore failed: {stderr.decode()}")
                return False
            
            print("✅ Database restored successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
    
    def restore_data_backup(self, backup_file):
        """Restore data from JSON backup"""
        try:
            if not os.path.exists(backup_file):
                print(f"❌ Backup file not found: {backup_file}")
                return False
            
            if not self.connect_to_database():
                return False
            
            print(f"🔄 Restoring data from: {backup_file}")
            
            # Load backup data
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            confirm = input("⚠️  This will replace existing data. Continue? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("❌ Restore cancelled")
                return False
            
            with self.engine.connect() as conn:
                for table_name, table_data in backup_data.items():
                    if not table_data:
                        continue
                    
                    print(f"  📊 Restoring {len(table_data)} rows to {table_name}")
                    
                    # Clear existing data
                    conn.execute(text(f"DELETE FROM {table_name}"))
                    
                    # Insert data
                    for row in table_data:
                        # Convert string dates back to datetime if needed
                        for key, value in row.items():
                            if key in ['date', 'created_at', 'updated_at'] and isinstance(value, str):
                                try:
                                    row[key] = datetime.fromisoformat(value)
                                except:
                                    pass
                        
                        # Build insert statement
                        columns = list(row.keys())
                        placeholders = [f":{col}" for col in columns]
                        
                        insert_sql = f"""
                            INSERT INTO {table_name} ({', '.join(columns)})
                            VALUES ({', '.join(placeholders)})
                        """
                        
                        conn.execute(text(insert_sql), row)
                
                conn.commit()
            
            print("✅ Data restored successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error restoring data backup: {e}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        try:
            print(f"\n📁 Available Backups in '{self.backup_dir}':")
            print("-" * 80)
            
            if not os.path.exists(self.backup_dir):
                print("📭 No backup directory found")
                return
            
            backups = []
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    size_mb = stat.st_size / (1024 * 1024)
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    
                    backup_type = "Full" if filename.startswith("full_backup") else "Data"
                    compressed = " (compressed)" if filename.endswith(".gz") else ""
                    
                    backups.append({
                        'filename': filename,
                        'type': backup_type,
                        'size': size_mb,
                        'modified': modified,
                        'compressed': compressed
                    })
            
            if not backups:
                print("📭 No backups found")
                return
            
            # Sort by modification date (newest first)
            backups.sort(key=lambda x: x['modified'], reverse=True)
            
            print(f"{'Filename':<40} {'Type':<8} {'Size (MB)':<12} {'Modified':<20}")
            print("-" * 80)
            
            for backup in backups:
                print(f"{backup['filename']:<40} {backup['type']:<8} {backup['size']:<12.2f} {backup['modified']:<20}{backup['compressed']}")
            
        except Exception as e:
            print(f"❌ Error listing backups: {e}")
    
    def delete_backup(self, backup_file):
        """Delete a backup file"""
        try:
            filepath = os.path.join(self.backup_dir, backup_file) if not os.path.isabs(backup_file) else backup_file
            
            if not os.path.exists(filepath):
                print(f"❌ Backup file not found: {filepath}")
                return False
            
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            
            confirm = input(f"⚠️  Delete '{backup_file}' ({file_size:.2f} MB)? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("❌ Deletion cancelled")
                return False
            
            os.remove(filepath)
            print(f"✅ Backup '{backup_file}' deleted successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting backup: {e}")
            return False
    
    def schedule_automatic_backup(self):
        """Create a script for automatic backups"""
        try:
            script_content = f'''#!/bin/bash
# Automatic Backup Script for Personal Finance Dashboard
# Schedule with cron: 0 2 * * * /path/to/auto_backup.sh

BACKUP_DIR="{os.path.abspath(self.backup_dir)}"
DB_NAME="{self.db_name}"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$BACKUP_DIR/backup.log"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Function to log messages
log_message() {{
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}}

log_message "Starting automatic backup"

# Create full backup
mysqldump --single-transaction --routines --triggers --events --hex-blob --set-gtid-purged=OFF "$DB_NAME" | gzip > "$BACKUP_DIR/auto_backup_$DATE.sql.gz"

if [ $? -eq 0 ]; then
    log_message "Backup completed successfully: auto_backup_$DATE.sql.gz"
    
    # Clean up old backups (keep last 7 days)
    find "$BACKUP_DIR" -name "auto_backup_*.sql.gz" -mtime +7 -delete
    log_message "Old backups cleaned up"
else
    log_message "Backup failed"
fi

log_message "Backup process completed"
'''
            
            script_file = os.path.join(self.backup_dir, "auto_backup.sh")
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            # Make script executable
            os.chmod(script_file, 0o755)
            
            print(f"✅ Automatic backup script created: {script_file}")
            print("📝 To schedule daily backups at 2 AM, add to crontab:")
            print(f"   0 2 * * * {script_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating backup script: {e}")
            return False

def main():
    print("Personal Finance Dashboard - Backup & Restore Manager")
    print("=" * 55)
    
    manager = BackupRestoreManager()
    
    while True:
        print("\n💾 Backup & Restore Options:")
        print("1. Create full backup")
        print("2. Create data backup")
        print("3. List available backups")
        print("4. Restore from backup")
        print("5. Delete backup")
        print("6. Create automatic backup script")
        print("7. Test database connection")
        print("8. Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            backup_file = manager.create_full_backup()
            if backup_file:
                print(f"🎉 Backup completed: {backup_file}")
        
        elif choice == '2':
            backup_file = manager.create_data_backup()
            if backup_file:
                print(f"🎉 Data backup completed: {backup_file}")
        
        elif choice == '3':
            manager.list_backups()
        
        elif choice == '4':
            manager.list_backups()
            backup_file = input("Enter backup filename: ").strip()
            if backup_file:
                if backup_file.endswith('.gz') or backup_file.endswith('.sql'):
                    manager.restore_full_backup(backup_file)
                elif backup_file.endswith('.json'):
                    manager.restore_data_backup(backup_file)
                else:
                    print("❌ Unsupported backup file format")
        
        elif choice == '5':
            manager.list_backups()
            backup_file = input("Enter backup filename to delete: ").strip()
            if backup_file:
                manager.delete_backup(backup_file)
        
        elif choice == '6':
            manager.schedule_automatic_backup()
        
        elif choice == '7':
            manager.connect_to_database()
        
        elif choice == '8':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
