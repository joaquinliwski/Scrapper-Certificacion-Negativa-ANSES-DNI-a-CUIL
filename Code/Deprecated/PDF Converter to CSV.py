# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:53:45 2023

@author: Joaquin
"""

import PyPDF2
import pandas as pd

def extract_text_from_page(file_path, page_number):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[page_number - 1]
        return page.extract_text()

def extract_table_from_text(text):
    # Split the text by new lines to separate rows
    rows = text.split('\n')
    
    # Remove the first row
    rows = rows[1:]
    
    # Initialize the data list
    data = []
    
    # Iterate over each row
    for row in rows:
        # Split the row by the "DNI" keyword
        columns = row.split('DNI')
        
        # Clean up leading/trailing whitespaces and remove empty columns
        cleaned_columns = [col.strip() for col in columns if col.strip()]
        
        # Append the cleaned columns to the data list
        data.append(cleaned_columns)
    
    # Create a DataFrame from the data list
    df = pd.DataFrame(data, columns=['APELLIDO NOMBRE', 'DNI'])
    
    return df

#Set File Path
file_path = "C:/Users/Joaquin/Desktop/DNIs/listado_contratados_250319.pdf"

# Get the total number of pages in the PDF
with open(file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)

# Iterate over each page and extract the table
tables = []
for page_number in range(1, num_pages + 1):
    text = extract_text_from_page(file_path, page_number)
    table = extract_table_from_text(text)
    tables.append(table)

# Concatenate the tables from all pages into a single DataFrame
result = pd.concat(tables, ignore_index=True)

# Save the result as a CSV file
result.to_csv("C:/Users/Joaquin/Desktop/DNIs/DNIs.csv", index=False)


