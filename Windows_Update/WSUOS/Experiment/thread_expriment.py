import subprocess
import os
import re
import sqlite3
import xml.etree.ElementTree as ET
import xmltodict
import json
import time
import threading
from queue import Queue

# ---------- Utility Functions ----------
def extract_7z(archive_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Run the 7z command
    command = ['7z', 'x', archive_path, f'-o{output_folder}', '-aos']
    
    try:
        subprocess.run(command, check=True)
        print(f"Extraction completed successfully to: {output_folder}")
    except subprocess.CalledProcessError as e:
        print(f"Error during extraction: {e}")

class SQLiteWriterThread:
    def __init__(self, db_path):
        self.db_path = db_path
        self.queue = Queue()
        self.stop_event = threading.Event()

        # Create a thread for handling writes
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        connection = sqlite3.connect(self.db_path, check_same_thread=False)
        connection.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode for concurrency
        cursor = connection.cursor()

        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                # Process all available items in the queue
                while not self.queue.empty():
                    query, params = self.queue.get()
                    cursor.execute(query, params)
                connection.commit()
            except Exception as e:
                print(f"Database write error: {e}")
            finally:
                # Sleep briefly to yield control
                threading.Event().wait(0.1)

        # Clean up after stopping
        cursor.close()
        connection.close()

    def add_write(self, query, params=()):
        """Add a query to the queue for the write thread to process."""
        self.queue.put((query, params))

    def stop(self):
        """Stop the writer thread and ensure all writes are completed."""
        self.stop_event.set()
        self.thread.join()

# Usage example
def insert_data(writer, update_data):
    writer.add_write('''
            INSERT OR IGNORE INTO Updates_metadata (
                id, CreationDate, RevisionId, RevisionNumber, DefaultLanguage, 
                IsLeaf, IsBundle, DeploymentAction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            update_data["id"],
            update_data["CreationDate"],
            update_data["RevisionId"],
            update_data["RevisionNumber"],
            update_data["DefaultLanguage"],
            update_data["IsLeaf"],
            update_data["IsBundle"],
            update_data["DeploymentAction"]
        ))

def create_metadata_table(xml_data, db_path):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the Updates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Updates_metadata (
            id TEXT PRIMARY KEY,
            CreationDate TEXT,
            RevisionId TEXT,
            RevisionNumber TEXT,
            DefaultLanguage TEXT,
            IsLeaf TEXT,
            IsBundle TEXT,
            DeploymentAction TEXT
        )
    ''')
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    # Initialize the database and writer thread
    writer = SQLiteWriterThread("updates.db")
    threads = []
    # Extract and insert each <Update> element into the table
    for update in xml_data.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Updates'):
        update_data = {
            "id": update.attrib.get('UpdateId'),
            "CreationDate": update.attrib.get('CreationDate'),
            "RevisionId": update.attrib.get('RevisionId', None),
            "RevisionNumber": update.attrib.get('RevisionNumber', None),
            "DefaultLanguage": update.attrib.get('DefaultLanguage', None),
            "IsLeaf": update.attrib.get('IsLeaf', None),
            "IsBundle": update.attrib.get('IsBundle', None),
            "DeploymentAction": update.attrib.get('DeploymentAction', None),
        }

        t = threading.Thread(target=insert_data, args=(writer, update_data))
        t.start()
        threads.append(t)

    # Wait for all insert threads to finish
    for t in threads:
        t.join()

    # Stop the writer thread
    writer.stop()
    print("Data metadata inserted successfully.")

def main():
    start_time = time.time()

    # Example usage
    archive_path = "wsusscn2.cab"
    output_folder = "wsusscn2_extracted"
    
    # Extract wsusscn2.cab to wsusscn2_extracted
    extract_7z(archive_path, output_folder)

    # Extract package.cab
    archive_path = output_folder + "/package.cab"
    output_folder = output_folder + "/package_extracted"
    extract_7z(archive_path, output_folder)
    
    # Read content of package.xml
    current_file = output_folder + "/package.xml"
    root = ET.parse(current_file, parser = ET.XMLParser(encoding = 'utf-8'))
    
    db_path = "updates.db"
    # Create Updates_metadata table in SQLite database
    create_metadata_table(root, db_path)
    
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")

if __name__ == "__main__":
    main()

## TODO: Keep database connection open and reuse it for multiple queries.
## TODO: Use Thread or Process to extract packages in parallel.