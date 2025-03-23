# Import packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset for the 48 portfolios from the Kenneth R. French data library for monthly value-weighted returns
# Load the dataset for the 48 portfolios, but only the relevant rows
data_value = pd.read_csv('Portfolios_C.csv', skiprows=11, nrows=1182)  # Adjust nrows as needed

# Convert the 'Unnamed: 0' column to numeric first to handle any spaces
data_value['Unnamed: 0'] = pd.to_numeric(data_value['Unnamed: 0'])

# Now convert to datetime
data_value['Date'] = pd.to_datetime(data_value['Unnamed: 0'].astype(str), format='%Y%m')

# Set Date as index
data_value = data_value.set_index('Date')

# Drop the original 'Unnamed: 0' column
data_value = data_value.drop('Unnamed: 0', axis=1)


# Load the dataset for the 48 portfolios from the Kenneth R. French data library for montlhy equal-weighted returns
# Load the dataset for the 48 portfolios, but only the relevant rows between 1197 and 3850
data_equal = pd.read_csv('Portfolios_C.csv', skiprows=1197)

# Stop at 1182 rows to match the value-weighted dataset
data_equal = data_equal.iloc[:1182]

# Convert the 'Unnamed: 0' column to numeric first to handle any spaces
data_equal['Unnamed: 0'] = pd.to_numeric(data_equal['Unnamed: 0'])

# Now convert to datetime
data_equal['Date'] = pd.to_datetime(data_equal['Unnamed: 0'].astype(str), format='%Y%m')

# Set Date as index
data_equal = data_equal.set_index('Date')

# Drop the original 'Unnamed: 0' column
data_equal = data_equal.drop('Unnamed: 0', axis=1)


# Load the dataset for the 48 portfolios from the Kenneth R. French data library for the number of firms
# Load the dataset for the 48 portfolios, but only the relevant rows between 2587 and 3770
data_firms = pd.read_csv('Portfolios_C.csv', skiprows=2587)

# Stop at 1182 rows 
data_firms = data_firms.iloc[:1182]

# Convert the 'Unnamed: 0' column to numeric first to handle any spaces
data_firms['Unnamed: 0'] = pd.to_numeric(data_firms['Unnamed: 0'])

# Now convert to datetime
data_firms['Date'] = pd.to_datetime(data_firms['Unnamed: 0'].astype(str), format='%Y%m')

# Set Date as index
data_firms = data_firms.set_index('Date')

# Drop the original 'Unnamed: 0' column
data_firms = data_firms.drop('Unnamed: 0', axis=1)


# Load the dataset for the 48 portfolios from the Kenneth R. French data library for the average firm size
# Load the dataset for the 48 portfolios, but only the relevant rows between 3773 and 5059
data_size = pd.read_csv('Portfolios_C.csv', skiprows=3773)

# Stop at 1282 rows
data_size = data_size.iloc[:1182]

# Convert the 'Unnamed: 0' column to numeric first to handle any spaces
data_size['Unnamed: 0'] = pd.to_numeric(data_size['Unnamed: 0'])

# Now convert to datetime
data_size['Date'] = pd.to_datetime(data_size['Unnamed: 0'].astype(str), format='%Y%m')

# Set Date as index
data_size = data_size.set_index('Date')

# Drop the original 'Unnamed: 0' column
data_size = data_size.drop('Unnamed: 0', axis=1)


# Load the dataset for the 48 portfolios from the Kenneth R. French data library for the sum of BE / sum of ME
# Load the dataset for the 48 portfolios, but only the relevant rows between 4959 and 5059
data_ratios = pd.read_csv('Portfolios_C.csv', skiprows=4959)

# Stop at 99
data_ratios = data_ratios.iloc[:99]

# Convert the 'Unnamed: 0' column to numeric first to handle any spaces
data_ratios['Unnamed: 0'] = pd.to_numeric(data_ratios['Unnamed: 0'])

# Store the original annual data
annual_ratios = data_ratios.copy()

# Create a list to store monthly data
monthly_data = []

# Convert annual ratio data to monthly data (July year s to June year s+1)
for idx, row in annual_ratios.iterrows():
    year = int(row['Unnamed: 0'])
    
    # For each year, create 12 monthly entries (July to June next year)
    for month_offset in range(12):
        # Calculate the month and year
        month = 7 + month_offset  # Start from July (7)
        curr_year = year
        
        # Adjust the year if month > 12 (January to June of next year)
        if month > 12:
            month = month - 12
            curr_year = year + 1
            
        # Create date string in YYYYMM format for the index
        date_str = f"{curr_year}{month:02d}"
        month_year = pd.to_datetime(date_str, format='%Y%m')
        
        # Create a row for this month with all the ratios from the annual data
        monthly_row = row.drop('Unnamed: 0').copy()
        monthly_data.append((month_year, *monthly_row))

# Create DataFrame from the monthly data
columns = ['Date'] + list(annual_ratios.columns.drop('Unnamed: 0'))
monthly_ratios = pd.DataFrame(monthly_data, columns=columns)

# Set Date as index
monthly_ratios = monthly_ratios.set_index('Date')

# Sort the index to ensure chronological order
monthly_ratios = monthly_ratios.sort_index()


# Print all the dataframes to check if they are loaded correctly
print("Value-weighted returns:")
print(data_value.head())
print("\nEqual-weighted returns:")
print(data_equal.head())
print("\nNumber of firms:")
print(data_firms.head())
print("\nAverage firm size:")
print(data_size.head())
print("\nSum of BE / sum of ME (monthly):")
print(monthly_ratios.head())
