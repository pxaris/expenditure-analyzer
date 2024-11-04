import os
import pandas as pd
import matplotlib.pyplot as plt
from config import DATA_DIR, FILENAME, N_SKIPROWS, REPORT_DIR


if __name__ == '__main__':
    # Load the CSV file with specific parameters
    data = pd.read_csv(os.path.join(DATA_DIR, FILENAME), skiprows=N_SKIPROWS, delimiter=';')
    
    # Convert date column to datetime format
    data['Ημ/νία συναλλαγής'] = pd.to_datetime(data['Ημ/νία συναλλαγής'], dayfirst=True)
    
    # Convert "Ποσό (EUR)" to numeric, handling commas and negative values, and take absolute values
    data['Ποσό (EUR)'] = data['Ποσό (EUR)'].replace(',', '.', regex=True).replace('-', '').astype(float).abs()

    # 1. Total expenditure
    total_expenditure = data['Ποσό (EUR)'].sum()
    print("Total Expenditure:", total_expenditure)

    # 2. Average expenditure per day
    min_date = data['Ημ/νία συναλλαγής'].min()
    max_date = data['Ημ/νία συναλλαγής'].max()
    days_range = (max_date - min_date).days + 1  # Include both min and max dates
    average_expenditure_per_day = total_expenditure / days_range
    print("Average Expenditure per Day:", average_expenditure_per_day)
    print("Number of Days (from min to max date):", days_range)

    # 3. Monthly total and average expenditure
    data['Month'] = data['Ημ/νία συναλλαγής'].dt.to_period('M')  # Extract month-year
    monthly_expenditure = data.groupby('Month')['Ποσό (EUR)'].agg(['sum', 'mean']).reset_index()
    monthly_expenditure.columns = ['Month', 'Total Expenditure', 'Average Expenditure']

    print("\nMonthly Expenditure:\n", monthly_expenditure)
    
    # Convert the 'Month' column to datetime for plotting
    monthly_expenditure['Month'] = monthly_expenditure['Month'].dt.to_timestamp()

    # 4. Visualization of monthly expenditure (Total Expenditure - Bar Chart)
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_expenditure['Month'].values, monthly_expenditure['Total Expenditure'].values, color='skyblue', width=16.2)
    plt.title('Total Monthly Expenditure')
    plt.xlabel('Month')
    plt.ylabel('Total Expenditure (EUR)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Visualization of monthly expenditure (Average Expenditure - Bar Chart)
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_expenditure['Month'].values, monthly_expenditure['Average Expenditure'].values, color='lightgreen', width=16.2)
    plt.title('Average Monthly Expenditure')
    plt.xlabel('Month')
    plt.ylabel('Average Expenditure (EUR)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # 5. Sum per category
    category_expenditure = data.groupby('Κατηγορία δαπάνης')['Ποσό (EUR)'].sum().reset_index()
    category_expenditure.columns = ['Category', 'Total Expenditure']

    print("\nExpenditure per Category:\n", category_expenditure)

    # 6. Pie chart of expenditures per category
    plt.figure(figsize=(8, 8))
    plt.pie(category_expenditure['Total Expenditure'], labels=category_expenditure['Category'], autopct='%1.1f%%')
    plt.title('Expenditure per Category')
    plt.show()
