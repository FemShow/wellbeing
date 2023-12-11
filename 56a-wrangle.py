import pandas as pd

# Read the Excel file into a DataFrame, skipping the first 3 rows and reading the first 15 rows
df = pd.read_excel("/Users/femisokoya/Documents/GitHub/wellbeing/ukmeasuresofnationalwellbeingnov2023.xlsx",
                   sheet_name='5.6_Feeling_safe',
                   skiprows=18,
                   nrows=34)

# Rename the column header for column 0 to 'Safe-walking'
df.rename(columns={df.columns[0]: 'Safe-walking'}, inplace=True)

# Remove the suffix '[L]' from values in the 'Safe-walking' column
df['Safe-walking'] = df['Safe-walking'].str.replace(r'\[L\]', '', regex=True)

df.drop(df.index[11:14], inplace=True)
df.reset_index(drop=True, inplace=True)


# Iterate through all columns in the DataFrame
for col in df.columns:
    # Find rows containing [x] in the current column
    mask = df[col].astype(str).str.contains(r'\[x\]', na=False)

    # Skip columns that are not in the specified list
    if col not in ['Male %', 'Male LCL %', 'Male UCL %', 'Male sample size', 'Female %', 'Female LCL %', 'Female UCL %', 'Female sample size']:
        continue

    # Drop the % suffix in the current column name
    new_column_name = col.replace('%', '_')

    # Replace spaces with underscores
    new_column_name = new_column_name.replace(' ', '_')
    
    # Create a new column name for the presence of [x]
    new_col_name = new_column_name + '_obsStatus'

    # Find the index of the current column
    col_index = df.columns.get_loc(col)

    # Insert a new column immediately after the current column
    df.insert(col_index + 1, new_col_name, '')

    # Update the new column with 'x' where [x] is found on the same row
    df.loc[mask, new_col_name] = 'x'
    
    # Replace [x] with an empty string only where [x] is found, else keep the original value
    df[col] = df.apply(lambda x: '' if '[x]' in str(x[col]) else x[col], axis=1)

    # Convert the current column to numeric values with one decimal place, handling non-numeric values
    df[col] = pd.to_numeric(df[col], errors='coerce').round(1)

# Ensure there are no non-finite values in the 'Male sample size' and 'Female sample size' columns
df['Male sample size'] = pd.to_numeric(df['Male sample size'], errors='coerce')
df['Female sample size'] = pd.to_numeric(df['Female sample size'], errors='coerce')

# Fill or remove non-integer and missing values
df['Male sample size'] = df['Male sample size'].fillna(0).astype(int)
df['Female sample size'] = df['Female sample size'].fillna(0).astype(int)

# Replace zeroes with empty strings
df = df.replace(0, '')

# Example dictionary for column name mapping
column_name_mapping = {
    'Male %': 'Male',
    'Male___obsStatus': 'Male_obsStatus',
    'Male LCL %': 'Male_LCL',
    'Male_LCL___obsStatus': 'M_LCL_obsStatus',
    'Male UCL %': 'Male_UCL',
    'Male_UCL___obsStatus': 'M_UCL_obsStatus',
    'Male sample size': 'M_sample_size',
    'Male_sample_size_obsStatus': 'M_s_s_obsStatus',
    'Female %': 'Female',
    'Female___obsStatus': 'F_obsStatus',
    'Female LCL %': 'F_LCL',
    'Female_LCL___obsStatus': 'F_LCL_obsStatus',
    'Female UCL %': 'Female_UCL',
    'Female_UCL___obsStatus': 'F_UCL_obsStatus',
    'Female sample size': 'F_sample_size',
    'Female_sample_size_obsStatus': 'F_s_s_obsStatus'
}

# Rename columns using the dictionary
df.rename(columns=column_name_mapping, inplace=True)

# Remove leading and trailing spaces from all string columns
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Replace missing values in the DataFrame with a default value (e.g., "")
df.fillna("", inplace=True)

# Remove columns with all NaN values from df
df.dropna(axis=1, how='all', inplace=True)

# Now, columns with all NaN values have been removed from df

# Assuming df is your DataFrame
df.dropna(axis=0, how='all', inplace=True)

# Managing missing values
df.fillna(value='', inplace=True)

# Display the resulting DataFrame
print(df)

# Save the modified DataFrame to a CSV file
df.to_csv('/Users/femisokoya/Documents/GitHub/wellbeing/results.csv', index=False)
