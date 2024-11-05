import os
import argparse
import pandas as pd
from config import CONFIG
from utils import (
    load_data, calculate_total_expenditure, calculate_average_expenditure,
    get_date_range, generate_monthly_summary, plot_bar_chart, plot_pie_chart
)


def parse_args():
    """Parse command-line arguments to override main config values."""
    parser = argparse.ArgumentParser(description="Analyze expenditure data and generate reports.")

    # Add arguments for main configuration overrides
    parser.add_argument('--data_filename', type=str, default=CONFIG['DATA_FILENAME'],
                        help='Name of the CSV file containing transaction data.')
    parser.add_argument('--report_dir', type=str, default=CONFIG['REPORT_DIR'],
                        help='Directory to save report and figures.')

    args = parser.parse_args()

    # Update CONFIG dictionary with parsed arguments
    CONFIG.update({
        'DATA_FILENAME': args.data_filename,
        'REPORT_DIR': args.report_dir,
    })


def generate_report():
    os.makedirs(CONFIG['REPORT_DIR'], exist_ok=True)
    report_path = os.path.join(CONFIG['REPORT_DIR'], CONFIG['OUTPUT_FILENAME'])
    data = load_data(CONFIG)
    min_date, max_date = get_date_range(data, CONFIG)
    days_range = (max_date - min_date).days + 1
    total_expenditure = calculate_total_expenditure(data, CONFIG)
    average_expenditure_per_day = calculate_average_expenditure(total_expenditure, days_range)
    monthly_summary = generate_monthly_summary(data, CONFIG)
    monthly_summary['Month'] = monthly_summary['Month'].dt.to_timestamp()

    formatted_min_date = min_date.strftime(CONFIG['DATE_FORMAT'])
    formatted_max_date = max_date.strftime(CONFIG['DATE_FORMAT'])

    plot_bar_chart(
        monthly_summary, 'Month', 'Total Expenditure',
        f'Total Monthly Expenditure ({formatted_min_date} to {formatted_max_date})', 
        f'Total Expenditure ({CONFIG["CURRENCY"]})',
        os.path.join(CONFIG['REPORT_DIR'], 'monthly_expenditure_total.png')
    )
    plot_bar_chart(
        monthly_summary, 'Month', 'Average Daily Expenditure',
        f'Average Daily Expenditure ({formatted_min_date} to {formatted_max_date})', 
        f'Average Expenditure ({CONFIG["CURRENCY"]})',
        os.path.join(CONFIG['REPORT_DIR'], 'monthly_expenditure_average.png')
    )

    # Expenditure per category for entire date range
    category_expenditure = data.groupby(CONFIG['EXPENDITURE_CATEGORY_COLUMN'])[
        CONFIG['EXPENDITURE_COLUMN']].sum().reset_index()
    category_expenditure.columns = ['Category', 'Total Expenditure']
    plot_pie_chart(
        category_expenditure,
        f"Date Range: {formatted_min_date} to {formatted_max_date}\nTotal Expenditure: {CONFIG['CURRENCY']}{round(total_expenditure, 2)}",
        os.path.join(CONFIG['REPORT_DIR'], 'expenditure_per_category.png')
    )

    # Last three months and last month category pie charts
    for period, offset, filename_suffix in [
        ("Last 3 Months", pd.DateOffset(months=3), 'last_three_months'),
        ("Last Month", pd.DateOffset(months=1), 'last_month')
    ]:
        recent_data = data[data[CONFIG['DATE_COLUMN']] >= max_date - offset]
        recent_category_expenditure = recent_data.groupby(CONFIG['EXPENDITURE_CATEGORY_COLUMN'])[
            CONFIG['EXPENDITURE_COLUMN']].sum().reset_index()
        recent_category_expenditure.columns = ['Category', 'Total Expenditure']
        recent_total_expenditure = recent_category_expenditure['Total Expenditure'].sum()

        plot_pie_chart(
            recent_category_expenditure,
            f"{period}: {(max_date - offset).strftime(CONFIG['DATE_FORMAT'])} to {formatted_max_date}\nTotal Expenditure: {CONFIG['CURRENCY']}{round(recent_total_expenditure, 2)}",
            os.path.join(
                CONFIG['REPORT_DIR'], f'expenditure_per_category_{filename_suffix}.png')
        )

    # write report to file
    with open(report_path, 'w') as report_file:
        print(
            f"Report Date Range: {formatted_min_date} to {formatted_max_date}", file=report_file)
        print("=" * 50, file=report_file)
        print("Total Expenditure:", round(
            total_expenditure, 2), file=report_file)
        print("Average Expenditure per Day:", round(
            average_expenditure_per_day, 2), file=report_file)
        print("Number of Days (from min to max date):",
              days_range, file=report_file)
        print("\nMonthly Expenditure:\n", monthly_summary, file=report_file)
        print("\nExpenditure per Category:\n",
              category_expenditure, file=report_file)

    print(f"Report saved to {report_path}")
    print(f"Figures saved in {CONFIG['REPORT_DIR']}")


if __name__ == '__main__':
    parse_args()
    generate_report()
