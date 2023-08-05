# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 18:19:27 2023

@author: Joaquin
"""

import pandas as pd
import numpy as np

# Read the CSV file
csv_file = 'C:/Users/Joaquin/Desktop/DNIs/Inputs/DNIs.csv'
df = pd.read_csv(csv_file)

# Generate random values for the 'genero' column
random_values = np.random.choice(['masculino', 'femenino'], size=len(df))

# Add the 'genero' column to the DataFrame
df['GENERO'] = random_values

# Save the modified DataFrame to a new CSV file
output_csv_file = 'C:/Users/Joaquin/Desktop/DNIs/Inputs/DNIs_with_genero.csv'
df.to_csv(output_csv_file, index=False)

print(f"CSV file with 'genero' column added: {output_csv_file}")
