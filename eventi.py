# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:12:03 2025

@author: MMUSSIN
"""
import os
import math
import pandas as pd
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
def calculate_event_values(events, day):
    results = []
    for event in events:
        values = [10 ** (laeq / 10) for time, laeq in event]
        total_sum = sum(values)
        result = 10 * math.log10(total_sum)
        
        # Calcola i valori aggiuntivi
        first_time = min(time for time, laeq in event)
        first_time_with_day = f"{day} {first_time}"
        sel = result
        n = len(event)
        laeq_value = result - 10 * math.log10(n)
        lmax = max(laeq for time, laeq in event)
        
        results.append((first_time_with_day, sel, n, laeq_value, lmax))
    return results

def save_results_to_csv(results, output_file):
    df = pd.DataFrame(results, columns=["First Time", "SEL", "N", "LAeq", "LMax"])
    df.to_csv(output_file, index=False)


# Esempio di utilizzo
file_path = '0110102023.his.txt'
# print(os.path.isfile(file_path),os.listdir("."))
threshold = 60.0
duration = 20
output_file = 'event_values.csv'

if os.path.isfile(file_path):
    day = file_path.split('.')[0][2:10]  # Estrai il giorno dal nome del file
    events = identify_events(file_path, threshold, duration)
    event_values = calculate_event_values(events, day)
    save_results_to_csv(event_values, output_file)
    print(f"Results saved to {output_file}")
else:
    print(f"File not found: {file_path}")