# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 18:35:08 2023

@author: Joaquin
"""

from selenium import webdriver
import time
import os
import datetime
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



##############################################################################
###############                   Inputs                       ###############
##############################################################################
wd = r'C:/Users/Joaquin/Desktop/DNIs/'
inputs = rf'{wd}Inputs/'
outputs = rf'{wd}Outputs/' 
dnis_file_name = r'DNIs.csv'
path_to_chromedriver = r'C:/Program Files/chromedriver.exe'
number_remaining = 1
dni_column_name = 'DNI'


##############################################################################
###############            Less needed to edit inputs          ###############
##############################################################################

# Last digit of CUIL
cuil_last_digits = range(0,10,1)

# First two digits of CUIL
cuil_first_digits = (20,27,23,24)

#Path to csv with IDs
path_to_dni = rf'{inputs}{dnis_file_name}'

#Dates (today and 6 month ago)
#TODAY
end_month =datetime.date.today().strftime("%m")
end_year =datetime.date.today().strftime("%Y")
#SIX MONTH AGO
# Calculate the date from 3 months ago
six_months_ago = datetime.date.today() - datetime.timedelta(days=6*30)
# Get the month and year from 3 months ago
initial_month = six_months_ago.strftime("%m")
initial_year = six_months_ago.strftime("%Y")



##############################################################################
###############                   Code                       ###############
##############################################################################

#options = Options()
#options.add_argument("--headless")
service = Service(executable_path= path_to_chromedriver)
options = webdriver.ChromeOptions()
driver =  webdriver.Chrome(service=service, options=options ) #Execute driver

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
    
#Keep the remaining not scrapped
df_whole = pd.read_csv(path_to_dni)#.head(3)
df_whole = df_whole.rename(columns={dni_column_name: 'DNI'})
# Convert the unique numeric values from "dni" column in df_full to strings
dni_full_values = df_full['dni'].astype(str).unique()
# Filter the rows in df_whole based on the condition: DNI value is not in df_full
df = df_whole[~df_whole['DNI'].astype(str).isin(dni_full_values)]



for doc in df['DNI']:
        indice = df.loc[df['DNI'] == doc].index + 1
        print('Searching CUIL of DNI', doc,'.')
        #Generate variable to loop
        cuit_correcto = False
        # Loop until cuit_correcto becomes True or any other exit condition
        while not cuit_correcto:
            for pre in cuil_first_digits:
                if cuit_correcto == True:
                    break
                else:
                    pass
                for fin in cuil_last_digits:
                    driver.get("https://servicioswww.anses.gob.ar/censite/index.aspx")
                    time.sleep(1)
                    driver.find_element('id',"txtCuitPre").send_keys(str(pre))
                    driver.find_element('id',"txtCuitDoc").send_keys(str(doc))
                    driver.find_element('id',"txtCuitDV").send_keys(str(fin))
                    driver.find_element('id',"txtDesdeMes").send_keys(str(initial_month))
                    driver.find_element('id',"txtDesdeAnio").send_keys(str(initial_year))
                    driver.find_element('id',"txtHastaMes").send_keys(str(end_month))
                    driver.find_element('id',"txtHastaAnio").send_keys(str(end_year))
                    
                    
                    
                    driver.find_element('id',"btnVerificar").click()
                    time.sleep(1)
                    # Check if the element is present in the HTML
                    if "Se ha producido un error en la aplicaci" in driver.page_source or "Acceso denegado"  in driver.page_source:
                        pass
                    else:
                        if"CUIT incorrecto."  not in driver.page_source:
                            cuit_correcto = True
                            break
                        else: pass
            print('Finded CUIL for', doc,', it is ', pre,doc,fin )
            t1 = driver.find_element('id','lblNombre')
            nom = t1.text
            t2 = driver.find_element('id','lblCuil')
            cuil = t2.text
            t3 = driver.find_element('xpath', "//td[@class='fa fa-check fa-5x']")
            cert = t3.text
            t4 = driver.find_element('id',"ANTECEDENTES")
            obs = t4.text
            t5 = driver.find_element('id','lblDocumento')
            dni = t5.text    
            line = [[nom,cuil,dni,cert,obs]]
            line_df = pd.DataFrame(line, columns=['nom', 'cuil', 'dni', 'cert', 'obs'])
            data = data.append(line_df, ignore_index=True)
            time.sleep(0.5)
                    
    
    
    
# Create a new column 'certificacion' based on 'cert' column
data['certificacion'] = data['cert'].map({'No es posible emitir la Certificación': 0,
                                             'Es posible emitir la Certificación': 1})
    
# ADD column for info.

# Update 'obrasocial' column based on conditions
data.loc[data['certificacion'] == 0, 'obrasocial'] = data['obs'].str.contains('Obra Social', case=False).astype(int)
 
# Update 'trabajadorenactividad' column based on conditions
data.loc[data['certificacion'] == 0, 'trabajadorenactividad'] = data['obs'].str.contains('Declaraciones Juradas como Trabajador en Actividad', case=False).astype(int)
   
# Update 'asignacionesfamiliares' column based on conditions
data.loc[data['certificacion'] == 0, 'asignacionesfamiliares'] = data['obs'].str.contains('Asignaciones Familiares', case=False).astype(int)
  
# Update 'ddjjprovnocipa' column based on conditions
data.loc[data['certificacion'] == 0, 'ddjjprovnocipa'] = data['obs'].str.contains('Declaraciones Juradas de Provincia no adherida al SIPA', case=False).astype(int)
    
# Update 'autonomomonotributista' column based on conditions
data.loc[data['certificacion'] == 0, 'autonomomonotributista'] = data['obs'].str.contains('Autónomo o Monotributista', case=False).astype(int)
  
# Update 'casaparticular' column based on conditions
data.loc[data['certificacion'] == 0, 'casaparticular'] = data['obs'].str.contains('Trabajador/a de Casas Particulares', case=False).astype(int)
    
# Update 'casaparticularmaternidad' column based on conditions
data.loc[data['certificacion'] == 0, 'casaparticularmaternidad'] = data['obs'].str.contains('Asignación por Maternidad para Trabajadora de Casas Particulares', case=False).astype(int)
    
# Update 'prestaciondesempleo' column based on conditions
data.loc[data['certificacion'] == 0, 'prestaciondesempleo'] = data['obs'].str.contains('Prestación por Desempleo', case=False).astype(int)
    
# Update 'plansocial' column based on conditions
data.loc[data['certificacion'] == 0, 'plansocial'] = data['obs'].str.contains('Plan Social, Ingreso Familiar de Emergencia o Programa de Empleo', case=False).astype(int)
    
# Update 'prestacionprevisional' column based on conditions
data.loc[data['certificacion'] == 0, 'prestacionprevisional'] = data['obs'].str.contains('Prestación Previsional.', case=False).astype(int)
   
# Update 'prestacionprevisionalnosipa' column based on conditions
data.loc[data['certificacion'] == 0, 'prestacionprevisionalnosipa'] = data['obs'].str.contains('Prestación Previsional de Provincia no adherida al SIPA', case=False).astype(int)
    
# Update 'iniciacionprevisional' column based on conditions
data.loc[data['certificacion'] == 0, 'iniciacionprevisional'] = data['obs'].str.contains('Iniciación de Prestación Previsional Nacional', case=False).astype(int)
    
# Update 'asignacionmadres' column based on conditions
data.loc[data['certificacion'] == 0, 'asignacionmadres'] = data['obs'].str.contains('Asignación Familiar Jubilados y Pensionados - Madre', case=False).astype(int)
    
# Update 'PROGRESAR' column based on conditions
data.loc[data['certificacion'] == 0, 'PROGRESAR'] = data['obs'].str.contains('PROG.R.ES.AR', case=False).astype(int)
    
# Update 'monotributistasocial' column based on conditions
data.loc[data['certificacion'] == 0, 'monotributistasocial'] = data['obs'].str.contains('Ministerio de Desarrollo Social como Monotributista Social', case=False).astype(int)
   
# Update 'pensionnocontributiva' column based on conditions
data.loc[data['certificacion'] == 0, 'pensionnocontributiva'] = data['obs'].str.contains('Registra Pensión NO Contributiva otorgada por el Ministerio de Desarrollo Social', case=False).astype(int)
   
# Update 'iniciacionpensionnocontributiva' column based on conditions
data.loc[data['certificacion'] == 0, 'iniciacionpensionnocontributiva'] = data['obs'].str.contains('Registra Iniciación de Pensión NO Contributiva otorgada por el Ministerio de Desarrollo Social', case=False).astype(int)
    
# Update 'AUHembarazo' column based on conditions
data.loc[data['certificacion'] == 0, 'auhembarazo'] = data['obs'].str.contains('Asignación Universal por Hijo', case=False).astype(int)
   
# Set all columns' values to 0 if 'certificacion' == 1
columns_to_reset = ['obrasocial', 'trabajadorenactividad', 'asignacionesfamiliares', 'ddjjprovnocipa',
                    'autonomomonotributista', 'casaparticular', 'casaparticularmaternidad', 'prestaciondesempleo',
                    'plansocial', 'prestacionprevisional', 'prestacionprevisionalnosipa', 'iniciacionprevisional',
                    'asignacionmadres', 'PROGRESAR', 'monotributistasocial', 'pensionnocontributiva',
                    'iniciacionpensionnocontributiva', 'auhembarazo']

data.loc[data['certificacion'] == 1, columns_to_reset] = 0
    
# Generate the file name
file_name = f"{outputs}chunks/chunk_remaining_{number_remaining}.csv"
    
# Save the chunk data as CSV
#data = data.astype(str)
data.to_csv(file_name, index=False, sep=';')
    
    
