# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:20:56 2023

@author: Joaquin Liwski
"""
import CUILArg
import pandas as pd
import re
import os

# Inputs 
wd = r'C:/Users/Joaquin/Desktop/DNIs/'  # Cambiar por la carpeta en la cual esta todo.
dnis_file_name = r'DNIs'  # Cambiar por nombre del archivo que contiene los dnis/asegurarse que sea un csv
gender_column ='sexo'  # Nombre de la columna que contiene genero/sexo
dni_column = 'DNI'  # Nombre de la columna que contiene DNI
subfiles_number = 5 # En cuantos archivos distintos se va a guardar

# Inputs que no necesitan cambio 
inputs = rf'{wd}Inputs/'  # Path for input files
outputs = rf'{wd}Outputs/'  # Path for output files
df_name = f'{inputs}{dnis_file_name}.csv'  # No hace falta cambiar.


# Code
df = pd.read_csv(df_name)  # Read the input file into a DataFrame, only retrieve the first 10 rows
# Filter for elements in 'dni_column' that contain numeric values
numeric_filter = df[dni_column].apply(lambda x: bool(re.match('^\d+$', str(x))))
# Create a new DataFrame with the filtered rows
filtered_df = df[numeric_filter]

def generate_cuil(row):
    dni = str(row[dni_column])  # Retrieve the DNI value from the row and convert it to a string
    gender = str(row[gender_column])  # Retrieve the gender value from the row and convert it to a string
    cuil, pre, dni_number, post = CUILArg.get(dni, gender)  # Call the CUILArg.get() function with the DNI and gender values, assign the returned values to variables
    return pd.Series({'cuil': cuil, 'pre': pre, 'dni': dni_number, 'post': post})  # Create a pandas Series with the CUIL components as values

result_df = filtered_df.apply(generate_cuil, axis=1)  # Apply the generate_cuil function to each row of the DataFrame, resulting in a new DataFrame with CUIL components
merged_df = pd.concat([df, result_df], axis=1)  # Concatenate the original DataFrame and the CUIL components DataFrame along the columns
file_name = f"{inputs}DNICUILS.csv"  # Define the file name for the output file
merged_df=merged_df.dropna(subset=['DNI'])
merged_df.to_csv(file_name, index=False, sep=';')  # Save the merged DataFrame as a CSV file, using ';' as the separator and excluding the index column


# Determine the number of rows to be saved in each CSV file
rows_per_csv = len(merged_df) // subfiles_number


# Delete old CSV files if they exist
for i in range(1, subfiles_number + 1):
    file_path = f"{inputs}DNICUILS_{i}.csv"
    if os.path.exists(file_path):
        os.remove(file_path)

# Save the DataFrame into n CSV files
for i in range(1, subfiles_number + 1):
    start_index = (i - 1) * rows_per_csv
    end_index = start_index + rows_per_csv

    if i == subfiles_number:
        # For the last CSV, include any remaining rows
        df_part = merged_df.iloc[start_index:]
    else:
        df_part = merged_df.iloc[start_index:end_index]

    file_path = f"{inputs}DNICUILS_{i}.csv"
    df_part.to_csv(file_path, index=False)