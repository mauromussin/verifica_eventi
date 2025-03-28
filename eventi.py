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
import plotly.graph_objects as go

import plotly.io as pio

def plot_merged_df_plotly(merged_df, output_file=None):
    """
    Plotta il contenuto del DataFrame merged_df usando Plotly.

    Args:
        merged_df (pd.DataFrame): Il DataFrame da plottare.
        output_file (str, optional): Il percorso del file in cui salvare il grafico HTML.
                                     Se None, il grafico viene mostrato nel browser.
    """

    # Verifica che il DataFrame contenga le colonne necessarie
    if 'Time' not in merged_df.columns or 'LAeq_x' not in merged_df.columns or 'LAeq_y' not in merged_df.columns:
        print("Errore: Il DataFrame deve contenere le colonne 'Time', 'LAeq_x' e 'LAeq_y'.")
        return

    # Converti la colonna 'Time' in datetime, se necessario
    if not pd.api.types.is_datetime64_any_dtype(merged_df['Time']):
        merged_df['Time'] = pd.to_datetime(merged_df['Time'], format="%d/%m/%Y %H:%M:%S")

    # Crea il grafico Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=merged_df['Time'], y=merged_df['LAeq_x'], mode='lines', name='LAeq_staz', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=merged_df['Time'], y=merged_df['LAeq_y'], mode='lines', name='LAeq_ARPA', line=dict(color='red')))

    
    # prendi l'id della stazione
    elementi = output_file.split("_")
    staz=elementi[0]

   # Aggiungi etichette e titolo
    fig.update_layout(
        title=f'LAeq over Time per staz={staz}',
        xaxis_title='Time',
        yaxis_title='LAeq'
    )
    
    # Mostra o salva il grafico
    if output_file:
        pio.write_html(fig, file=output_file, auto_open=False)
        print(f"Grafico salvato in {output_file}")
        fig.write_image(f"{output_file}.png")
    else:
        fig.show()

# Esempio di utilizzo:
# Supponiamo di avere un DataFrame chiamato merged_df
# merged_df = ...

# plot_merged_df_plotly(merged_df, output_file='merged_plot.html') #per salvare il plot come file HTML
# plot_merged_df_plotly(merged_df) #per visualizzare il plot nel browser

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

    results_df = pd.DataFrame(results, columns=["First Time", "SEL_staz", "d",
                                                    "LAeq_staz", "LMax_staz", "SEL_ARPA", "LAeq_ARPA", "LMax_ARPA"])
   
    
    #calcola la statistica degli eventi identificati
    
    return results_df

def read_file_his(file_path):
    # Read the file into a DataFrame, skipping the first 18 rows
    # No CSV flag on TranslateHis.exe
    try:
        with open(file_path, 'r', encoding='latin1') as f:
            lines = f.readlines()

        # Estrai la data dalla riga 7
        date_str = lines[6].split('\t')[-1].strip()  # Ottiene l'ultimo elemento dopo la divisione e rimuove gli spazi extra
        date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
        
        # Leggi i dati dal file, saltando le prime 19 righe
        df = pd.read_csv(file_path, skiprows=16, sep='\t', encoding='latin1',usecols=[0, 1], names=['Time', 'LAeq'])
        
        if 'Time' not in df.columns:
            print(f"Errore: Colonna 'Time' non trovata nel file {file_path}")
            return None
        # Combina la data con i tempi e formatta come datetime
        df['Time'] = df['Time'].apply(lambda x: datetime.strptime(f"{date_obj} {x}", '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M:%S'))
        df['LAeq'] = pd.to_numeric(df['LAeq'], errors='coerce')  # 'coerce' sostituisce i valori non validi con NaN
        return df

    except FileNotFoundError:
        print(f'Errore di lettura in {file_path}: file non trovato')
        return None
    except ValueError as e:
        print(f'Errore di formato data/ora in {file_path}: {e}')
        return None
    except pd.errors.ParserError as e:
        print(f'Errore durante la lettura del file {file_path}: {e}')
        return None
    except Exception as e:
        print(f'Errore inatteso durante la lettura del file {file_path}: {e}')
        return None

# funzione che legge sia NNW che dBTrait
def read_and_process_file(file_path):
    try:
       with open(file_path, 'r') as f:
           lines = f.readlines()

       # Verifica il formato del file
       if ';' in lines[6]:  # Riga 7
           df = pd.read_csv(file_path, skiprows=7, engine='python', delimiter=';', decimal=',', names=['Time', 'LAeq'])
       elif '\t' in lines[9]:  # Riga 10
           df = pd.read_csv(file_path, skiprows=10, engine='python', delimiter='\t', decimal=',', names=['Time', 'LAeq'])
       else:
           print(f'Errore di lettura in {file_path}: formato non riconosciuto')
           return None

       # Conversione della colonna 'LAeq' in float
       df['LAeq'] = df['LAeq'].astype(str).str.replace(',', '.').astype(float)
       return df

    except FileNotFoundError:
       print(f'Errore di lettura in {file_path}: file non trovato')
       return None
    except Exception as e:
       print(f'Errore di lettura in {file_path}: {e}')
       return None
    
def merge_dataframes(df_staz, df_ARPA):
    # Filter df_staz to keep only rows with times that exist in df_ARPA
    filtered_df_staz = df_staz[df_staz['Time'].isin(df_ARPA['Time'])]
    
    # Merge the two dataframes on the time columns
    merged_df = pd.merge(filtered_df_staz, df_ARPA, left_on='Time', right_on='Time')
    
    return merged_df


def save_results_to_csv(results, output_file):
    df = pd.DataFrame(results, columns=["First Time", "SEL_staz", "d", "LAeq_staz",
                                        "LMax_staz","SEL_ARPA","LAeq_ARPA","LMax_ARPA"])
    df.to_csv(output_file, index=False, float_format='%.2f', mode='a', header=False)

def confronta_distribuzioni(df,output_file):
    """
    Calcola le medie e le varianze delle colonne specificate, confronta le medie e le varianze tra coppie di colonne
    e verifica con un test statistico se le coppie di colonne provengono dalla stessa distribuzione.

    Args:
        df (pd.DataFrame): Il DataFrame contenente i dati.
        output_file: il file dove vengono stampati i dati (di tipo markdown, estensione aggiunta automaticamente)
    Returns:
        None
    """
    # Definisci l'ordine desiderato delle colonne
    ordine_colonne = ["First Time", "d", "SEL_staz", "LAeq_staz", "LMax_staz", "SEL_ARPA", "LAeq_ARPA", "LMax_ARPA"]
    # Riordina il DataFrame
    df = df[ordine_colonne]

    fileout=output_file+'.stats.html'
    # Aggiungi intestazione HTML
    with open(fileout, "w") as f:
      f.write("<html><head><title>Confronto Distribuzioni</title></head><body>")
      f.write("<h1>Confronto delle Distribuzioni</h1>")
      
      # Tabella degli eventi in parallelo
      f.write("<h2>Eventi in parallelo</h2>")
      f.write(df.to_html(index=False,float_format="%.2f"))
      f.write("<br><br>")
      
      # Calcola le medie
      medie = df[['SEL_staz', 'LAeq_staz', 'LMax_staz', 'SEL_ARPA', 'LAeq_ARPA', 'LMax_ARPA']].mean()
      
      # Calcola le varianze
      varianze = df[['SEL_staz', 'LAeq_staz', 'LMax_staz', 'SEL_ARPA', 'LAeq_ARPA', 'LMax_ARPA']].var()
     
      risultati = []     
      # Confronta le medie e le varianze tra coppie di colonne
      coppie = [('SEL_staz', 'SEL_ARPA'), ('LAeq_staz', 'LAeq_ARPA'), ('LMax_staz', 'LMax_ARPA')]
      for col1, col2 in coppie:
          # Test di Kolmogorov-Smirnov
          stat, p = stats.ks_2samp(df[col1], df[col2])
          esito = "simili" if p > 0.05 else "diverse"
          risultati.append([col1, medie[col1], varianze[col1], "", "", ""])
          risultati.append([col2, medie[col2], varianze[col2], stat, p, esito])
          
      # Creazione DataFrame per tabella HTML
      tabella_df = pd.DataFrame(risultati, columns=["Colonna", "Medie", "Varianza", "Test K-S", "p-value", "Esito"])   
      f.write(tabella_df.to_html(index=False))
      # Chiudi il tag body e html
      f.write("</body></html>")

    print(f"HTML creato con successo: {fileout}")

def read_csv_to_dataframe(file_path):
    # Leggi il file CSV in un DataFrame
    df = pd.read_csv(file_path, delimiter=';')
    return df

def process_and_merge_files(input_file_path):
    """
    Legge un file di input, legge i file specificati nelle colonne 'file_staz' e 'file_ARPA',
    unisce i DataFrame e converte la colonna 'Time' in formato datetime.

    Args:
        input_file_path (str): Percorso del file di input.

    Returns:
        pandas.DataFrame: DataFrame unito, o None in caso di errori.
    """
    try:
        # Leggi il file di input
        input_df = pd.read_csv(input_file_path,sep=';')

        # Inizializza una lista per i DataFrame uniti
        merged_dfs = []

        # Itera sulle righe del DataFrame di input
        for index, row in input_df.iterrows():
            file_staz_path = row['file_staz']
            file_arpa_path = row['file_ARPA']
            threshold = row['thr']
            duration = row['dur']
            staz=row['id']
            print(f'Elaborazione dei file stazione:{file_staz_path} ARPA {file_arpa_path}')
            # Leggi i file con le funzioni specificate
            df_staz = read_file_his(file_staz_path)
            df_arpa = read_and_process_file(file_arpa_path)

            # Verifica se la lettura dei file ha avuto successo
            if df_staz is None or df_arpa is None:
                print(f"Errore: Impossibile leggere file per la riga {index}")
                continue  # Passa alla riga successiva

            # Unisci i DataFrame
            merged_df = merge_dataframes(df_staz, df_arpa)

            # Converti la colonna 'Time' in datetime
            merged_df['Time'] = pd.to_datetime(merged_df['Time'], format="%d/%m/%Y %H:%M:%S")
            # Applica identify_and_calculate_events
            results_df = identify_and_calculate_events(merged_df, threshold, duration)
            
            # Salva i risultati in un file CSV (append)
            output_file=f'{staz}_output_events'
            
            #Calcola le statistiche e stampa il file md
            confronta_distribuzioni(results_df,output_file)
            
            # plotta il grafico e stampa il file png
            plot_merged_df_plotly(merged_df,output_file+'.html') #per visualizzare il plot nel browser 
            save_results_to_csv(results_df, output_file+'.csv')
            merged_dfs.append(merged_df)

        # Concatena tutti i DataFrame uniti in uno singolo
        if merged_dfs:
            final_merged_df = pd.concat(merged_dfs, ignore_index=True)
            return final_merged_df
        else:
            return None

    except FileNotFoundError:
        print(f"Errore: File di input '{input_file_path}' non trovato.")
        return None
    except Exception as e:
        print(f"Errore inatteso: {e}")
        return None


input_file = 'MXP-1-2024.CSV' #sostituisci il percorso

result_df = process_and_merge_files(input_file)

if result_df is not None:
    print(result_df)


