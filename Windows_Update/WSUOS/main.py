import subprocess
import os
import sqlite3
import xml.etree.ElementTree as ET

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
        
        # Insert into the database
        cursor.execute('''
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
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Data metadata inserted successfully.")

def create_file_locations_table(xml_data, db_path):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the Updates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS File_locations (
            id TEXT PRIMARY KEY,
            Url TEXT
        )
    ''')
    
    # Extract and insert each <Update> element into the table
    for update in xml_data.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}FileLocations'):
        update_data = {
            "id": update.attrib.get('Id'),
            "Url": update.attrib.get('Url'),
        }
        
        # Insert into the database
        cursor.execute('''
            INSERT OR IGNORE INTO File_locations (
                id, Url
            ) VALUES (?, ?)
        ''', (
            update_data["id"],
            update_data["Url"]
        ))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Data file locations inserted successfully.")

def create_details_table(xml_data, db_path):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the Update_details table for storing file_id and bundle_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Update_details (
            id TEXT,
            file_id TEXT,
            bundle_id TEXT,
            FOREIGN KEY (id) REFERENCES Updates(id)
        )
    ''')
    
    # Extract and insert each <Update> element into the tables
    for update in xml_data.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Updates'):
        update_data = {
            "id": update.attrib.get('UpdateId'),
            "DeploymentAction": update.attrib.get('DeploymentAction', None)
        }
        
        # Extract file_id and bundle_id for Update_details table

        if update_data["DeploymentAction"] != "Bundle":
            continue

        file_id = None
        bundle_id = None

        # Check if there's a <PayloadFiles> and extract <File Id>
        payload_files = update.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}PayloadFiles')
        if payload_files is not None:
            file_element = payload_files.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}File')
            if file_element is not None:
                file_id = file_element.attrib.get('Id')
        
        # Check if there's a <BundledBy> element and extract <Revision Id>
        bundled_by = update.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}BundledBy')
        if bundled_by is not None:
            revision_element = bundled_by.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Revision')
            if revision_element is not None:
                bundle_id = revision_element.attrib.get('Id')
        
        # Insert file_id and bundle_id into the Update_details table
        cursor.execute('''
            INSERT OR IGNORE INTO Update_details (id, file_id, bundle_id)
            VALUES (?, ?, ?)
        ''', (update_data["id"], file_id, bundle_id))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Data Update details inserted successfully.")

def main():
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
    
    # Create File_locations table in SQLite database
    create_file_locations_table(root, db_path)

    # Create Update_details table in SQLite database
    create_details_table(root, db_path)

if __name__ == "__main__":
    main()