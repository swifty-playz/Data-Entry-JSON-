# ===== UNIVERSAL JSON DATA ENTRY TOOL =====
print("This is a universal data entry tool made with Python used to create, edit, and delete JSON files.")
print("This tool's basic version will be fully fleshed out with comments to be altered in any specific ways for any tasks (e.g., language data, creature data, etc.).");


import json
import os

# Finds exact folder where data_entry.py is currently sitting
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create subdirectories relative to the script location
SCHEMA_FOLDER = os.path.join(BASE_DIR, "schemas")
DATABASE_FOLDER = os.path.join(BASE_DIR, "databases")

# Create folders automatically so file saving never crashes
os.makedirs(SCHEMA_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# Active targets start empty
active_schema_path = None
active_database_path = None
active_schema = "None"
active_database = "None"


def main():
	home_screen()


# Home Screen
# "===== UNIVERSAL JSON DATA ENTRY TOOL ====="
# "Active Directory: ./directory_name/"

# "[1] Edit schema file"
# "[2] Edit database file"
# "[3] Create a brand new JSON database"

# "Select action (1-3) or 'Q' to quit: "

def home_screen():
	global active_schema_path
	global active_database_path

	# Selecting actions
	while True:
		# Clear the screen for clarity on next loop
		clear_screen()

		print("===== UNIVERSAL JSON DATA ENTRY TOOL =====")
		print("\n--- Home Screen ---\n")

		# Get active directory and print it
		print(f"Active Directory: {BASE_DIR}\n")

		print("[1] Edit schema file")
		print("[2] Edit database file")
		print("[3] Create a brand new SCHEMA blueprint")
		print("[4] Create a brand new DATABASE file from a schema")
		print()

		choice = input("Select action (1-4) or 'Q' to quit: ")

		if choice == '1':
			# SCHEMA ONLY WORKFLOW
			chosen_file = select_file(SCHEMA_FOLDER, "schema")
			if chosen_file:
				active_schema_path = chosen_file
				active_schema = os.path.basename(active_schema_path)
				active_database_path = None
				active_database = "None"
			main_action_menu()

		elif choice == '2':
			# DATABASE WORKFLOW (AUTO-LOAD)
			chosen_file = select_file(DATABASE_FOLDER, "database")
			if chosen_file:
				load_database_and_schema(chosen_file)
				if active_database_path and active_schema_path:
					main_action_menu()
		elif choice == '3':
			print("Creating new schema blueprint")
			create_new_schema()
			#return
		elif choice == '4':
			print("Creating new JSON database")
			create_new_database()
			#return
		elif choice == 'Q' or choice == 'q':
			return
		else:
			print("Please enter either 1-3 or 'Q' for an action\n")


# File selection
def select_file(target_folder, label_name):
	print(f"\nChoose a {label_name} file:")

	# Scan folder and check if it is empty
	files = [f for f in os.listdir(target_folder) if f.endswith('.json')]

	if not files:
		print(f"[ No existing {label_name} files found ]")
		return None

	# Print files with numbers for easy selection
	for index, filename in enumerate(files, start=1):
		print(f"[{index}] {filename}")

	# Get user choice
	choice = input("> ")

	# Convert choice to index and return the full path
	try:
		selected_index = int(choice) - 1
		if 0 <= selected_index < len(files):
			chosen_file = files[selected_index]
			return os.path.join(target_folder, chosen_file)
	except ValueError:
		pass

	print("Invalid selection.")
	return None


def load_database_and_schema(chosen_db_path):
	global active_database_path
	global active_schema_path
	global active_database
	global active_schema

	try:
		with open(chosen_db_path, "r") as f:
			data = json.load(f)

		# Lock onto the database path
		active_database_path = chosen_db_path
		active_database = os.path.basename(chosen_db_path)

		# Extract the schema name from the file's metadata wrapper
		schema_name = data.get("schema_used")
		active_schema = schema_name

		# Automatically stitch together the full path to that schema
		active_schema_path = os.path.join(SCHEMA_FOLDER, schema_name)

		# Double check that the schema file actually exists on the disk
		if not os.path.exists(active_schema_path):
			print(f"\n[Warning] This database requires '{schema_name}', but that schema file is missing.")
			active_schema_path = None
			active_schema = "None"
	except Exception as e:
		print(f"Error loading file data: {e}")


def create_new_database():
	print("\n--- Create a Brand New Database ---")

	# Get the new filename
	db_name = input("Enter a name for your new database file: ").strip()
	if not db_name:
		print("Filename cannot be blank.")
		return None

	# Auto append .json extension if the user forgets to type it
	if not db_name.endswith(".json"):
		db_name += ".json"

	full_db_path = os.path.join(DATABASE_FOLDER, db_name)

	# Check if file already exists to prevent accidental overwrites
	if os.path.exists(full_db_path):
		print(f"Error: A database file named '{db_name}' already exists.")
		return None

	# Force selection of a schema blueprint
	print(f"\nSelect a schema layout blueprint for '{db_name}':")
	chosen_schema_path = select_file(SCHEMA_FOLDER, "schema")

	if not chosen_schema_path:
		print("Database creation cancelled because no valid schema was selected.")
		return None

	# Extract just the filename to store as a reference
	schema_filename = os.path.basename(chosen_schema_path)

	# Blueprint wrapper
	db_structure = {
		"schema_used": schema_filename,
		"entries": []	# Data records will live inside this list
	}

	print(db_structure)

	# Initialize the file with an empty JSON array
	# A fresh database must start as a valid JSON list [] so you can append records to it later
	try:
		with open(full_db_path, "w") as f:
			json.dump(db_structure, f, indent=4)	# indent=4 keeps the text file readable
		print(f"\nSuccessfully created database file: {db_name} linked to {schema_filename}.")

		# Return both paths so the script can immediately load them into active memory
		return full_db_path, chosen_schema_path
	except Exception as e:
		print(f"An error occurred while creating the file: {e}")
		return None


def create_new_schema():
	print("\n--- Create a Brand New Schema Blueprint ---")

	# Get the new schema filename
	schema_name = input("Enter a name for this schema: ").strip()
	if not schema_name:
		print("Schema name cannot be blank.")
		return None

	# Auto append .json extension if the user forgets to type it
	if not schema_name.endswith(".json"):
		schema_name += ".json"

	full_schema_path = os.path.join(SCHEMA_FOLDER, schema_name)

	# Check if file already exists to prevent accidental overwrites
	if os.path.exists(full_schema_path):
		print(f"Error: A schema file named '{schema_name}' already exists.")
		return None

	# Field collection loop
	schema_fields = []
	print("\nEnter the fields you want in this schema one by one.")
	print("Press [Enter] on a blank line when you are completely finished.")
	print("-" * 50)

	while True:
		# Number the field prompt dynamically based on list size
		field_number = len(schema_fields) + 1
		field_name = input(f"Field Num. {field_number} Name: ").strip()

		# User pressed enter on an empty line, so stop collecting fields
		if not field_name:
			break

		# Prevent duplicate fields within the same schema blueprint
		if field_name in schema_fields:
			print(f"The field '{field_name}' is already in this schema.")
			continue

		schema_fields.append(field_name)

	# Guard against saving an empty blueprint
	if not schema_fields:
		print("\nSchema creation cancelled. A schema must have at least one field.")
		return None

	# Save the schema list to the file
	try:
		with open(full_schema_path, "w") as f:
			json.dump(schema_fields, f, indent=4)	# indent=4 keeps the text file readable

		print(f"\nSuccessfully created schema blueprint: {schema_name}")
		print(f"Fields saved: {', '.join(schema_fields)}")
		return full_schema_path

	except Exception as e:
		print(f"An error occurred while saving the schema: {e}")
		return None



# Main Action Menu
# "DATABASE: yokai_watch.json | SCHEMA: creatures_schema.json"

# "[1] Add new Entry"
# "[2] Search / Edit Entries"
# "[3] Delete an Entry"
# "[4] View All (Print Data)"
# "[5] Drop to Manual Editor (Nano)"
# "[6] Change Active File/Schema"

# "Select action (1-6) or 'B' to go back: "

def main_action_menu():
	# Selecting actions
	while True:
		print("\n--- Main Action Menu ---")

		# Print active database and schema
		if active_database_path == None:
			print(f"\nDATABASE: {active_database_path} | SCHEMA: {os.path.basename(active_schema_path)}\n")
		else:
			print(f"\nDATABASE: {os.path.basename(active_database_path)} | SCHEMA: {os.path.basename(active_schema_path)}\n")

		print("[1] Add new Entry")
		print("[2] Search / Edit Entries")
		print("[3] Delete an Entry")
		print("[4] View Entire Database")
		print("[5] View Schema")
		print("[6] Drop to Manual Editor (Nano)")
		print("[7] Change Active File/Schema")
		print("[8] Delete Schema")
		print("[9] Delete Database")
		print()

		choice = input("Select action (1-9) or 'B' to go back: ")

		if choice == '1':
			add_entry()
			#return
		elif choice == '2':
			print("Searching / Editing Entries")
			#return
		elif choice == '3':
			print("Deleting an Entry")
			#return
		elif choice == '4':
			print_database()
			#return
		elif choice == '5':
			print_schema()
			#return
		elif choice == '6':
			print("Dropping to Manuel Editor")
			#return
		elif choice == '7':
			print("Changing Active File/Schema")
			#return
		elif choice == '8':
			print("Deleting Schema")
			#return
		elif choice == '9':
			print("Deleting Database")
			#return
		elif choice == 'B' or choice == 'b':
			return
		else:
			print("\nPlease enter either 1-9 or 'B' for an action")


# Dynamic Entry Form (Core Mechanic)
# "--- Adding New Entry ---"	# Loops through schema with a for loop
# "--- Filling Data Fields from Schema: {active_schema} ---"
# "Name: "
# "Tribe: "
# "Rank: "
# "Element: "
# "Location: "

# "[S] Save Entry"
# "[C] Cancel Entry"

# "Select action 'S' or 'C': "

# "Entry '{name}' already exists. [O]verwrite or [C]ancel?"	# Prints if user selects 'S' but main entry (name, word, etc.) already exists in the file
# "Select action 'O' or 'C': "

# "Entry added successfully!"	# Prints if user selects 'S' and it is the only entry of its kind

def add_entry():
	global active_database_path
	global active_schema_path
	global active_schema
	
	# Safety Check: Prevent crashes if no file is currently loaded
	if not active_database_path or not active_schema_path:
		print("Error: No active database or schema loaded.")
		input("\nPress [Enter] to go back.")
		return
	
	print("\n--- Add Entry Form ---\n")
	print(f"Filling Data Fields from Schema: {active_schema}\n")
	
	# Read the schema file to see what fields are needed
	with open(active_schema_path, "r") as f:
			fields = json.load(f)
			
	# Loop through fields and collect inputs into a clean directory
	new_entry = {}
	for field in fields:
			user_input = input(f"{field}: ").strip()
			new_entry[field] = user_input
		
	# deleted code----------------
			
	# Confirm Saving
	print("\n[S]ave Entry")
	print("[C]ancel Entry")
	action = input("Select action 'S' or 'C': ").strip().upper()
	
	if action == 'S':
		# Open the database file and load the earlier built structure
		with open(active_database_path, "r") as f:
			db_data = json.load(f)
		
		# Duplicate Entry Check
		# Grab the primary key field name (will always be index 0 of the schema layout)
		primary_key_field = fields[0]
		new_value_to_check = new_entry[primary_key_field].lower().strip()
		
		duplicate_found = False
		duplicate_index = -1
		
		# Scan existing records inside the data array for a matching entry string
		for idx, existing_entry in enumerate(db_data["entries"]):
			if existing_entry.get(primary_key_field, "").lower().strip() == new_value_to_check:
				duplicate_found = True
				duplicate_index = idx
				break
		
		# If a match is found, prompt user with an overwrite loop
		if duplicate_found:
			print(f"\nEntry '{new_entry[primary_key_field]}' already exists.")
			print("[O]verwrite or [C]ancel?")
			overwrite_choice = input("Select action 'O' or 'C': ").upper()
			
			if overwrite_choice == 'O':
				# Replace the old record dictionary completely with the new one
				db_data["entries"] [duplicate_index] = new_entry
				print("\nEntry overwritten successfully.")
			else:
				print("\nSave cancelled. Existing entry preserved.")
				input("\nPress [Enter] to go back to the menu.")
				return
		else:
			# Append the new entry dictionary (no duplicate) to the 'entries' list inside the database
			db_data["entries"].append(new_entry)

		# Save the entire updated structure back to the file
		with open(active_database_path, "w") as f:
			json.dump(db_data, f, indent=4)
			
		print("\nEntry added successfully.")
		input("\nPress [Enter] to continue.")
	else:
		print("\nEntry cancelled.")
		input("\nPress [Enter] to continue.")

	# Access schema for the database
	# Loop through fields from schema, requesting value inputs
	# Combine fields and values, and add them to a single entry in the database
	
	return
	
	
def add_schema_field():
	# Ask for a field name
	# Add new field into the schema blueprint
	
	# Ask user if they want to add this field into all entries using this updated schema

	return
	
	
def remove_schema_field():
	# Ask which field to remove
	# Remove that field from the schema blueprint
	
	# Ask user if they want to remove this field from all entries using this updated schema
	
	return
	

def update_database_with_new_schema():
	# This function may be called when a schema is updated
	# It will update the entries in a database with an updated schema (added/removed fields)
	
	return


def print_database():
	# Open the database file and load the data into db_data
	with open(active_database_path, "r") as f:
			db_data = json.load(f)
			
	# Convert the dictionary into a perfectly indented string
	pretty_json = json.dumps(db_data, indent=4)
	
	print("\nViewing the Entire Database")
	print("-" * 50)
	print(pretty_json)
	print("-" * 50)
	
	input("\nPress [Enter] to go back.")


def print_schema():
	# Open the schema file and load the data into schema_data
	with open(active_schema_path, "r") as f:
			schema_data = json.load(f)
			
	# Convert the dictionary into a perfectly indented string
	pretty_json = json.dumps(schema_data, indent=4)
	
	print("\nViewing the Schema")
	print("-" * 50)
	print(pretty_json)
	print("-" * 50)
	
	input("\nPress [Enter] to go back.")


def clear_screen():
	# 'nt' means Windows, 'posix' covers Linux and Mac
	os.system('cls' if os.name == 'nt' else 'clear')


main()





# Writes "Choose JSON file:"
	# "1) file1"	# reference file1.json
	# "2) file2"	# reference file2.json
	# "3) file3"	# reference file3.json
# If file does not exist in current directory, it creates new file (file4.json)

# Writes "Enter choice:"
# Go through each field of the JSON file (based of schema) for the entry
# "Word:"
# "> "
# "Meaning:"
# "> "
# If word is already covered, give the otpion to continue on or overwrite it with a new value

# Add the full entry into the JSON file





# Writes UI
# ls -> Reads files in current directory
# open file.json -> Opens JSON file to fully read
# create file.json -> Creates JSON file

# Universal
# Schemas?
# UI: Create, Program Edit, Nano Edit, Delete, Open, Read, Search, ls
# Create folders?
# Looping system
# Call function for each major task
# Able to Open JSON file to fully read
# Able to Read a defined amount of the file
# Able to Search if a defined object is in the file
# Able to Edit through a designed method via this program (i.e., search for specific object, look through the inside, and edit it)
# Able to Edit through a Nano call on the file for manual edits
