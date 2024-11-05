import os
import pandas as pd
import matplotlib.pyplot as plt
from config import DATA_DIR, REPORT_DIR, DATA_FILENAME, N_SKIPROWS, CSV_DELIMITER, DATE_COLUMN, EXPENDITURE_COLUMN, EXPENDITURE_CATEGORY_COLUMN, CURRENCY, DATE_FORMAT, OUTPUT_FILENAME


def load_data():
    """Load and preprocess CSV data."""
    data = pd.read_csv(os.path.join(DATA_DIR, DATA_FILENAME),
                       skiprows=N_SKIPROWS, delimiter=CSV_DELIMITER)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], dayfirst=True)
    data[EXPENDITURE_COLUMN] = data[EXPENDITURE_COLUMN].replace(
        ',', '.', regex=True).replace('-', '').astype(float).abs()
    return data


def calculate_total_expenditure(data):
    """Calculate total expenditure."""
    return data[EXPENDITURE_COLUMN].sum()


def calculate_average_expenditure(total, days_range):
    """Calculate average expenditure per day."""
    return total / days_range


def get_date_range(data):
    """Get min and max dates from the data."""
    return data[DATE_COLUMN].min(), data[DATE_COLUMN].max()


def generate_monthly_summary(data):
    """Generate monthly summary with total and average expenditure."""
    data['Month'] = data[DATE_COLUMN].dt.to_period('M')
    monthly_expenditure = data.groupby('Month')[EXPENDITURE_COLUMN].agg([
        'sum', 'mean']).reset_index()
    monthly_expenditure.columns = [
        'Month', 'Total Expenditure', 'Average Expenditure']
    return monthly_expenditure.round(2)


def plot_bar_chart(data, x_col, y_col, title, ylabel, filename):
    """Plot and save a bar chart with an average line."""
    avg_value = data[y_col].mean()  # Calculate the average value for the dashed line
    
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_col].values, data[y_col].values, color='skyblue' if 'Total' in y_col else 'lightgreen', width=16.2)
    plt.axhline(y=avg_value, color='r', linestyle='--', label=f'Average: {avg_value:.2f}')
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.yticks(list(plt.yticks()[0]) + [avg_value])  # Add average line value to y-ticks
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_pie_chart(data, title, filename):
    """Plot and save a pie chart."""
    plt.figure(figsize=(10, 8))
    plt.pie(data['Total Expenditure'], labels=data['Category'],
            autopct='%1.1f%%', startangle=140)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.title(title)
    plt.savefig(filename)
    plt.show()


def generate_report():
    """Main function to generate the expenditure report and charts."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, OUTPUT_FILENAME)
    data = load_data()
    min_date, max_date = get_date_range(data)
    days_range = (max_date - min_date).days + 1
    total_expenditure = calculate_total_expenditure(data)
    average_expenditure_per_day = calculate_average_expenditure(
        total_expenditure, days_range)
    monthly_summary = generate_monthly_summary(data)
    monthly_summary['Month'] = monthly_summary['Month'].dt.to_timestamp()

    # Format dates as 'dd-mm-yyyy'
    formatted_min_date = min_date.strftime(DATE_FORMAT)
    formatted_max_date = max_date.strftime(DATE_FORMAT)

    plot_bar_chart(
        monthly_summary, 'Month', 'Total Expenditure',
        f'Total Monthly Expenditure ({formatted_min_date} to {formatted_max_date})', f'Total Expenditure ({CURRENCY})',
        os.path.join(REPORT_DIR, 'monthly_expenditure_total.png')
    )
    plot_bar_chart(
        monthly_summary, 'Month', 'Average Expenditure',
        f'Average Daily Expenditure ({formatted_min_date} to {formatted_max_date})', f'Average Expenditure ({CURRENCY})',
        os.path.join(REPORT_DIR, 'monthly_expenditure_average.png')
    )

    # Expenditure per category for entire date range
    category_expenditure = data.groupby(EXPENDITURE_CATEGORY_COLUMN)[
        EXPENDITURE_COLUMN].sum().reset_index()
    category_expenditure.columns = ['Category', 'Total Expenditure']
    plot_pie_chart(
        category_expenditure,
        f"Date Range: {formatted_min_date} to {formatted_max_date}\nTotal Expenditure: {CURRENCY}{round(total_expenditure, 2)}",
        os.path.join(REPORT_DIR, 'expenditure_per_category.png')
    )

    # Last three months and last month category pie charts
    for period, offset, filename_suffix in [
        ("Last 3 Months", pd.DateOffset(months=3), 'last_three_months'),
        ("Last Month", pd.DateOffset(months=1), 'last_month')
    ]:
        recent_data = data[data[DATE_COLUMN] >= max_date - offset]
        recent_category_expenditure = recent_data.groupby(EXPENDITURE_CATEGORY_COLUMN)[
            EXPENDITURE_COLUMN].sum().reset_index()
        recent_category_expenditure.columns = ['Category', 'Total Expenditure']
        recent_total_expenditure = recent_category_expenditure['Total Expenditure'].sum(
        )

        plot_pie_chart(
            recent_category_expenditure,
            f"{period}: {(max_date - offset).strftime(DATE_FORMAT)} to {formatted_max_date}\nTotal Expenditure: {CURRENCY}{round(recent_total_expenditure, 2)}",
            os.path.join(
                REPORT_DIR, f'expenditure_per_category_{filename_suffix}.png')
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
    print(f"Figures saved in {REPORT_DIR}")


if __name__ == '__main__':
    generate_report()
