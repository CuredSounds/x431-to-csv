#!/usr/bin/env python3
"""Extract XLSX to CSV for comparison."""
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_xlsx_to_csv(xlsx_path, output_path):
    """Extract first sheet from XLSX to CSV."""
    
    # XLSX is a zip file
    with zipfile.ZipFile(xlsx_path, 'r') as z:
        # Read shared strings
        try:
            strings_xml = z.read('xl/sharedStrings.xml')
            strings_tree = ET.fromstring(strings_xml)
            shared_strings = [
                ''.join(t.text or '' for t in si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'))
                for si in strings_tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si')
            ]
        except:
            shared_strings = []
        
        # Read first sheet
        sheet_xml = z.read('xl/worksheets/sheet1.xml')
        sheet_tree = ET.fromstring(sheet_xml)
        
        # Parse cells
        rows = {}
        for cell in sheet_tree.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
            ref = cell.get('r')
            if not ref:
                continue
            
            # Parse cell reference (e.g., "A1" -> row=1, col=A)
            col = ''.join(c for c in ref if c.isalpha())
            row = int(''.join(c for c in ref if c.isdigit()))
            
            # Get value
            v_elem = cell.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            if v_elem is None or v_elem.text is None:
                value = ''
            else:
                # Check if it's a shared string
                if cell.get('t') == 's':
                    value = shared_strings[int(v_elem.text)]
                else:
                    value = v_elem.text
            
            if row not in rows:
                rows[row] = {}
            rows[row][col] = value
        
        # Convert to CSV
        with open(output_path, 'w', encoding='utf-8') as f:
            for row_num in sorted(rows.keys())[:100]:  # First 100 rows
                row_data = rows[row_num]
                # Get max column
                cols = sorted(row_data.keys(), key=lambda x: (len(x), x))
                values = [row_data.get(col, '') for col in cols]
                f.write(','.join(f'"{v}"' if ',' in str(v) else str(v) for v in values))
                f.write('\n')

if __name__ == '__main__':
    xlsx = Path(sys.argv[1])
    output = xlsx.with_suffix('.extracted.csv')
    extract_xlsx_to_csv(xlsx, output)
    print(f"Extracted to: {output}")

