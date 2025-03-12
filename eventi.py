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

#Funzione che crea il grafico in parallelo
def plot_merged_df(merged_df):
    plt.figure(figsize=(12, 6))
    plt.plot(merged_df['Time'], merged_df['LAeq_x'], label='LAeq_staz')
    plt.plot(merged_df['Time'], merged_df['LAeq_y'], label='LAeq_ARPA')
    plt.xlabel('Time')
    plt.ylabel('LAeq')
    plt.title('LAeq over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

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
    df = pd.DataFrame(results, columns=["First Time", "SEL", "N", "LAeq", "LMax"])
    df.to_csv(output_file, index=False,float_format='%.2f')


# Esempio di utilizzo
file_path = './data/0815112023.his.txt'
# print(os.path.isfile(file_path),os.listdir("."))
threshold = 60.0
duration = 20
output_file = './data/event_values.csv'
df_staz=read_file_his(file_path)
#lettura dBTrait
# Esempio di utilizzo
file_path = './data/santasavina.txt'
df_ARPA = read_and_process_dbTrait(file_path)

merged_df = merge_dataframes(df_staz, df_ARPA)
plt.figure(figsize=(12, 6))
plt.plot(merged_df['Time'], merged_df['LAeq_x'], label='LAeq_staz')
plt.plot(merged_df['Time'], merged_df['LAeq_y'], label='LAeq_ARPA')
plt.xlabel('Time')
plt.ylabel('LAeq')
plt.title('LAeq over Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#plot_merged_df(merged_df)
"""
if os.path.isfile(file_path):
    day = file_path.split('.his')[0][9:17]  # Estrai il giorno dal nome del file
    events = identify_events(file_path, threshold, duration)
    event_values = calculate_event_values(events, day)
    print(event_values)
    save_results_to_csv(event_values, output_file)
    print(f"Results saved to {output_file}")
else:
    print(f"File not found: {file_path}")
"""