#!/usr/bin/env python3
"""
X431 Log File to CSV Converter

Reads LAUNCH diagnostic X431 log files and converts them to CSV format
for easier analysis with other tools.

Author: Neural Harmonics Lab
"""

import struct
import csv
import sys
from pathlib import Path
from typing import List, Tuple


class X431Parser:
    """Parser for LAUNCH X431 diagnostic log files."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.file_data = self._read_file()
        self.point_values: List[str] = []
        self.column_count = 0

    def _read_file(self) -> bytes:
        """Read the entire file into memory."""
        with open(self.filepath, 'rb') as f:
            return f.read()

    def _read_uint8(self, offset: int) -> int:
        """Read unsigned 8-bit integer at offset."""
        return struct.unpack_from('<B', self.file_data, offset)[0]

    def _read_uint16(self, offset: int) -> int:
        """Read unsigned 16-bit little-endian integer at offset."""
        return struct.unpack_from('<H', self.file_data, offset)[0]

    def _read_uint32(self, offset: int) -> int:
        """Read unsigned 32-bit little-endian integer at offset."""
        return struct.unpack_from('<I', self.file_data, offset)[0]

    def _extract_channel_count(self) -> int:
        """Extract the number of data channels/columns."""
        return self._read_uint8(0x134) // 4

    def _extract_point_values(self) -> List[str]:
        """Extract all point value strings from the file."""
        # Navigate to the start of point values section
        offset = 0x0c
        var32 = self._read_uint32(offset)
        offset += 4 + var32

        # Skip 8 header sections
        for _ in range(8):
            var16 = self._read_uint16(offset)
            offset += var16

        # Read all point values
        point_values = []
        file_size = len(self.file_data)

        while offset < file_size:
            if offset + 2 > file_size:
                break

            var16 = self._read_uint16(offset)
            offset += 2

            if var16 < 3 or offset + var16 - 2 > file_size:
                break

            # Extract string (null-terminated)
            value_bytes = self.file_data[offset:offset + var16 - 3]
            try:
                value = value_bytes.decode('utf-8', errors='ignore')
                point_values.append(value)
            except Exception:
                point_values.append("")

            offset += var16 - 2

        return point_values

    def _extract_column_names(self) -> List[str]:
        """Extract column header names."""
        column_names = ["Num"]
        offset = 0x138

        # First pass: get primary column names
        for i in range(self.column_count):
            index = self._read_uint16(offset)
            offset += 4

            if index != 0 and (index - 0x09) < len(self.point_values):
                column_names.append(
                    f"{i + 1}. {self.point_values[index - 0x09]}"
                )
            else:
                column_names.append(f"{i + 1}. Unknown")

        # Second pass: append units/additional info
        for i in range(self.column_count):
            index = self._read_uint16(offset)
            offset += 4

            if index != 0 and (index - 0x09) < len(self.point_values):
                column_names[i + 1] = (
                    f"{column_names[i + 1]} "
                    f"({self.point_values[index - 0x09]})"
                )

        return column_names

    def _extract_data_rows(self) -> List[List[str]]:
        """Extract all data rows from the file."""
        # Find data section
        offset = 0x11c
        var16 = self._read_uint16(offset)
        offset = var16 + 8

        records_count = self._read_uint32(offset)
        offset += 8

        total_rows = (records_count // 4) // self.column_count
        rows = []

        for row_num in range(total_rows):
            row = [str(row_num + 1)]

            for _ in range(self.column_count):
                if offset + 2 > len(self.file_data):
                    row.append("0")
                    continue

                index = self._read_uint16(offset) - 0x09
                offset += 4

                if 0 <= index < len(self.point_values):
                    row.append(self.point_values[index])
                else:
                    row.append("0")

            rows.append(row)

        return rows

    def parse(self) -> Tuple[List[str], List[List[str]]]:
        """
        Parse the X431 file and return headers and data rows.

        Returns:
            Tuple of (column_names, data_rows)
        """
        self.column_count = self._extract_channel_count()
        self.point_values = self._extract_point_values()
        column_names = self._extract_column_names()
        data_rows = self._extract_data_rows()

        return column_names, data_rows


def convert_x431_to_csv(
    input_path: Path,
    output_path: Path = None
) -> None:
    """
    Convert an X431 file to CSV format.

    Args:
        input_path: Path to the .x431 input file
        output_path: Path to the output CSV file (optional)
    """
    if output_path is None:
        output_path = input_path.with_suffix(input_path.suffix + '.csv')

    print(f"Processing: {input_path.name}")

    try:
        parser = X431Parser(input_path)
        column_names, data_rows = parser.parse()

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(data_rows)

        print(f"✓ CSV export complete: {output_path.name}")
        print(f"  Rows: {len(data_rows)}, Columns: {len(column_names)}")

    except Exception as e:
        print(f"✗ Error processing {input_path.name}: {e}")
        raise


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <input-file-path>")
        print("\nExample:")
        print(f"  {Path(sys.argv[0]).name} example.x431")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    if not input_path.suffix == '.x431':
        print(
            f"Warning: File does not have .x431 extension: {input_path}"
        )

    convert_x431_to_csv(input_path)


if __name__ == '__main__':
    main()

