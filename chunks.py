import os
import csv
import time
import math

def save_characters_with_limit(characters, base_filename, max_chars=1500):
    """
    Save characters to files with a maximum character limit.
    If characters exceed the limit, create multiple files.
    
    Returns the list of created filenames.
    """
    chars_list = list(characters)
    total_chars = len(chars_list)
    
    if total_chars == 0:
        return []
    
    # Calculate number of files needed
    num_files = math.ceil(total_chars / max_chars)
    created_files = []
    
    # Split extension from base filename
    name_parts = base_filename.rsplit('.', 1)
    base_name = name_parts[0]
    extension = name_parts[1] if len(name_parts) > 1 else 'txt'
    
    if num_files == 1:
        # If all characters fit in one file, use the original filename
        with open(base_filename, 'w', encoding='utf-8') as file:
            file.write(''.join(chars_list))
        created_files.append(base_filename)
    else:
        # Create multiple files with numbering
        for i in range(num_files):
            start_idx = i * max_chars
            end_idx = min((i + 1) * max_chars, total_chars)
            
            # Create filename with part number
            filename = f"{base_name}_part{i+1}.{extension}"
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(''.join(chars_list[start_idx:end_idx]))
            
            created_files.append(filename)
    
    return created_files

def extract_characters():
    print("Multi-Language Character Extractor")
    print("===================================\n")
    print("This script will extract unique characters from CSV columns:")
    print("• Chinese (Simplified): 'Chinese (Standard)' and 'Chinese (Simplified)' → unique_simplified_characters.txt")
    print("• Chinese (Traditional): 'Chinese (Traditional)' → unique_traditional_characters.txt")
    print("• Japanese: 'Japanese' → unique_japanese_characters.txt")
    print("• Korean: 'Korean' → unique_korean_characters.txt")
    print("• ASCII characters (32-126) will be added to all files")
    print("• Files will be split if they exceed 1500 characters\n")
    
    # Get all CSV files in the current directory
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the current directory.")
        return
    
    # Sets to store unique characters for each language
    simplified_chars = set()
    traditional_chars = set()
    japanese_chars = set()
    korean_chars = set()
    
    # Add ASCII characters from 32 to 126 to all sets
    print("Adding ASCII characters (32-126) to all output files...")
    for char_code in range(32, 127):
        char = chr(char_code)
        simplified_chars.add(char)
        traditional_chars.add(char)
        japanese_chars.add(char)
        korean_chars.add(char)
    
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
                has_japanese = 'Japanese' in field_names
                has_korean = 'Korean' in field_names
                
                # Print columns found
                if has_standard:
                    print(f"  ✓ Found 'Chinese (Standard)' column (→ simplified file)")
                if has_simplified:
                    print(f"  ✓ Found 'Chinese (Simplified)' column (→ simplified file)")
                if has_traditional:
                    print(f"  ✓ Found 'Chinese (Traditional)' column (→ traditional file)")
                if has_japanese:
                    print(f"  ✓ Found 'Japanese' column (→ japanese file)")
                if has_korean:
                    print(f"  ✓ Found 'Korean' column (→ korean file)")
                
                if not (has_standard or has_simplified or has_traditional or has_japanese or has_korean):
                    print(f"  ✗ No relevant language columns found, skipping...")
                    continue
                
                # Reset position to start of file
                file.seek(0)
                reader = csv.DictReader(file)
                
                # Process each row
                row_count = 0
                for row in reader:
                    row_count += 1
                    
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
                    
                    # JAPANESE FILE: Add characters from Japanese
                    if has_japanese and 'Japanese' in row and row['Japanese']:
                        for char in row['Japanese']:
                            japanese_chars.add(char)
                    
                    # KOREAN FILE: Add characters from Korean
                    if has_korean and 'Korean' in row and row['Korean']:
                        for char in row['Korean']:
                            korean_chars.add(char)
                
                print(f"  Processed {row_count} rows")
                    
        except Exception as e:
            print(f"  Error processing {csv_file}: {e}")
    
    # Remove ASCII chars for counting language-specific characters only
    ascii_chars = set(chr(i) for i in range(32, 127))
    chinese_simplified_count = len(simplified_chars - ascii_chars)
    chinese_traditional_count = len(traditional_chars - ascii_chars)
    japanese_count = len(japanese_chars - ascii_chars)
    korean_count = len(korean_chars - ascii_chars)
    
    print("\n=== SAVING FILES (max 1500 chars per file) ===")
    
    # Save all character sets with file splitting
    all_outputs = []
    
    # Save Simplified Chinese characters
    if len(simplified_chars) > 0:
        simplified_files = save_characters_with_limit(
            simplified_chars, 
            "unique_simplified_characters.txt", 
            max_chars=1500
        )
        all_outputs.append(("Simplified Chinese", simplified_files, chinese_simplified_count, len(simplified_chars)))
    
    # Save Traditional Chinese characters
    if len(traditional_chars) > 0:
        traditional_files = save_characters_with_limit(
            traditional_chars, 
            "unique_traditional_characters.txt", 
            max_chars=1500
        )
        all_outputs.append(("Traditional Chinese", traditional_files, chinese_traditional_count, len(traditional_chars)))
    
    # Save Japanese characters
    if len(japanese_chars) > 0:
        japanese_files = save_characters_with_limit(
            japanese_chars, 
            "unique_japanese_characters.txt", 
            max_chars=1500
        )
        all_outputs.append(("Japanese", japanese_files, japanese_count, len(japanese_chars)))
    
    # Save Korean characters
    if len(korean_chars) > 0:
        korean_files = save_characters_with_limit(
            korean_chars, 
            "unique_korean_characters.txt", 
            max_chars=1500
        )
        all_outputs.append(("Korean", korean_files, korean_count, len(korean_chars)))
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"ASCII characters added to all files: 95 (code points 32-126)")
    print()
    
    for lang_name, files, lang_count, total_count in all_outputs:
        print(f"{lang_name}:")
        print(f"  • {lang_count} unique {lang_name} characters")
        print(f"  • {total_count} total characters (including ASCII)")
        print(f"  • Files created:")
        for filename in files:
            # Get actual character count in file
            with open(filename, 'r', encoding='utf-8') as f:
                file_char_count = len(f.read())
            print(f"    - {filename} ({file_char_count} characters)")
        print()
    
    if not all_outputs:
        print("No characters were extracted from the CSV files.")

if __name__ == "__main__":
    extract_characters()
    print("\nProcess completed.")
    print("\nPress Enter to exit...")
    input()  # This keeps the console window open until user presses Enter