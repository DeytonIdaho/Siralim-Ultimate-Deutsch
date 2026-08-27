import os
import csv
import time

def extract_chinese_characters():
    print("Chinese Character Extractor")
    print("==========================\n")
    print("This script will:")
    print("1. Extract characters from 'Chinese (Standard)' and 'Chinese (Simplified)' columns into unique_simplified_characters.txt")
    print("2. Extract characters from 'Chinese (Traditional)' columns into unique_traditional_characters.txt")
    print("3. Add ASCII characters (32-126) to both files\n")
    
    # Get all CSV files in the current directory
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the current directory.")
        return
    
    # Sets to store unique characters
    simplified_chars = set()
    traditional_chars = set()
    
    # Add ASCII characters from 32 to 126 to both sets
    print("Adding ASCII characters (32-126) to both output files...")
    for char_code in range(32, 127):
        char = chr(char_code)
        simplified_chars.add(char)
        traditional_chars.add(char)
    
    # Process each CSV file
    print(f"\nFound {len(csv_files)} CSV files to process...")
    for csv_file in csv_files:
        print(f"\nProcessing: {csv_file}")
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                # Create CSV reader
                reader = csv.DictReader(file)
                
                # Check which columns exist in this file
                field_names = reader.fieldnames or []
                has_standard = 'Chinese (Standard)' in field_names
                has_simplified = 'Chinese (Simplified)' in field_names
                has_traditional = 'Chinese (Traditional)' in field_names
                
                # Print columns found
                if has_standard:
                    print(f"  ✓ Found 'Chinese (Standard)' column (goes to simplified file)")
                if has_simplified:
                    print(f"  ✓ Found 'Chinese (Simplified)' column (goes to simplified file)")
                if has_traditional:
                    print(f"  ✓ Found 'Chinese (Traditional)' column (goes to traditional file)")
                
                if not (has_standard or has_simplified or has_traditional):
                    print(f"  ✗ No relevant Chinese columns found, skipping...")
                    continue
                
                # Reset position to start of file
                file.seek(0)
                reader = csv.DictReader(file)
                
                # Track characters added from this file
                standard_count = 0
                simplified_count = 0
                traditional_count = 0
                
                # Process each row
                for row in reader:
                    # SIMPLIFIED FILE: Add characters from Chinese (Standard)
                    if has_standard and 'Chinese (Standard)' in row and row['Chinese (Standard)']:
                        for char in row['Chinese (Standard)']:
                            simplified_chars.add(char)
                    
                    # SIMPLIFIED FILE: Add characters from Chinese (Simplified)
                    if has_simplified and 'Chinese (Simplified)' in row and row['Chinese (Simplified)']:
                        for char in row['Chinese (Simplified)']:
                            simplified_chars.add(char)
                    
                    # TRADITIONAL FILE: Add characters from Chinese (Traditional)
                    if has_traditional and 'Chinese (Traditional)' in row and row['Chinese (Traditional)']:
                        for char in row['Chinese (Traditional)']:
                            traditional_chars.add(char)
                    
        except Exception as e:
            print(f"  Error processing {csv_file}: {e}")
    
    # Remove ASCII chars for counting Chinese characters only
    ascii_chars = set(chr(i) for i in range(32, 127))
    chinese_simplified_count = len(simplified_chars - ascii_chars)
    chinese_traditional_count = len(traditional_chars - ascii_chars)
    
    # Save Simplified characters to text file
    simplified_output = "unique_simplified_characters.txt"
    with open(simplified_output, 'w', encoding='utf-8') as file:
        file.write(''.join(simplified_chars))
    
    # Save Traditional characters to text file
    traditional_output = "unique_traditional_characters.txt"
    with open(traditional_output, 'w', encoding='utf-8') as file:
        file.write(''.join(traditional_chars))
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"ASCII characters added to both files: 95 (code points 32-126)")
    print(f"Simplified file ({simplified_output}):")
    print(f"  - {chinese_simplified_count} unique Chinese characters from 'Chinese (Standard)' and 'Chinese (Simplified)' columns")
    print(f"  - {len(simplified_chars)} total characters (including ASCII)")
    print(f"Traditional file ({traditional_output}):")
    print(f"  - {chinese_traditional_count} unique Chinese characters from 'Chinese (Traditional)' columns")
    print(f"  - {len(traditional_chars)} total characters (including ASCII)")

if __name__ == "__main__":
    extract_chinese_characters()
    print("\nProcess completed.")
    print("\nPress Enter to exit...")
    input()  # This keeps the console window open until user presses Enter