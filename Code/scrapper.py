# -*- coding: utf-8 -*-
"""
Created on Sun Jul  20 13:06:00 2023

@author: Joaquin Liwski
"""

from selenium import webdriver
import time
import os
import datetime
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.service import Service
import random


##############################################################################
###############                   Inputs                       ###############
##############################################################################
wd = r'C:/Users/Joaquin/Desktop/DNIs/'  # Carpeta principal
path_to_chromedriver = r'C:/Program Files/chromedriver.exe'  # Donde esta el chromedriver
chunk_size = 5 # Cuantos juntos scrapea antes de cerrar y volver a abrir el driver
dnis_file_name = r'DNICUILS.csv' # Como se llama el archivo con los DNIs
headless = False # True si no se quiere ver el driver, False si lo queremos ver.

# Estos inputs corresponden a los meses.
# Fecha elegida por quien lo corra.
end_month = 6
end_month = "{:02d}".format(int(end_month))

end_year = 2023
end_year = str(end_year)

initial_month = 2
initial_month = "{:02d}".format(int(initial_month))

initial_year = 2023
initial_year = str(initial_year)


# Si se quieren fechas especificas

# Si se quieren los ultimos 6 meses:  
#Dates (today and 6 month ago)

#TODAY
#end_month =datetime.date.today().strftime("%m")
#end_year =datetime.date.today().strftime("%Y")

#SIX MONTH AGO
# Calculate the date from 6 months ago
#six_months_ago = datetime.date.today() - datetime.timedelta(days=6*30)
# Get the month and year from 6 months ago
#initial_month = six_months_ago.strftime("%m")
#initial_year = six_months_ago.strftime("%Y")

##############################################################################
###############            Less needed to edit inputs          ###############
##############################################################################

# Inputs and Outputs
inputs = rf'{wd}Inputs/'
outputs = rf'{wd}Outputs/' 


# UserAgent number defined
current_index = 7 #UserAgent starting specif


# Last digit of CUIL
cuil_last_digits = range(0,10,1)

# First two digits of CUIL
cuil_first_digits = (20,27,23)

#dni files
dni_column_name = 'dni' 
pre_column_name = 'pre'
post_column_name = 'post'

#Path to csv with IDs
path_to_dni = rf'{inputs}{dnis_file_name}'


starting_chunk = 1




##############################################################################
###############                   Code                       ###############
##############################################################################

# Specify the path and filename
filename = "certificaciones.csv"
path = f"{outputs}/{filename}"

# Check if the file exists
if not os.path.exists(path):
    # Create an empty DataFrame with the column names
    column_names = ['nom', 'cuil', 'dni', 'cert', 'obs', 'certificacion', 'obrasocial',
                    'trabajadorenactividad', 'asignacionesfamiliares', 'ddjjprovnocipa',
                    'autonomomonotributista', 'casaparticular', 'casaparticularmaternidad',
                    'prestaciondesempleo', 'plansocial', 'prestacionprevisional',
                    'prestacionprevisionalnosipa', 'iniciacionprevisional',
                    'asignacionmadres', 'PROGRESAR', 'monotributistasocial',
                    'pensionnocontributiva', 'iniciacionpensionnocontributiva',
                    'auhembarazo']
    df = pd.DataFrame(columns=column_names)
    
    # Save the DataFrame to a CSV file
    df.to_csv(path, index=False,sep=';')
    print(f"{filename} created as an empty DataFrame.")
else:
    print(f"{filename} already exists.")


# Directory containing the CSV files
directory = f"{outputs}certificaciones.csv"

df_full = pd.read_csv(directory, sep = ';')


# Print the combined dataframe
print(df_full)
    
#Keep the remaining not scrapped
df_whole = pd.read_csv(path_to_dni,sep=';')#.head(3)
df_whole = df_whole.rename(columns={dni_column_name: 'DNI'})
# Convert the unique numeric values from "dni" column in df_full to strings
dni_full_values = df_full['dni'].astype(str).unique()
# Filter the rows in df_whole based on the condition: DNI value is not in df_full
df_whole = df_whole.loc[:, ~df_whole.columns.duplicated()]
df_mid = df_whole[~df_whole['DNI'].isin(df_full['dni'])]

df_chunked = df_mid#.head(2)
df_chunked = df_chunked.rename(columns={dni_column_name: 'DNI'})
# Calculate the chunk number for each row

num_chunks = int(np.ceil(len(df_chunked) / chunk_size))
df_chunked['chunk'] = np.repeat(np.arange(num_chunks), chunk_size)[:len(df_chunked)]


#Define User Agents to prevent acces denied
user_agents = [
    # Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.20",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.17 Safari/537.36",

    # Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.17 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.17 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",

    # Macintosh
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.17 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.17 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
]



#random.shuffle(user_agents)
# We sort the so they do not repear.
sorted_user_agents = []

linux_user_agents = sorted([ua for ua in user_agents if "Linux" in ua])
mac_user_agents = sorted([ua for ua in user_agents if "Macintosh" in ua])
windows_user_agents = sorted([ua for ua in user_agents if "Windows" in ua])

max_length = max(len(linux_user_agents), len(mac_user_agents), len(windows_user_agents))

for i in range(max_length):
    if i < len(linux_user_agents):
        sorted_user_agents.append(linux_user_agents[i])
    if i < len(mac_user_agents):
        sorted_user_agents.append(mac_user_agents[i])
    if i < len(windows_user_agents):
        sorted_user_agents.append(windows_user_agents[i])

for ua in sorted_user_agents:
    print(ua)



#Create data df
data = pd.DataFrame(columns=['nom', 'cuil', 'dni', 'cert', 'obs'])
df_chunked = df_chunked.loc[:, ~df_chunked.columns.duplicated()]
df_chunked = df_chunked.dropna(subset=['pre', 'post'])

try:
    # Convert integer part of 'pre' column to string
    df_chunked['pre'] = df_chunked['pre'].apply(lambda x: str(int(x)))
    # Convert integer part of 'post' column to string
    df_chunked['post'] = df_chunked['post'].apply(lambda x: str(int(x)))
except:
    pass

for chunk in range(starting_chunk-1,num_chunks,1):
  try:
    # options, not used, so you can see what it is doint
    #options = Options()
    
    service = Service(executable_path= path_to_chromedriver)
    # All this options are to prevent acces denied. s
    options = webdriver.ChromeOptions()
    #user_agent = random.choice(user_agents)
    user_agent = sorted_user_agents[current_index]
    #useragent = UserAgent()
    #user_agent= useragent.random
    if headless:
        options.add_argument("--headless")
    else:
        pass
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-bundled-ppapi-flash")
    options.add_argument("--disable-gpu-compositing")
    options.add_argument("--disable-gpu-shader-disk-cache")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    #options.add_argument("--window-size=600,600")
    #options.page_load_strategy = 'none'
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent={0}'.format(user_agent))
    
    #Open Driver
    driver =  webdriver.Chrome(service=service, options=options ) #Execute driver

    df = df_chunked[df_chunked['chunk'] == chunk]
    # Create the DataFrame
    
    for doc in df['DNI']:
        indice = df.loc[df['DNI'] == doc].index + 1
        pre =df.loc[df['DNI'] == doc, 'pre'].iloc[0]
        fin =df.loc[df['DNI'] == doc, 'post'].iloc[0]
        cuit_correcto = False
        attempts = 0
        while cuit_correcto == False and attempts < 2:
          try:  
            print('Searching CUIL of DNI', doc,'element number ', indice.tolist(),' from chunk number',chunk +1, ' out of ', num_chunks, ' of size ',chunk_size,'.')
            #Generate variable to loop
            # Loop until cuit_correcto becomes True or any other exit condition
            driver.get("https://servicioswww.anses.gob.ar/censite/index.aspx")
            times = random.uniform(1,3)
            time.sleep(times)
            driver.find_element('id',"txtCuitPre").send_keys(str(pre))
            driver.find_element('id',"txtCuitDoc").send_keys(str(doc))
            driver.find_element('id',"txtCuitDV").send_keys(str(fin))
            driver.find_element('id',"txtDesdeMes").send_keys(str(initial_month))
            driver.find_element('id',"txtDesdeAnio").send_keys(str(initial_year))
            driver.find_element('id',"txtHastaMes").send_keys(str(end_month))
            driver.find_element('id',"txtHastaAnio").send_keys(str(end_year))
                        
                        
            
            driver.find_element('id',"btnVerificar").click()
            times = random.uniform(1,1.7)
            time.sleep(times)
            # Check if the element is present in the HTML
            if "Se ha producido un error en la aplicaci" in driver.page_source or "Acceso denegado"  in driver.page_source:
                pass
            else:
                cuit_correcto = True
                break
          except: 
              pass  
          attempts += 1
        try: 
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
            line = [[nom,cuil,dni,pre,fin,cert,obs,initial_month,initial_year,end_month,end_year]]
            line_df = pd.DataFrame(line, columns=['nom', 'cuil', 'dni', 'pre','fin', 'cert', 'obs', 'initialmonth', 'initialyear','endmonth','endyear'])
            data = data.append(line_df, ignore_index=True)
            times = random.uniform(0,1)
            time.sleep(times)
        except:
            pass
            
      
    
    
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
    
    # Update 'AUHembarazo' column based on conditions
    data.loc[data['certificacion'] == 1, 'auhembarazo'] = ~data['obs'].str.contains('No Registra Liquidaciones de Asignación Universal por Hijo', case=False)
    data['auhembarazo'] = data['auhembarazo'].replace({True: 1, False: 0})
    # Update 'AUHembarazo' column based on conditions
    #data['AUHembarazo'] = (data['certificacion'] == 1) & (~data['obs'].str.contains('No Registra Liquidaciones de Asignación Universal por Hijo', case=False))
    
    # Generate the file name
    file_name = f"{outputs}certificaciones.csv"
    
    #data = data.astype(str)
    df_full=df_full.append(data, ignore_index=True)
    
    # Keep only unique rows based on the "dni" column
    df_full_unique = df_full.drop_duplicates(subset='dni')

    # Save the unique rows as CSV
    df_full_unique.to_csv(file_name, index=False, sep=';')
    
  except: 
    pass
  current_index += 1
  if current_index >= len(user_agents):
      current_index = 0
  print(f'Current index is {current_index}, and user agent is {user_agent}.')
  driver.quit()
  times = random.uniform(1,20)
  time.sleep(times)
    
print('                       \n \n \n\n \n                                               THATS ALL, FOLKS! \n \n \n \n \n ')