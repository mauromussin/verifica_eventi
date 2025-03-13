# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:12:03 2025

@author: MMUSSIN
"""

import os
import math
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import bokeh
from scipy import stats

#Funzione che crea il grafico in parallelo
def plot_merged_df(merged_df,output_file):
    from bokeh.plotting import figure, show
    from bokeh.io import output_file
    from bokeh.models import ColumnDataSource

      # Salva il grafico come HTML
    source = ColumnDataSource(merged_df)

    p = figure(x_axis_type="datetime", title="LAeq over Time", width=1000, height=500)
    p.line(x="Time", y="LAeq_x", source=source, legend_label="LAeq_staz", line_width=2, color="blue")
    p.line(x="Time", y="LAeq_y", source=source, legend_label="LAeq_ARPA", line_width=2, color="red")

    show(p)  # Apri il grafico in un browser

#Funzione che identifica gli eventi
"""
to-do: prendere dal dataframe e non dal file
"""    
def identify_events(file_path, threshold, duration):
    events = []
    current_event = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            columns = line.split()
            if len(columns) > 1 and columns[1].replace('.', '', 1).isdigit():
                time = columns[0]
                laeq = float(columns[1])
                if laeq > threshold:
                    current_event.append((time, laeq))
                else:
                    if len(current_event) >= duration:
                        events.append(current_event)
                    current_event = []
        if len(current_event) >= duration:
            events.append(current_event)
    return events
#Funzione che calcola i valori degli eventi dal LAeq 1s
"""
to do: eliminare il riferimento a day e usare il dataframe
"""
def calculate_event_values(events, day):
    results = []
    for event in events:
        values = [10 ** (laeq / 10) for time, laeq in event]
        total_sum = sum(values)
        result = 10 * math.log10(total_sum)
        
        # Calcola i valori aggiuntivi
        first_time = min(time for time, laeq in event)
        first_datetime = datetime.strptime(f"{day} {first_time}", "%d%m%Y %H:%M:%S.%f")
        formatted_dt = first_datetime.strftime("%d/%m/%Y %H:%M:%S")

        sel = result
        n = len(event)
        laeq_value = result - 10 * math.log10(n)
        lmax = max(laeq for time, laeq in event)
        
        results.append((formatted_dt, sel, n, laeq_value, lmax))
    return results

def identify_and_calculate_events(df, threshold, duration):
    events = []
    current_event = []
    
    for index, row in df.iterrows():
        time = row['Time']
        laeq_x = row['LAeq_x']
        laeq_y = row['LAeq_y']
        if laeq_x > threshold or laeq_y > threshold:
            current_event.append((time, laeq_x, laeq_y))
        else:
            if len(current_event) >= duration:
                events.append(current_event)
            current_event = []
    if len(current_event) >= duration:
        events.append(current_event)
    
    results = []
    for event in events:
        values_x = [10 ** (laeq_x / 10) for time, laeq_x, laeq_y in event]
        values_y = [10 ** (laeq_y / 10) for time, laeq_x, laeq_y in event]
        
        total_sum_x = sum(values_x)
        total_sum_y = sum(values_y)
        
        result_x = 10 * math.log10(total_sum_x)
        result_y = 10 * math.log10(total_sum_y)
        
        # Calculate additional values
        first_time = min(time for time, laeq_x, laeq_y in event)
        formatted_dt = first_time.strftime("%d/%m/%Y %H:%M:%S")

        sel_x = result_x
        sel_y = result_y
        
        n = len(event)
        
        laeq_value_x = result_x - 10 * math.log10(n)
        laeq_value_y = result_y - 10 * math.log10(n)
        
        lmax_x = max(laeq_x for time, laeq_x, laeq_y in event)
        lmax_y = max(laeq_y for time, laeq_x, laeq_y in event)
        
        results.append((formatted_dt, sel_x, n, laeq_value_x, lmax_x, sel_y, laeq_value_y, lmax_y))
        # Convert results to a DataFrame
        results_df = pd.DataFrame(results, columns=["First Time", "SEL_staz", "d", 
                            "LAeq_staz", "LMax_staz", "SEL_ARPA", "LAeq_ARPA", "LMax_ARPA"])
    return results_df

def read_and_process_dbTrait(file_path):
    # Read the file into a DataFrame, skipping the first 8 rows and the last row
    df = pd.read_csv(file_path, skiprows=9, skipfooter=1, engine='python', 
                     delimiter='\t', decimal=',',names=['Time', 'LAeq'])
    
    # Replace comma with point in the decimal separator
    df['LAeq'] = df['LAeq'].astype(str).replace(',', '.').astype(float)
    
    return df
def read_file_his(file_path):
    # Read the file into a DataFrame, skipping the first 8 rows
    day = file_path.split('.his')[0][9:17]  # Estrai il giorno dal nome del file
    df = pd.read_csv(file_path, skiprows=18, delimiter='\s+', usecols=[0, 1], 
                     names=['Time', 'LAeq'], encoding='latin1')
    # Add day to time and convert to datetime format
    df['Time'] = df['Time'].apply(lambda x: datetime.strptime(f"{day} {x}", 
                        "%d%m%Y %H:%M:%S.%f").strftime("%d/%m/%Y %H:%M:%S"))
    return df

def merge_dataframes(df_staz, df_ARPA):
    # Filter df_staz to keep only rows with times that exist in df_ARPA
    filtered_df_staz = df_staz[df_staz['Time'].isin(df_ARPA['Time'])]
    
    # Merge the two dataframes on the time columns
    merged_df = pd.merge(filtered_df_staz, df_ARPA, left_on='Time', right_on='Time')
    
    return merged_df


def save_results_to_csv(results, output_file):
    df = pd.DataFrame(results, columns=["First Time", "SEL_staz", "N", "LAeq_staz", 
        "LMax_staz","SEL_ARPA","LAeq_ARPA","LMAX_ARPA"])
    df.to_csv(output_file, index=False,float_format='%.2f')

def confronta_distribuzioni(df):
    """
    Calcola le medie e le varianze delle colonne specificate, confronta le medie e le varianze tra coppie di colonne
    e verifica con un test statistico se le coppie di colonne provengono dalla stessa distribuzione.

    Args:
        df (pd.DataFrame): Il DataFrame contenente i dati.

    Returns:
        None
    """

    # Calcola le medie
    medie = df[['SEL_staz', 'LAeq_staz', 'LMax_staz', 'SEL_ARPA', 'LAeq_ARPA', 'LMax_ARPA']].mean()
    print("Medie:\n", medie)

    # Calcola le varianze
    varianze = df[['SEL_staz', 'LAeq_staz', 'LMax_staz', 'SEL_ARPA', 'LAeq_ARPA', 'LMax_ARPA']].var()
    print("\nVarianze:\n", varianze)

    # Confronta le medie e le varianze tra coppie di colonne
    coppie = [('SEL_staz', 'SEL_ARPA'), ('LAeq_staz', 'LAeq_ARPA'), ('LMax_staz', 'LMax_ARPA')]
    for col1, col2 in coppie:
        print(f"\nConfronto tra {col1} e {col2}:")
        print(f"  Media {col1}: {medie[col1]:.2f}, Media {col2}: {medie[col2]:.2f}")
        print(f"  Varianza {col1}: {varianze[col1]:.2f}, Varianza {col2}: {varianze[col2]:.2f}")

        # Esegui il test di Kolmogorov-Smirnov per verificare se le distribuzioni sono simili
        stat, p = stats.ks_2samp(df[col1], df[col2])
        print(f"  Test di Kolmogorov-Smirnov: Statistica = {stat:.3f}, p-value = {p:.3f}")
        if p > 0.05:
            print("  Le distribuzioni sono probabilmente simili.")
        else:
            print("  Le distribuzioni sono probabilmente diverse.")


# Esempio di utilizzo
# Leggo i dati della stazione
file_path = './data/0815112023.his.txt'
# print(os.path.isfile(file_path),os.listdir("."))
#day = file_path.split('.his')[0][9:17]  # Estrai il giorno dal nome del file
df_staz=read_file_his(file_path)
#lettura dBTrait
file_path = './data/santasavina.txt'
df_ARPA = read_and_process_dbTrait(file_path)

merged_df = merge_dataframes(df_staz, df_ARPA)

#Setto Time come datetime x bokeh
merged_df['Time'] = pd.to_datetime(merged_df['Time'], format="%d/%m/%Y %H:%M:%S")
print("Inizio il plot...")
output_file='./data/merged_plot.png'
#plot_merged_df(merged_df,output_file)

#Ciclo riconoscimento eventi

threshold = 60.0
duration = 20
output_file = './data/event_values.csv'
events_values_df=pd.DataFrame()
events_values_df = identify_and_calculate_events(merged_df, threshold, duration)
print(events_values_df)
events_values_df.to_csv(output_file,index=False,float_format='%.2f')
confronta_distribuzioni(events_values_df)

