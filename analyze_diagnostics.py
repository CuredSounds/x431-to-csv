#!/usr/bin/env python3
"""
X431 Diagnostic Data Analyzer

Provides quick insights and statistics from converted X431 CSV files.

Author: Neural Harmonics Lab
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any


class DiagnosticAnalyzer:
    """Analyzer for X431 diagnostic CSV data."""

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.headers: List[str] = []
        self.data: List[List[str]] = []
        self._load_data()

    def _load_data(self) -> None:
        """Load CSV data into memory."""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.headers = next(reader)
            self.data = list(reader)

    def get_summary(self) -> Dict[str, Any]:
        """Get basic summary statistics."""
        return {
            'file': self.csv_path.name,
            'total_rows': len(self.data),
            'total_columns': len(self.headers),
            'columns': self.headers,
        }

    def get_column_stats(self, column_idx: int) -> Dict[str, Any]:
        """Get statistics for a specific column."""
        if column_idx >= len(self.headers):
            return {}

        values = [row[column_idx] for row in self.data if column_idx < len(row)]

        # Try to parse as numeric
        numeric_values = []
        for val in values:
            try:
                numeric_values.append(float(val))
            except (ValueError, TypeError):
                pass

        stats = {
            'column_name': self.headers[column_idx],
            'total_values': len(values),
            'unique_values': len(set(values)),
        }

        if numeric_values:
            stats['numeric_count'] = len(numeric_values)
            stats['min'] = min(numeric_values)
            stats['max'] = max(numeric_values)
            stats['avg'] = sum(numeric_values) / len(numeric_values)
            stats['type'] = 'numeric'
        else:
            # Show most common values for non-numeric
            value_counts = defaultdict(int)
            for val in values:
                value_counts[val] += 1
            top_values = sorted(
                value_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            stats['most_common'] = top_values
            stats['type'] = 'categorical'

        return stats

    def find_changing_columns(self) -> List[Dict[str, Any]]:
        """Find columns that have changing values (not constant)."""
        changing = []

        for i in range(1, len(self.headers)):  # Skip "Num" column
            values = [
                row[i] for row in self.data
                if i < len(row) and row[i] not in ['0', '', 'Not Avl']
            ]
            unique_values = set(values)

            if len(unique_values) > 1:
                changing.append({
                    'index': i,
                    'name': self.headers[i],
                    'unique_count': len(unique_values),
                    'sample_values': list(unique_values)[:5]
                })

        return changing

    def print_summary(self) -> None:
        """Print a formatted summary report."""
        summary = self.get_summary()

        print(f"\n{'='*70}")
        print(f"  Diagnostic Data Summary: {summary['file']}")
        print(f"{'='*70}\n")
        print(f"  Total Rows:    {summary['total_rows']:,}")
        print(f"  Total Columns: {summary['total_columns']}")
        print()

        changing = self.find_changing_columns()
        print(f"  Active Channels: {len(changing)} (columns with varying data)")
        print()

        if changing:
            print("  Top 10 Active Channels:")
            print(f"  {'-'*66}")
            for i, col in enumerate(changing[:10], 1):
                name = col['name'][:50]
                print(f"  {i:2}. {name}")
                print(f"      Unique values: {col['unique_count']}")
                print(f"      Samples: {', '.join(str(v)[:20] for v in col['sample_values'][:3])}")
                print()

        # Show some column statistics
        if len(changing) > 0:
            print(f"\n  {'='*70}")
            print("  Detailed Statistics for First Active Channel:")
            print(f"  {'='*70}\n")
            first_col = changing[0]['index']
            stats = self.get_column_stats(first_col)
            for key, value in stats.items():
                if key != 'most_common':
                    print(f"  {key:20}: {value}")
            if 'most_common' in stats:
                print(f"  most_common:")
                for val, count in stats['most_common']:
                    print(f"    '{val}': {count} occurrences")

        print(f"\n{'='*70}\n")


def main():
    """Main entry point for the analyzer CLI."""
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <csv-file-path>")
        print("\nExample:")
        print(f"  {Path(sys.argv[0]).name} example.x431.csv")
        sys.exit(1)

    csv_path = Path(sys.argv[1])

    if not csv_path.exists():
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)

    if not csv_path.suffix == '.csv':
        print(f"Warning: File does not have .csv extension: {csv_path}")

    analyzer = DiagnosticAnalyzer(csv_path)
    analyzer.print_summary()


if __name__ == '__main__':
    main()

