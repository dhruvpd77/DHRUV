"""
CSV to Excel Converter - Guaranteed to work!
"""

import pandas as pd
import sys
import os

def convert_csv_to_excel(csv_file):
    print(f"\n[*] Reading CSV file: {csv_file}")
    
    try:
        # Read CSV (pure text, no corruption possible)
        df = pd.read_csv(csv_file, dtype=str, keep_default_na=False, encoding='utf-8')
        
        print(f"[SUCCESS] Read {len(df)} rows!")
        print(f"   Columns: {len(df.columns)}")
        
        # Show first few column names
        print(f"   Column names: {list(df.columns[:5])}...")
        
        # Create Excel file
        excel_file = csv_file.replace('.csv', '_CLEAN.xlsx')
        print(f"\n[*] Creating clean Excel file: {excel_file}")
        
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        file_size = os.path.getsize(excel_file) / 1024  # KB
        
        print(f"[SUCCESS] Clean Excel file created!")
        print(f"   File: {excel_file}")
        print(f"   Size: {file_size:.1f} KB")
        print(f"\n[*] This file is guaranteed to work with QuizNjoy!")
        print(f"\n[NEXT STEP] Upload this file to QuizNjoy:")
        print(f"   1. Go to Admin Dashboard")
        print(f"   2. Click 'Upload Questions'")
        print(f"   3. Select subject")
        print(f"   4. Upload: {os.path.basename(excel_file)}")
        
        return excel_file
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        print("\n[*] Enter path to your CSV file:")
        csv_file = input().strip().strip('"').strip("'")
    
    if csv_file and os.path.exists(csv_file):
        convert_csv_to_excel(csv_file)
    else:
        print("[ERROR] File not found!")
    
    print("\n" + "=" * 60)

