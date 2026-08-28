# CSV Analyser

A Streamlit web app for quickly analyzing and visualizing any CSV file — no spreadsheet tool required.

## Overview
Upload a CSV and instantly get row/column counts, per-column data types and null counts, statistical summaries, and charts showing missing data, numeric distributions, and top categories in text columns.

## Tech Stack
- Python
<<<<<<< HEAD
- Streamlit
- pandas
- Matplotlib

## Features
- Drag-and-drop CSV upload (up to 200 MB), with friendly errors for unreadable or empty files
- Quick overview: total rows, total columns, total null values
- Per-column breakdown of data types and null counts
- Statistical summary (count, mean, min, max) for numeric columns
- Bar chart of null values per column
- Distribution charts for each numeric column
- Top 5 category breakdown for each text column
=======
- pandas 

## Features
- Load and parse CSV files
- Generate summary statistics (mean, count, min/max, etc.)
- Handle missing/invalid data
>>>>>>> 2135d8d9374140e8273f112f47c3b8e899f64bca

## How to Run
```bash
pip install -r requirements.txt
streamlit run csv_analyser.py
```

Then open the local URL Streamlit prints in your terminal, and upload a CSV file (or use the included `sample_data.csv`) to see the analysis.

## Screenshots
![Before upload](images/csv1.png)
![After upload](images/After%20upload.gif)

## Project Structure
```
csv_analyser/
├── csv_analyser.py
├── sample_data.csv
├── requirements.txt
└── README.md
```

## Author
Pranav K — [Pranav10261](https://github.com/Pranav10261)

