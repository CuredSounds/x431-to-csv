#!/usr/bin/env python3
"""Debug X431 file structure to understand the format better."""

import struct
import sys
from pathlib import Path


def debug_x431(filepath: Path):
    """Debug X431 file structure."""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print(f"File: {filepath.name}")
    print(f"Size: {len(data):,} bytes\n")
    
    # Magic signature
    magic = data[0:4].decode('ascii', errors='ignore')
    print(f"Magic: {magic}")
    
    # Channel count at 0x134
    channel_count = struct.unpack_from('<B', data, 0x134)[0] // 4
    print(f"Channel Count: {channel_count}")
    
    # Extract point values (all strings in the file)
    print(f"\n{'='*70}")
    print("Extracting Point Values (all parameter strings)...")
    print(f"{'='*70}\n")
    
    offset = 0x0c
    var32 = struct.unpack_from('<I', data, offset)[0]
    offset += 4 + var32
    
    # Skip 8 headers
    for i in range(8):
        var16 = struct.unpack_from('<H', data, offset)[0]
        offset += var16
    
    point_values = []
    while offset < len(data):
        if offset + 2 > len(data):
            break
        
        var16 = struct.unpack_from('<H', data, offset)[0]
        offset += 2
        
        if var16 < 3 or offset + var16 - 2 > len(data):
            break
        
        value_bytes = data[offset:offset + var16 - 3]
        try:
            value = value_bytes.decode('utf-8', errors='ignore')
            point_values.append(value)
            if len(point_values) <= 50:  # Show first 50
                print(f"  [{len(point_values)-1:3d}] {value}")
        except:
            break
        
        offset += var16 - 2
    
    print(f"\n  ... Total {len(point_values)} point values extracted")
    
    # Show column header mapping
    print(f"\n{'='*70}")
    print("Column Header Mapping (from file offsets 0x138+)")
    print(f"{'='*70}\n")
    
    offset = 0x138
    print("First pass (primary parameter names):")
    indices_pass1 = []
    for i in range(channel_count):
        index = struct.unpack_from('<H', data, offset)[0]
        offset += 4
        indices_pass1.append(index)
        
        if index != 0 and (index - 0x09) < len(point_values):
            param = point_values[index - 0x09]
            print(f"  Col {i+1:2d}: Index={index:4d} → \"{param}\"")
        else:
            print(f"  Col {i+1:2d}: Index={index:4d} → (invalid/missing)")
    
    print(f"\nSecond pass (units/secondary labels):")
    indices_pass2 = []
    for i in range(channel_count):
        index = struct.unpack_from('<H', data, offset)[0]
        offset += 4
        indices_pass2.append(index)
        
        if index != 0 and (index - 0x09) < len(point_values):
            param = point_values[index - 0x09]
            print(f"  Col {i+1:2d}: Index={index:4d} → \"{param}\"")
        else:
            print(f"  Col {i+1:2d}: Index={index:4d} → (invalid/missing)")
    
    print(f"\n{'='*70}")
    print("Combined Column Headers (as currently generated):")
    print(f"{'='*70}\n")
    
    for i in range(min(channel_count, 10)):  # Show first 10
        idx1 = indices_pass1[i]
        idx2 = indices_pass2[i]
        
        name1 = point_values[idx1 - 0x09] if idx1 != 0 and (idx1 - 0x09) < len(point_values) else "?"
        name2 = point_values[idx2 - 0x09] if idx2 != 0 and (idx2 - 0x09) < len(point_values) else "?"
        
        print(f"  Col {i+1:2d}: \"{name1}\" ({name2})")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <x431-file>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    debug_x431(filepath)

