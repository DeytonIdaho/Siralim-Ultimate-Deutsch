import os

def rename_files():
    # Get all files in the current working directory
    files = os.listdir('.')
    
    # Loop through each file
    for filename in files:
        # Check if filename contains "translated_"
        if filename.startswith("translated_"):
            # Create new filename by removing "translated_"
            new_filename = filename.replace("translated_", "", 1)
            
            # Rename the file
            os.rename(filename, new_filename)
            print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    print("Starting file renaming process...")
    rename_files()
    print("File renaming completed.")