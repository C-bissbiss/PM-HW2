# Import packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to load and process dataset sections
def load_dataset(skiprows, nrows=None, date_format='%Y%m', convert_annual=False):
    data = pd.read_csv('Portfolios_C.csv', skiprows=skiprows, nrows=nrows)
    data['Unnamed: 0'] = pd.to_numeric(data['Unnamed: 0'])
    
    if not convert_annual:
        # Standard monthly data processing
        data['Date'] = pd.to_datetime(data['Unnamed: 0'].astype(str), format=date_format)
        data = data.set_index('Date').drop('Unnamed: 0', axis=1)
        data = data.astype(float)
        data.replace([-99.99, -999], np.nan, inplace=True)
        return data
    else:
        # Annual to monthly conversion for ratios
        annual_data = data.copy()
        monthly_data = []
        
        for idx, row in annual_data.iterrows():
            year = int(row['Unnamed: 0'])
            for month_offset in range(12):
                month = 7 + month_offset
                curr_year = year if month <= 12 else year + 1
                if month > 12:
                    month -= 12
                
                date_str = f"{curr_year}{month:02d}"
                month_year = pd.to_datetime(date_str, format='%Y%m')
                monthly_row = row.drop('Unnamed: 0').copy()
                monthly_data.append((month_year, *monthly_row))
        
        columns = ['Date'] + list(annual_data.columns.drop('Unnamed: 0'))
        monthly_df = pd.DataFrame(monthly_data, columns=columns)
        monthly_df = monthly_df.set_index('Date').sort_index()
        monthly_df = monthly_df[monthly_df.index <= '2024-12-01']
        monthly_df = monthly_df.astype(float)
        monthly_df.replace([-99.99, -999], np.nan, inplace=True)
        return monthly_df

# Load all datasets 
data_value = load_dataset(skiprows=11, nrows=1182)
data_equal = load_dataset(skiprows=1197, nrows=1182)
data_firms = load_dataset(skiprows=2587, nrows=1182)
data_size = load_dataset(skiprows=3773, nrows=1182)
monthly_ratio = load_dataset(skiprows=4959, nrows=99, date_format='%Y', convert_annual=True)

# Load the risk-free rate data
data_rf = pd.read_csv('Factors_C.csv', skiprows=3, nrows=1182)

# Process the risk-free rate data
data_rf['Unnamed: 0'] = pd.to_numeric(data_rf['Unnamed: 0'])
data_rf['Date'] = pd.to_datetime(data_rf['Unnamed: 0'].astype(str), format='%Y%m')
data_rf = data_rf.set_index('Date').drop('Unnamed: 0', axis=1)
data_rf = data_rf.astype(float)

# Keep only the 'RF' and 'Date' columns
data_rf = data_rf[['RF']]

# Strip all spaces from column names in the datasets before merging
data_value.columns = data_value.columns.str.strip()
data_equal.columns = data_equal.columns.str.strip()
data_firms.columns = data_firms.columns.str.strip()
data_size.columns = data_size.columns.str.strip()
monthly_ratio.columns = monthly_ratio.columns.str.strip()
data_rf.columns = data_rf.columns.str.strip()

# Merge all datasets into a single DataFrame
data_combined = data_value.join(data_equal, lsuffix='_value', rsuffix='_equal')
data_combined = data_combined.join(data_firms, rsuffix='_firms')
data_combined = data_combined.join(data_size, rsuffix='_size')
data_combined = data_combined.join(monthly_ratio, rsuffix='_ratio')
data_combined = data_combined.join(data_rf, rsuffix='_rf')

