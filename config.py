import os

# directory paths
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
REPORT_DIR = os.path.join(ROOT_DIR, 'report')

# data specific information
DATA_FILENAME = 'sample_data.csv'
N_SKIPROWS = 6  # rows of the CSV file to skip
CSV_DELIMITER = ';'
DATE_COLUMN = 'Ημ/νία συναλλαγής'
EXPENDITURE_COLUMN = 'Ποσό (EUR)'
EXPENDITURE_CATEGORY_COLUMN = 'Κατηγορία δαπάνης'
CURRENCY = '€'

# reporting information
DATE_FORMAT = '%d/%m/%Y'
OUTPUT_FILENAME = 'report.txt'

