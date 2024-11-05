
# Expenditure Data Analysis

This repository provides a set of scripts and configurations to analyze expenditure data. The main goal of the analysis is to generate reports and visualizations for financial transactions over time, categorized by various types of expenditures. After running the analysis, a summary report and visualizations are saved for easy interpretation of the data.

## Docker Installation and Usage

You can use Docker to run the analysis script without needing to install dependencies directly on your machine.

Clone the repository:
   ```bash
   git clone https://github.com/pxaris/expenditure-analyzer.git
   cd expenditure-analyzer
   ```

### Step 1: Build the Docker Image

In the root directory of this repository, build the Docker image:

```bash
docker build -t expenditure-analyzer .
```

### Step 2: Run the Analysis with Docker

To analyze expenditure data, run the following Docker command:
```bash
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/report:/app/report expenditure-analyzer --data_filename 'sample_data.csv'
```

This command:

- Mounts the `data` directory to `/app/data` in the container, so it can access the specified at `--data_filename` CSV file.
- Mounts the `report` directory to `/app/report` in the container, where it will save the generated reports and figures.

### Step 3: View the Results

The `report.txt` file and the figures can be found under the `report/` directory.

---

## Manual Installation and Usage

To get started, install the required Python packages. It's recommended to use a virtual environment.

### Requirements Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pxaris/expenditure-analyzer.git
   cd expenditure-analyzer
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

To analyze expenditure data, follow these steps:

#### Step 1: Configure Default Variables

Open the `config.py` file and set the following default configuration variables if needed:

- `DATA_FILENAME`: Name of the default CSV file containing transaction data, e.g., `'sample_data.csv'`.
- `N_SKIPROWS`: Number of rows to skip at the beginning of the CSV file, typically for headers or additional info, e.g., `6`.
- `CSV_DELIMITER`: The delimiter used in the CSV file, e.g., `';'`.
- `DATE_COLUMN`: Name of the column in the CSV file containing transaction dates, e.g., `'Ημ/νία συναλλαγής'`.
- `EXPENDITURE_COLUMN`: Name of the column with expenditure amounts, e.g., `'Ποσό (EUR)'`.
- `EXPENDITURE_CATEGORY_COLUMN`: Name of the column categorizing expenditures, e.g., `'Κατηγορία δαπάνης'`.
- `CURRENCY`: Currency symbol to display in the report, e.g., `'€'`.

#### Step 2: Run the Analysis

You can override the default `DATA_FILENAME` and `REPORT_DIR` values directly from the command line.

##### Basic Usage
To use the default values specified in `config.py`, simply run:
```bash
python analyze.py
```

##### Custom Usage
To specify a different data file or report directory, use the following arguments:
```bash
python analyze.py --data_filename 'custom_data.csv' --report_dir 'custom_report_dir'
```

This will process the specified input data, perform analysis, and generate reports and visualizations in the designated report directory.

#### Step 3: View the Results

After the analysis completes:

1. **Report**: Open the `report.txt` file located in the `report/` directory (or the directory specified in `--report_dir`). This file contains a summary of the analyzed expenditure data, including total and average expenditures, breakdowns by category, and more.
   
2. **Figures**: Find the generated figures saved in the `report/` directory (or the one specified in `--report_dir`). These figures include bar charts of monthly expenditures and pie charts for expenditure breakdowns by category.

The analysis results offer a comprehensive overview of the expenditure trends, helping you better understand spending patterns over time.

---

## Additional Information

- **Sample Data**: A sample CSV file is included to demonstrate the format required for analysis. It follows the rationale of an exported data file from a Greek bank and the respective analysis can be found in the `sample_report/` directory.
- **Customization**: Modify `config.py` and adjust the `analyze.py` and `utils.py` scripts as needed to fit different datasets or specific analysis requirements.

Enjoy analyzing your expenditure data!
