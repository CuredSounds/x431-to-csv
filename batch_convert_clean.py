#!/usr/bin/env python3
"""
Batch X431 to Clean CSV Converter

Processes all .x431 files with Excel-friendly formatting.

Author: Neural Harmonics Lab
"""

import sys
from pathlib import Path
from x431_to_csv_clean import convert_x431_to_csv


def batch_convert_clean(directory: Path = None) -> None:
    """
    Convert all .x431 files to Excel-friendly CSV format.

    Args:
        directory: Directory containing .x431 files (default: current dir)
    """
    if directory is None:
        directory = Path.cwd()
    else:
        directory = Path(directory)

    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    x431_files = sorted(directory.glob('**/*.x431'))

    if not x431_files:
        print(f"No .x431 files found in {directory}")
        return

    print(f"Found {len(x431_files)} .x431 file(s)")
    print("Creating Excel-friendly CSV files...\n")

    success_count = 0
    error_count = 0

    for x431_file in x431_files:
        try:
            convert_x431_to_csv(x431_file)
            success_count += 1
        except Exception as e:
            print(f"  Error: {e}")
            error_count += 1
        print()

    print(f"{'='*60}")
    print(f"Conversion complete:")
    print(f"  ✓ Success: {success_count}")
    print(f"  ✗ Errors:  {error_count}")
    print(f"\nFiles created with '_clean.csv' suffix")
    print(f"These have simplified headers optimized for Excel!")
    print(f"{'='*60}")


def main():
    """Main entry point for batch processing CLI."""
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    batch_convert_clean(directory)


if __name__ == '__main__':
    main()

