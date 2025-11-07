"""
Ultra-Clean Excel Converter
Reads even severely corrupted files and creates clean output
"""

import openpyxl
import pandas as pd
import sys

def convert_file(input_file):
    print("\n[*] Reading file cell by cell (slow but works)...")
    
    try:
        # Read with read_only mode (most forgiving)
        wb = openpyxl.load_workbook(input_file, read_only=True, data_only=True)
        ws = wb.active
        
        # Read all data row by row
        all_data = []
        for idx, row in enumerate(ws.iter_rows(values_only=True)):
            row_data = [str(cell) if cell is not None else '' for cell in row]
            all_data.append(row_data)
            if idx % 100 == 0:
                print(f"   Read {idx} rows...")
        
        wb.close()
        
        print(f"\n[SUCCESS] Read {len(all_data)} rows!")
        
        # Save as CSV first (removes ALL Excel corruption)
        csv_file = input_file.replace('.xlsx', '_CLEAN.csv')
        print(f"\n[*] Saving as CSV: {csv_file}")
        
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            import csv
            writer = csv.writer(f)
            writer.writerows(all_data)
        
        print(f"[SUCCESS] CSV saved!")
        
        # Now read CSV and save as clean Excel
        print(f"\n[*] Converting CSV to clean Excel...")
        df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
        
        output_file = input_file.replace('.xlsx', '_ULTRA_CLEAN.xlsx')
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        print(f"[SUCCESS] Clean Excel created: {output_file}")
        print(f"\n[*] Now upload this file to QuizNjoy!")
        
        return output_file
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        print("Enter file path:")
        input_file = input().strip().strip('"').strip("'")
    
    convert_file(input_file)
    input("\nPress Enter to exit...")

