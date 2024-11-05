import os
import calendar
import pandas as pd
import matplotlib.pyplot as plt


def load_data(config):
    """Load and preprocess CSV data, filtering rows with non-negative expenditures."""
    data = pd.read_csv(os.path.join(config['DATA_DIR'], config['DATA_FILENAME']),
                       skiprows=config['N_SKIPROWS'], delimiter=config['CSV_DELIMITER'])
    
    # Parse date and expenditure columns
    data[config['DATE_COLUMN']] = pd.to_datetime(data[config['DATE_COLUMN']], dayfirst=True)
    data[config['EXPENDITURE_COLUMN']] = data[config['EXPENDITURE_COLUMN']].replace(',', '.', regex=True)
    
    # Filter out rows where the expenditure column does not start with a minus sign (income data)
    data = data[data[config['EXPENDITURE_COLUMN']].str.startswith('-')]

    # Convert expenditure column to a positive float for analysis
    data[config['EXPENDITURE_COLUMN']] = data[config['EXPENDITURE_COLUMN']].astype(float).abs()
    
    return data


def calculate_total_expenditure(data, config):
    """Calculate total expenditure."""
    return data[config['EXPENDITURE_COLUMN']].sum()

def calculate_average_expenditure(total, days_range):
    """Calculate average expenditure per day."""
    return total / days_range

def get_date_range(data, config):
    """Get min and max dates from the data."""
    return data[config['DATE_COLUMN']].min(), data[config['DATE_COLUMN']].max()

def generate_monthly_summary(data, config):
    """Generate monthly summary with total expenditure and average daily expenditure."""
    # Extract the month from the date column
    data['Month'] = data[config['DATE_COLUMN']].dt.to_period('M')
    
    # Calculate the total expenditure for each month
    monthly_expenditure = data.groupby('Month')[config['EXPENDITURE_COLUMN']].sum().reset_index()
    monthly_expenditure.columns = ['Month', 'Total Expenditure']
    
    # Calculate the number of days in each month
    monthly_expenditure['Days in Month'] = monthly_expenditure['Month'].apply(
        lambda x: calendar.monthrange(x.year, x.month)[1]
    )
    
    # Calculate the average daily expenditure by dividing total by the number of days
    monthly_expenditure['Average Daily Expenditure'] = (
        monthly_expenditure['Total Expenditure'] / monthly_expenditure['Days in Month']
    ).round(2)
    
    # Drop the 'Days in Month' column if it’s not needed in the output
    monthly_expenditure = monthly_expenditure.drop(columns=['Days in Month'])
    
    return monthly_expenditure

def plot_bar_chart(data, x_col, y_col, title, ylabel, filename):
    """Plot and save a bar chart with an average line."""
    avg_value = data[y_col].mean()
    
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
