"""
Excel File Fixer - QuizNjoy
============================

This script fixes problematic Excel files that have XML corruption issues.
It reads the data and re-saves it as a clean Excel file.

Usage:
    python fix_excel_file.py "path/to/your/file.xlsx"

Or just run it and it will ask for the file path.
"""

import pandas as pd
import sys
import os

def fix_excel_file(input_file):
    """
    Fix a problematic Excel file by reading and re-saving it.
    
    Args:
        input_file: Path to the problematic Excel file
    
    Returns:
        Path to the fixed file
    """
    print(f"\n[*] Fixing Excel file: {input_file}")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"[ERROR] File not found: {input_file}")
        return None
    
    # Generate output filename
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_FIXED.xlsx"
    
    # Try multiple engines to read the file
    engines = ['openpyxl', 'xlrd', None]
    df = None
    successful_engine = None
    
    print("\n[*] Attempting to read file...")
    
    for engine in engines:
        try:
            engine_name = engine if engine else "auto"
            print(f"   Trying engine: {engine_name}...", end=" ")
            
            if engine:
                df = pd.read_excel(input_file, dtype=str, keep_default_na=False, engine=engine)
            else:
                df = pd.read_excel(input_file, dtype=str, keep_default_na=False)
            
            successful_engine = engine_name
            print("[SUCCESS]")
            break
        except Exception as e:
            print(f"[FAILED]: {str(e)[:50]}")
            continue
    
    if df is None:
        print("\n[ERROR] Could not read the Excel file with any available engine.")
        print("\n[INFO] Alternative solution:")
        print("   1. Open the file in Microsoft Excel")
        print("   2. File -> Save As")
        print("   3. Choose 'Excel Workbook (*.xlsx)'")
        print("   4. Save with a new name")
        print("   5. Upload the new file to QuizNjoy")
        return None
    
    print(f"\n[SUCCESS] File read successfully using '{successful_engine}' engine!")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
    
    # Check for required columns
    print("\n[*] Checking columns...")
    required_columns = ['unit_number', 'question_text', 'MCQ Answer', 
                       'option A', 'option B', 'option C', 'option D']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"   [WARNING] Missing columns: {missing_columns}")
        print(f"   Found columns: {list(df.columns)}")
    else:
        print("   [OK] All required columns present!")
    
    # Count valid MCQ questions
    valid_count = 0
    for idx, row in df.iterrows():
        if all([
            str(row.get('question_text', '')).strip() and str(row.get('question_text', '')) != 'nan',
            str(row.get('option A', '')).strip() and str(row.get('option A', '')) != 'nan',
            str(row.get('option B', '')).strip() and str(row.get('option B', '')) != 'nan',
            str(row.get('option C', '')).strip() and str(row.get('option C', '')) != 'nan',
            str(row.get('option D', '')).strip() and str(row.get('option D', '')) != 'nan'
        ]):
            valid_count += 1
    
    print(f"   [OK] Valid MCQ questions: {valid_count}/{len(df)}")
    
    # Save as new Excel file
    print(f"\n[*] Saving fixed file...")
    try:
        # Use xlsxwriter engine for clean output
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        print(f"   [SUCCESS] Fixed file saved: {output_file}")
        print(f"   Location: {os.path.abspath(output_file)}")
        
        # Get file size
        file_size = os.path.getsize(output_file) / 1024  # KB
        print(f"   File size: {file_size:.1f} KB")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Your file has been fixed!")
        print("=" * 60)
        print(f"\n[*] Next steps:")
        print(f"   1. Go to QuizNjoy Admin Dashboard")
        print(f"   2. Click 'Upload Questions'")
        print(f"   3. Select your subject")
        print(f"   4. Upload: {os.path.basename(output_file)}")
        print(f"\n[NOTE] Images cannot be extracted from corrupted files.")
        print(f"   You can add images manually after upload if needed.")
        
        return output_file
        
    except Exception as e:
        print(f"   [ERROR] Error saving file: {str(e)}")
        return None


def main():
    """Main function to run the Excel fixer."""
    print("\n" + "=" * 60)
    print("   Excel File Fixer for QuizNjoy")
    print("=" * 60)
    
    # Get input file path
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        print("\n[*] Enter the path to your Excel file:")
        print("   (or drag and drop the file here)")
        input_file = input().strip().strip('"').strip("'")
    
    if not input_file:
        print("[ERROR] No file provided. Exiting.")
        return
    
    # Fix the file
    result = fix_excel_file(input_file)
    
    if result:
        print(f"\n[SUCCESS] All done! Use the fixed file: {os.path.basename(result)}")
    else:
        print("\n[ERROR] Could not fix the file automatically.")
        print("\n[INFO] Manual fix required:")
        print("   1. Open your Excel file in Microsoft Excel")
        print("   2. Select all data (Ctrl+A)")
        print("   3. Copy (Ctrl+C)")
        print("   4. Create a NEW blank Excel workbook")
        print("   5. Paste (Ctrl+V)")
        print("   6. Add column headers if needed")
        print("   7. Save as .xlsx")
        print("   8. Upload to QuizNjoy")
    
    print("\n" + "=" * 60)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

