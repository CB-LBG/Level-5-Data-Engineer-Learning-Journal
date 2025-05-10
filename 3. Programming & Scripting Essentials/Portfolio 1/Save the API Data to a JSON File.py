import sqlite3  # Imports the 'sqlite3' module, which provides functionality for working with SQLite databases.
import json  # Imports the 'json' module, used for working with JSON (JavaScript Object Notation) data.

# Connect to the SQLite database
conn = sqlite3.connect('branches.db')  # Establishes a connection to a SQLite database file named 'branches.db'. If the file doesn't exist, it will be created.
cursor = conn.cursor()  # Creates a cursor object, which allows you to execute SQL queries against the database.

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS branches (
        id TEXT PRIMARY KEY,
        name TEXT,
        address TEXT,
        latitude REAL,
        longitude REAL
    )
''')
# Executes an SQL command to create a table named 'branches' if it doesn't already exist.
# The table has the following columns:
#   - id: TEXT data type, serves as the primary key (unique identifier for each row).
#   - name: TEXT data type, for storing the name of the branch.
#   - address: TEXT data type, for storing the address of the branch.
#   - latitude: REAL data type, for storing the latitude coordinate as a floating-point number.
#   - longitude: REAL data type, for storing the longitude coordinate as a floating-point number.

# Load the JSON data
with open('branches.json') as f:  # Opens the 'branches.json' file in read mode ('r'). The 'with' statement ensures the file is automatically closed.
    data = json.load(f)  # Reads the JSON data from the opened file and parses it into a Python dictionary or list, storing it in the 'data' variable.

# Extract branches
branches = data['data'][0]['Brand'][0]['Branch']
# Accesses a specific nested structure within the loaded JSON data to extract a list of branch information.
# It assumes the JSON has a top-level key 'data', whose value is a list.
# The first element of this list is expected to be a dictionary with a key 'Brand', whose value is also a list.
# The first element of this 'Brand' list is expected to be a dictionary containing a key 'Branch', whose value is the desired list of branch data.

# Insert data into the database
for branch in branches:  # Iterates through each dictionary in the 'branches' list.
    branch_id = branch.get('Identification')  # Safely retrieves the value associated with the key 'Identification' from the current 'branch' dictionary. If the key doesn't exist, it defaults to None.
    name = branch.get('Name')  # Safely retrieves the value associated with the key 'Name' from the current 'branch' dictionary, defaulting to None if not found.
    address_lines = branch.get('PostalAddress', {}).get('AddressLine', [])
    # Safely retrieves the list of address lines. It first tries to get the 'PostalAddress' dictionary, defaulting to an empty dictionary if not found.
    # Then, it tries to get the 'AddressLine' list from the 'PostalAddress' dictionary, defaulting to an empty list if not found.
    address = ', '.join(address_lines)  # Joins the elements of the 'address_lines' list into a single string, separated by commas and spaces.
    geo = branch.get('PostalAddress', {}).get('GeoLocation', {}).get('GeographicCoordinates', {})
    # Safely retrieves the geographic coordinates dictionary by navigating through nested keys: 'PostalAddress', 'GeoLocation', and 'GeographicCoordinates', with default empty dictionaries at each level to prevent errors.
    latitude = float(geo.get('Latitude', 0.0))  # Safely retrieves the 'Latitude' value from the 'geo' dictionary, defaulting to 0.0 if not found, and converts it to a floating-point number.
    longitude = float(geo.get('Longitude', 0.0))  # Safely retrieves the 'Longitude' value from the 'geo' dictionary, defaulting to 0.0 if not found, and converts it to a floating-point number.

    cursor.execute('''
        INSERT OR REPLACE INTO branches (id, name, address, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    ''', (branch_id, name, address, latitude, longitude))
    # Executes an SQL INSERT OR REPLACE command.
    # If a row with the same 'id' already exists, it will be updated with the new values.
    # Otherwise, a new row will be inserted into the 'branches' table with the extracted data.
    # The '?' are placeholders for the values provided in the second argument (a tuple).

# Save and close
conn.commit()  # Saves all the changes made during the current transaction to the database file.
conn.close()  # Closes the connection to the SQLite database. It's important to close the connection to release resources and prevent data corruption.

print("Data inserted successfully.")  # Prints a message to the console indicating that the data has been successfully inserted or updated in the database.
