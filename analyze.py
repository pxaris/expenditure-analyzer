import os
import pandas as pd
import matplotlib.pyplot as plt
from config import DATA_DIR, FILENAME, N_SKIPROWS, REPORT_DIR

def load_data():
    """Load and preprocess CSV data."""
    data = pd.read_csv(os.path.join(DATA_DIR, FILENAME), skiprows=N_SKIPROWS, delimiter=';')
    data['Ημ/νία συναλλαγής'] = pd.to_datetime(data['Ημ/νία συναλλαγής'], dayfirst=True)
    data['Ποσό (EUR)'] = data['Ποσό (EUR)'].replace(',', '.', regex=True).replace('-', '').astype(float).abs()
    return data

def calculate_total_expenditure(data):
    """Calculate total expenditure."""
    return data['Ποσό (EUR)'].sum()

def calculate_average_expenditure(total, days_range):
    """Calculate average expenditure per day."""
    return total / days_range

def get_date_range(data):
    """Get min and max dates from the data."""
    return data['Ημ/νία συναλλαγής'].min(), data['Ημ/νία συναλλαγής'].max()

def generate_monthly_summary(data):
    """Generate monthly summary with total and average expenditure."""
    data['Month'] = data['Ημ/νία συναλλαγής'].dt.to_period('M')
    monthly_expenditure = data.groupby('Month')['Ποσό (EUR)'].agg(['sum', 'mean']).reset_index()
    monthly_expenditure.columns = ['Month', 'Total Expenditure', 'Average Expenditure']
    return monthly_expenditure.round(2)

def plot_bar_chart(data, x_col, y_col, title, ylabel, filename):
    """Plot and save a bar chart."""
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_col].values, data[y_col].values, color='skyblue', width=16.2)
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def plot_pie_chart(data, title, filename):
    """Plot and save a pie chart."""
    plt.figure(figsize=(10, 8))
    plt.pie(data['Total Expenditure'], labels=data['Category'], autopct='%1.1f%%', startangle=140)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.title(title)
    plt.savefig(filename)
    plt.show()

def generate_report():
    """Main function to generate the expenditure report and charts."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, 'report.txt')
    data = load_data()
    min_date, max_date = get_date_range(data)
    days_range = (max_date - min_date).days + 1
    total_expenditure = calculate_total_expenditure(data)
    average_expenditure_per_day = calculate_average_expenditure(total_expenditure, days_range)
    monthly_summary = generate_monthly_summary(data)
    monthly_summary['Month'] = monthly_summary['Month'].dt.to_timestamp()

    plot_bar_chart(
        monthly_summary, 'Month', 'Total Expenditure',
        'Total Monthly Expenditure', 'Total Expenditure (EUR)',
        os.path.join(REPORT_DIR, 'monthly_expenditure_total.png')
    )
    plot_bar_chart(
        monthly_summary, 'Month', 'Average Expenditure',
        'Average Monthly Expenditure', 'Average Expenditure (EUR)',
        os.path.join(REPORT_DIR, 'monthly_expenditure_average.png')
    )
    
    # Expenditure per category for entire date range
    category_expenditure = data.groupby('Κατηγορία δαπάνης')['Ποσό (EUR)'].sum().reset_index()
    category_expenditure.columns = ['Category', 'Total Expenditure']
    plot_pie_chart(
        category_expenditure,
        f"Date Range: {min_date.date()} to {max_date.date()}, Total Expenditure: €{round(total_expenditure, 2)}",
        os.path.join(REPORT_DIR, 'expenditure_per_category.png')
    )

    # Last three months and last month category pie charts
    for period, offset, filename_suffix in [
        ("Last 3 Months", pd.DateOffset(months=3), 'last_three_months'),
        ("Last Month", pd.DateOffset(months=1), 'last_month')
    ]:
        recent_data = data[data['Ημ/νία συναλλαγής'] >= max_date - offset]
        recent_category_expenditure = recent_data.groupby('Κατηγορία δαπάνης')['Ποσό (EUR)'].sum().reset_index()
        recent_category_expenditure.columns = ['Category', 'Total Expenditure']
        recent_total_expenditure = recent_category_expenditure['Total Expenditure'].sum()
        
        plot_pie_chart(
            recent_category_expenditure,
            f"{period}: {(max_date - offset).date()} to {max_date.date()}, Total Expenditure: €{round(recent_total_expenditure, 2)}",
            os.path.join(REPORT_DIR, f'expenditure_per_category_{filename_suffix}.png')
        )
    
    # write report to file
    with open(report_path, 'w') as report_file:
        print(f"Report Date Range: {min_date.date()} to {max_date.date()}", file=report_file)
        print("=" * 50, file=report_file)
        print("Total Expenditure:", round(total_expenditure, 2), file=report_file)
        print("Average Expenditure per Day:", round(average_expenditure_per_day, 2), file=report_file)
        print("Number of Days (from min to max date):", days_range, file=report_file)
        print("\nMonthly Expenditure:\n", monthly_summary, file=report_file)
        print("\nExpenditure per Category:\n", category_expenditure, file=report_file)

    print(f"Report saved to {report_path}")
    print(f"Figures saved in {REPORT_DIR}")

if __name__ == '__main__':
    generate_report()
