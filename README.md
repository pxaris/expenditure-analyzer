
# Expenditure Data Analysis

This repository provides a set of scripts and configurations to analyze expenditure data. The main goal of the analysis is to generate reports and visualizations for financial transactions over time, categorized by various types of expenditures. After running the analysis, a summary report and visualizations are saved for easy interpretation of the data.

## Requirements

To get started, install the required Python packages. It's recommended to use a virtual environment.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pxaris/expenditure-analyzer.git
   cd expenditure-analyzer
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To analyze expenditure data, follow these steps:

### Step 1: Configure Variables

Open the `config.py` file and set the following configuration variables:

- `DATA_FILENAME`: Name of the CSV file containing transaction data, e.g., `'sample_data.csv'`.
- `N_SKIPROWS`: Number of rows to skip at the beginning of the CSV file, typically for headers or additional info, e.g., `6`.
- `DATE_COLUMN`: Name of the column in the CSV file containing transaction dates, e.g., `'Ημ/νία συναλλαγής'`.
- `EXPENDITURE_COLUMN`: Name of the column with expenditure amounts, e.g., `'Ποσό (EUR)'`.
- `EXPENDITURE_CATEGORY_COLUMN`: Name of the column categorizing expenditures, e.g., `'Κατηγορία δαπάνης'`.
- `CURRENCY`: Currency symbol to display in the report, e.g., `'€'`.

### Step 2: Run the Analysis

Execute the analysis script:

```bash
python analyze.py
```

This will process the input data, perform analysis, and generate reports and visualizations.

### Step 3: View the Results

After the analysis completes:

1. **Report**: Open the `report.txt` file located in the `report/` directory. This file contains a summary of the analyzed expenditure data, including total and average expenditures, breakdowns by category, and more.
   
2. **Figures**: Find the generated figures saved in the `report/` directory. These figures include bar charts of monthly expenditures and pie charts for expenditure breakdowns by category.

The analysis results offer a comprehensive overview of the expenditure trends, helping you better understand spending patterns over time.

---

## Additional Information

- **Sample Data**: A sample CSV file is included to demonstrate the format required for analysis. It follows the rationale of an exported data file from a Greek bank and the respective analysis can be found in the `sample_report/` directory.
- **Customization**: Modify `config.py` and adjust the `analyze.py` script as needed to fit different datasets or specific analysis requirements.

Enjoy analyzing your expenditure data!
