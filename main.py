#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 07:58:20 2025

@author: mauro

Il codice contiene le istruzioni del main per eseguire il calcolo degli eventi e la generazione del report
in formato pdf.

Il file di input che contiene tutte le informazioni può essere passato come argomento del file oppure 
può essere inserito manualmente in fase di esecuzione. Anche la cartella di destinazione dei file pdf 
può essere passata come argomento oppure viene richiesta in fase di esecuzione:
    
    python main.py nome_file_input.csv cartella_output
    
oppure

   python main.py nome_file_input.csv 
   
   In fase di esecuzione verrà chiesto:
       Inserisci la cartella di output per i PDF:
           
           
oppure

   python main.py
   
   In fase di esecuzione verrà chiesto:
      Inserisci il nome del file da elaborare:
      Inserisci la cartella di output per i PDF:
   
    
"""

import sys
from verifica_eventi_lib.eventi import process_and_merge_files
from verifica_eventi_lib.report_eventi import convert_html_to_pdf_with_image
import glob
import os
if __name__ == "__main__":
    print("Esecuzione del calcolo degli eventi e generazione dei report...")
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_folder = sys.argv[2]
    elif len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_folder = input("Inserisci la cartella di output per i PDF: ")
    else:
        input_file = input("Inserisci il nome del file da elaborare: ")
        output_folder = input("Inserisci la cartella di output per i PDF: ")

    # Crea la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
     
    print ("...lettura dati di input da {input_file} ed elaborazione su {output_folder}...")
    result_df = process_and_merge_files(input_file)

    if result_df is not None:
            print("...eventi identificati:")
            print(result_df)
            print("Generazione report pdf...")
            image_files_list = glob.glob("*.html.png")
            lista_base_nomi = [nome_file.replace('.html.png', '.stats.html') for nome_file in image_files_list]
            lista_report = [os.path.join(output_folder, nome_file.replace('.html.png', '.pdf')) for nome_file in image_files_list] 
            elenco_file = []
            for i in range(len(image_files_list)):
                elemento = [image_files_list[i], lista_base_nomi[i]]
                elenco_file.append(elemento)
                convert_html_to_pdf_with_image(lista_base_nomi[i], lista_report[i], image_files_list[i])
            for file_da_cancellare in lista_base_nomi:
                try:
                    os.remove(file_da_cancellare)
                    print(f"File {file_da_cancellare} cancellato con successo.")
                except FileNotFoundError:
                    print(f"File {file_da_cancellare} non trovato.")
                except Exception as e:
                    print(f"Errore durante la cancellazione del file {file_da_cancellare}: {e}")
            print("Elaborazione terminata!")
    else:
            print("Errore durante l'elaborazione del file.")
    