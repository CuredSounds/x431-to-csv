# X431-to-CSV Quick Start Guide

## 🚀 Quick Commands

### Convert a single file
```bash
python3 x431_to_csv.py Files/TOYOTA_989347712041_20251028105043.x431
```

### Convert all files in a directory
```bash
python3 batch_convert.py Files/
```

### Analyze converted data
```bash
python3 analyze_diagnostics.py Files/TOYOTA_989347712041_20251028105043.x431.csv
```

## 📊 Your Current Files

### Original X431 Files (5 total)
```
Files/
├── TOYOTA_989347712041_20251028105043.x431  (956 KB)  →  9,630 rows
├── TOYOTA_989347712041_20251028105656.x431  (7.7 MB)  → 82,134 rows
├── TOYOTA_989347712041_20251028120111.x431  (7.8 MB)  → 83,691 rows
├── TOYOTA_989347712041_20251028150616.x431  (9.5 MB)  → 101,547 rows
└── TOYOTA_989347712041_20251028162810.x431  (1.3 MB)  → 13,095 rows
```

All files have **25 data channels** including:
- Battery voltage
- Engine diagnostics
- A/F (Air/Fuel) sensor readings
- Catalyst monitor data
- Misfire counts
- And 20+ other diagnostic parameters

### Converted CSV Files
All `.x431` files have been converted to `.csv` format in the same directory.

## 🔍 Common Analysis Tasks

### Find active sensors
```bash
python3 analyze_diagnostics.py Files/TOYOTA_989347712041_20251028105043.x431.csv
```

### Open in spreadsheet
```bash
open Files/TOYOTA_989347712041_20251028105043.x431.csv
# or
excel Files/TOYOTA_989347712041_20251028105043.x431.csv
```

### Process with pandas (Python)
```python
import pandas as pd

df = pd.read_csv('Files/TOYOTA_989347712041_20251028105043.x431.csv')
print(df.describe())
print(df.head())
```

### Filter specific columns with grep
```bash
head -1 Files/TOYOTA_989347712041_20251028105043.x431.csv | tr ',' '\n' | nl
```

## 📁 Project Structure

```
x431-to-csv/
├── main.go                    # Original Go implementation
├── x431_to_csv.py             # Python converter (single file)
├── batch_convert.py           # Python batch processor
├── analyze_diagnostics.py     # Data analyzer utility
├── Files/                     # Your diagnostic data
│   ├── *.x431                 # Original binary files
│   └── *.x431.csv            # Converted CSV files
├── README.md                  # Full documentation
├── QUICKSTART.md              # This file
└── requirements.txt           # Python dependencies (none)
```

## 🛠️ Utilities Created

1. **x431_to_csv.py** - Single file converter
   - Parses binary X431 format
   - Extracts headers with units
   - Outputs clean CSV

2. **batch_convert.py** - Batch processor
   - Recursive directory scanning
   - Progress reporting
   - Error handling

3. **analyze_diagnostics.py** - Data analyzer
   - Summary statistics
   - Active channel detection
   - Quick insights

## 💡 Tips

- CSV files can be opened in Excel, Numbers, Google Sheets
- Use pandas for advanced analysis in Python
- Use R or MATLAB for signal processing
- Check the "Active Channels" to find which sensors had varying data
- The `Num` column is the row number/timestamp index

## 📝 Next Steps

1. **Explore the data**: Open CSV files in your preferred tool
2. **Time-series analysis**: Plot sensor values over time
3. **Anomaly detection**: Look for unusual patterns
4. **Compare sessions**: Analyze differences between diagnostic runs
5. **Export for ML**: Use CSV format for machine learning pipelines

## 🐛 Troubleshooting

### File not found error
- Ensure the file path is correct
- Use absolute paths if relative paths fail

### Encoding issues
- All CSV files use UTF-8 encoding
- If special characters appear wrong, check your viewer's encoding settings

### Performance
- Large files (>100K rows) may take a few seconds to process
- Consider splitting very large datasets for analysis

## 📞 Support

For issues or enhancements, see the [README.md](README.md) for full documentation.

---
**Neural Harmonics Lab** • Python implementation based on original Go code by [ucukertz](https://github.com/ucukertz)

