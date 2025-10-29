# X431 Log File to CSV Converter

This program reads LAUNCH diagnostic X431 log files and converts them into CSV format for easier analysis with various tools.
It extracts structured data from the proprietary binary format into readable CSV files.

## Features
- ✓ Parse LAUNCH X431 diagnostic log files
- ✓ Extract all data channels with proper headers and units
- ✓ Support for batch processing multiple files
- ✓ Available in both Go and Python implementations

## Prerequisites

### Python Version (Recommended)
- Python 3.7 or higher
- No external dependencies (uses standard library only)

### Go Version
- Go 1.16 or higher

## Installation

Clone the repository and navigate into the directory:

```bash
git clone https://github.com/ucukertz/x431-to-csv.git && cd x431-to-csv
```

### Build Go Version (Optional)

```bash
go build -o x431-to-csv
```

### Python Version

No build required - Python scripts are ready to use.

```bash
chmod +x x431_to_csv.py batch_convert.py
```

## Usage

### Single File Conversion

**Python:**
```bash
python3 x431_to_csv.py <input-file-path>
# or
./x431_to_csv.py example.x431
```

**Go:**
```bash
./x431-to-csv example.x431
```

Both will generate `example.x431.csv` in the same directory as your input file.

### Batch Processing (Python only)

Convert all `.x431` files in a directory:

```bash
python3 batch_convert.py Files/
# or
./batch_convert.py Files/
```

This will process all `.x431` files recursively and create corresponding `.csv` files.

## Output Format

The CSV output includes:
- **Row numbers** in the first column
- **Data channel headers** with descriptive names and units
- **All timestamped data points** from the diagnostic session

Example output structure:
```csv
Num,1. Battery Voltage (V),2. Engine RPM (rpm),3. Coolant Temp (°C),...
1,14.2,850,89,...
2,14.1,855,90,...
```

## Example

```bash
$ python3 batch_convert.py Files/

Found 5 .x431 file(s)

Processing: TOYOTA_989347712041_20251028105043.x431
✓ CSV export complete: TOYOTA_989347712041_20251028105043.x431.csv
  Rows: 9630, Columns: 25

Processing: TOYOTA_989347712041_20251028105656.x431
✓ CSV export complete: TOYOTA_989347712041_20251028105656.x431.csv
  Rows: 82134, Columns: 25

============================================================
Conversion complete:
  ✓ Success: 5
  ✗ Errors:  0
============================================================
```

## File Format Details

The X431 format is a proprietary binary format used by LAUNCH diagnostic tools. The parser:
1. Reads channel configuration at offset `0x134`
2. Extracts point value strings (parameter names, units)
3. Builds column headers with descriptive names and units
4. Extracts all timestamped data records
5. Outputs to standard CSV format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See [LICENSE](LICENSE) file for details.

## Credits

- Original Go implementation: [ucukertz](https://github.com/ucukertz)
- Python port and enhancements: Neural Harmonics Lab