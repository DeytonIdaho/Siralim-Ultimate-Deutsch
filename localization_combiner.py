import os
import pandas as pd

def update_localization_files():
    # Step 1: Ask for column name
    column_name = input("Enter the column name to update (e.g., 'Chinese (Traditional)'): ")
    
    # Step 2: Setup folders
    input_folder = "input"
    output_folder = "output"
    log_folder = "logs"
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(log_folder, exist_ok=True)
    
    # Step 3: Find all CSVs in the current directory
    csv_files = [f for f in os.listdir() if f.endswith(".csv")]
    
    for filename in csv_files:
        print(f"\nProcessing {filename}...")
        base_path = filename
        input_path = os.path.join(input_folder, filename)
        
        if not os.path.exists(input_path):
            print(f"Skipping {filename}: no matching file in input folder.")
            continue
        
        try:
            base_df = pd.read_csv(base_path, dtype=str, encoding='utf-8-sig')
            input_df = pd.read_csv(input_path, dtype=str, encoding='utf-8-sig')
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            # Try with different encoding
            try:
                base_df = pd.read_csv(base_path, dtype=str, encoding='utf-8')
                input_df = pd.read_csv(input_path, dtype=str, encoding='utf-8')
            except Exception as e2:
                print(f"Error reading {filename} with utf-8 encoding: {e2}")
                continue
        
        base_df.fillna("", inplace=True)
        input_df.fillna("", inplace=True)
        
        # Get the first column name for both dataframes
        base_tag_col = base_df.columns[0]
        input_tag_col = input_df.columns[0]
        
        print(f"  Base file first column: '{base_tag_col}'")
        print(f"  Input file first column: '{input_tag_col}'")
        print(f"  Looking for column: '{column_name}'")
        
        if column_name not in base_df.columns:
            print(f"Skipping {filename}: '{column_name}' column missing in base.")
            print(f"  Available columns in base: {list(base_df.columns)}")
            continue
        
        if column_name not in input_df.columns:
            print(f"Skipping {filename}: '{column_name}' column missing in input.")
            print(f"  Available columns in input: {list(input_df.columns)}")
            continue
        
        # Create mapping using first column from input file
        input_map = dict(zip(input_df[input_tag_col], input_df[column_name]))
        
        updated_tags = []
        skipped_empty = []
        missing_tags = []
        
        # Iterate through base file using its first column
        for idx, row in base_df.iterrows():
            tag = row[base_tag_col]
            
            if tag in input_map:
                new_val = input_map[tag]
                if new_val != "":
                    base_df.at[idx, column_name] = new_val
                    updated_tags.append(tag)
                else:
                    skipped_empty.append(tag)
            else:
                missing_tags.append(tag)
        
        output_path = os.path.join(output_folder, filename)
        base_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        
        log_path = os.path.join(log_folder, filename.replace(".csv", "_log.txt"))
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(f"Updated column: {column_name}\n")
            log_file.write(f"Used tag column: {base_tag_col} (first column)\n\n")
            
            log_file.write(f"✅ UPDATED TAGS ({len(updated_tags)}):\n")
            log_file.write("\n".join(updated_tags) + "\n\n")
            
            log_file.write(f"⚠️ SKIPPED EMPTY TRANSLATIONS ({len(skipped_empty)}):\n")
            log_file.write("\n".join(skipped_empty) + "\n\n")
            
            log_file.write(f"❌ MISSING FROM INPUT ({len(missing_tags)}):\n")
            log_file.write("\n".join(missing_tags) + "\n")
        
        print(f"[{filename}] {len(updated_tags)} updated, {len(skipped_empty)} skipped (empty), {len(missing_tags)} missing. Log written to '{log_path}'")

if __name__ == "__main__":
    update_localization_files()