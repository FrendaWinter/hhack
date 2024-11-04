import subprocess
import os
import re
import sqlite3
import xml.etree.ElementTree as ET
import xmltodict
import json

# ---------- Utility Functions ----------

def find_package_for_id(id_num, index_content):
    # Search for the package that contains the ID
    for package, range_values in index_content.items():
        if range_values["start"] <= id_num <= (range_values["end"] or float('inf')):
            return package
    return None  # ID not found in any package range

def find_file_in_package_folder(id_str, package_name):
    # Define the folder path
    folder_path = f"wsusscn2_extracted/{package_name}_extracted/c/"
    
    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return None

    # Look for a file that matches the ID
    for filename in os.listdir(folder_path):
        if filename == id_str:
            return os.path.join(folder_path, filename)
    
    print(f"No file named {id_str} found in {folder_path}.")
    return None

def find_file_by_id(id_text, index_content):
    # Convert ID to integer
    try:
        id_num = int(id_text)
    except ValueError:
        print("Invalid ID format. Please provide a numeric ID.")
        return None

    # Find the package the ID belongs to
    package = find_package_for_id(id_num, index_content)
    if not package:
        print("ID does not belong to any known package.")
        return None

    # Find the file in the package's folder
    file_path = find_file_in_package_folder(id_text, package)
    if file_path:
        # print(f"File found: {file_path}")
        return file_path
    else:
        # print(f"File not found. Id: {id_text}, package: {package}")
        return None
    
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

# ---------- Main Functions ----------
def extract_core_data(revision_id, index_content):
    core_file_location = find_file_by_id(revision_id, index_content)
    try:
        file = open(core_file_location, encoding="utf8")
        # Workaround to able to parse the XML content
        xml_content = "<root>" + file.read() + "</root>"
        root = ET.fromstring(xml_content)
        
        # Get the Properties UpdateType attribute
        properties = root.find("Properties")
        update_type = properties.get("UpdateType") if properties is not None else None
        
        # Get the content of ApplicabilityRules and Relationships tags
        applicability_rules = root.find("ApplicabilityRules")
        applicability_content = ET.tostring(applicability_rules, encoding="utf-8") if applicability_rules is not None else None
        applicability_content = json.dumps(xmltodict.parse(applicability_content)) if applicability_rules is not None else None
        
        relationships = root.find("Relationships")
        relationships_content = ET.tostring(relationships, encoding="utf-8") if relationships is not None else None
        relationships_content = json.dumps(xmltodict.parse(relationships_content)) if relationships is not None else None

        return update_type, applicability_content, relationships_content
    
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None, None, None

def create_metadata_table(xml_data, db_path, index_content):
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
            DeploymentAction TEXT,
            Properties TEXT,
            Relationships TEXT,
            ApplicabilityRules TEXT
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
        
        Properties, Relationships, ApplicabilityRules = extract_core_data(update_data["RevisionId"], index_content)

        # Insert into the database
        cursor.execute('''
            INSERT OR IGNORE INTO Updates_metadata (
                id, CreationDate, RevisionId, RevisionNumber, DefaultLanguage, 
                IsLeaf, IsBundle, DeploymentAction, Properties, Relationships, ApplicabilityRules
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            update_data["id"],
            update_data["CreationDate"],
            update_data["RevisionId"],
            update_data["RevisionNumber"],
            update_data["DefaultLanguage"],
            update_data["IsLeaf"],
            update_data["IsBundle"],
            update_data["DeploymentAction"],
            Properties, Relationships, ApplicabilityRules
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
            languages TEXT,
            prerequisites TEXT,
            FOREIGN KEY (id) REFERENCES Updates(id)
        )
    ''')
    
    # Extract and insert each <Update> element into the tables
    for update in xml_data.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Updates'):
        update_data = {
            "id": update.attrib.get('UpdateId')
        }

        file_id = None
        bundle_id = None
        languages_data = None
        prerequisites_data = None

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
        
        
        # Check if there's a <Languages> element and extract <Language Name>
        languages = update.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Languages')
        if languages is not None:
            languages_data = [lang.get('Name') for lang in languages.findall('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Language')]
            languages_data = ','.join(str(v) for v in languages_data)
        
        # Extract Prerequisites
        prerequisites = update.find('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Prerequisites')
        if prerequisites is not None:
            prerequisites_data = [prerequisite.get('Id') for prerequisite in prerequisites.findall('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}UpdateId')]
            for or_element in prerequisites.findall('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}Or'):
                prerequisites_data.append([or_prerequisite.get('Id') for or_prerequisite in or_element.findall('{http://schemas.microsoft.com/msus/2004/02/OfflineSync}UpdateId')])
            prerequisites_data = ','.join(str(v) for v in prerequisites_data)

        # Insert file_id and bundle_id into the Update_details table
        cursor.execute('''
            INSERT OR IGNORE INTO Update_details (id, file_id, bundle_id, languages, prerequisites)
            VALUES (?, ?, ?, ?, ?)
        ''', (update_data["id"], file_id, bundle_id, languages_data, prerequisites_data))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print("Data Update details inserted successfully.")

def extract_all_packages(base_folder):
    """Extracts all package.cab files in the base folder."""
    pattern = re.compile(r'package(\d+)\.cab')
    package_numbers = []

    # Iterate over files in the folder
    for filename in os.listdir(base_folder):
        match = pattern.match(filename)
        if match:
            # Convert the extracted number to an integer and add to the list
            package_numbers.append(int(match.group(1)))
    
    print(package_numbers)
    for i in range(min(package_numbers), max(package_numbers) + 1):
        archive_path = os.path.join(base_folder, f"package{i}.cab")
        output_folder = os.path.join(base_folder, f"package{i}_extracted")
        extract_7z(archive_path, output_folder)

def extract_index_xml(base_folder):
    """Extracts the index.xml file from the base folder."""
    index_xml_path = os.path.join(base_folder, "index.xml")
    root = ET.parse(index_xml_path, parser = ET.XMLParser(encoding = 'utf-8'))

    cabs = root.find('CABLIST').findall('CAB')
    
    package_ranges = {}
    previous_range_start = 0

    # Process each package
    for i, cab in enumerate(cabs):
        # Get package name without ".cab"
        package_name = cab.get('NAME').replace('.cab', '')

        # Get the start range (default to previous if not present)
        current_range_start = int(cab.get('RANGESTART', previous_range_start))

        # Determine end range (one less than next package's start, if it exists)
        if i + 1 < len(cabs) and 'RANGESTART' in cabs[i + 1].attrib:
            next_range_start = int(cabs[i + 1].get('RANGESTART'))
            end_index = next_range_start - 1
        else:
            end_index = None  # Last package has no end range

        # Save to dictionary
        package_ranges[package_name] = {"start": current_range_start, "end": end_index}
        previous_range_start = current_range_start
    
    return package_ranges

def main():
    # Example usage
    archive_path = "wsusscn2.cab"
    output_folder = "wsusscn2_extracted"
    
    # Extract wsusscn2.cab to wsusscn2_extracted
    extract_7z(archive_path, output_folder)

    # Read content of index.xml
    index_content = extract_index_xml(output_folder)

    # Extract other package.cab files
    # extract_all_packages(output_folder)

    # Extract package.cab
    archive_path = output_folder + "/package.cab"
    output_folder = output_folder + "/package_extracted"
    # extract_7z(archive_path, output_folder)
    
    # Read content of package.xml
    current_file = output_folder + "/package.xml"
    root = ET.parse(current_file, parser = ET.XMLParser(encoding = 'utf-8'))
    
    db_path = "updates.db"
    # Create Updates_metadata table in SQLite database
    create_metadata_table(root, db_path, index_content)
    
    # Create File_locations table in SQLite database
    create_file_locations_table(root, db_path)

    # Create Update_details table in SQLite database
    create_details_table(root, db_path)

if __name__ == "__main__":
    main()

## TODO: Keep database connection open and reuse it for multiple queries.
## TODO: Use Thread or Process to extract packages in parallel.