# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 18:35:08 2023

@author: Joaquin
"""
import os
import pandas as pd


##############################################################################
###############                   Inputs                       ###############
##############################################################################
wd = r'C:/Users/Joaquin/Desktop/DNIs/'
inputs = rf'{wd}Inputs/'
outputs = rf'{wd}Outputs/' 
dnis_file_name = r'DNIs.csv'
path_to_chromedriver = r'C:/Program Files/chromedriver.exe'
number_remaining = 1

##############################################################################
###############                   Code                       ###############
##############################################################################
# Directory containing the CSV files
directory = f"{outputs}chunks"

# Initialize an empty dataframe
df_full = pd.DataFrame()

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        
        # Read the CSV file using ';' as the delimiter
        data = pd.read_csv(file_path, delimiter=';')
        
        # Append the data to the main dataframe
        df_full = df_full.append(data, ignore_index=True)

# Print the combined dataframe
print(df_full)

# Generate the file name
file_name = f"{outputs}/certificaciones.csv"
    
# Keep only unique rows based on the "dni" column
df_full_unique = df_full.drop_duplicates(subset='dni')

# Save the unique rows as CSV
df_full_unique.to_csv(file_name, index=False, sep=';')