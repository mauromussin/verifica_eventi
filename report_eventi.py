#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 10:13:39 2025

@author: mauro
"""
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
import markdown
import io
import re

def create_pdf_with_image_and_markdown(image_path, markdown_path, pdf_file):
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    width, height = letter
    elements = []
    
    # 1. Inserisci l'immagine PNG
    img_width = 6 * inch
    img_height = 4 * inch
    img = Image(image_path, width=img_width, height=img_height)
    elements.append(img)
    elements.append(Spacer(1, 0.5 * inch))  # Spazio dopo l'immagine

    # 2. Inserisci il contenuto del file Markdown
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    html_content = markdown.markdown(markdown_content, extensions=['tables'])

    # Estrai le tabelle HTML
    tables = re.findall(r'<table.*?</table>', html_content, re.DOTALL)

    styles = getSampleStyleSheet()

    for table_html in tables:
        rows = re.findall(r'<tr.*?</tr>', table_html, re.DOTALL)
        table_data = []

        for row in rows:
            cells = re.findall(r'<t[dh]>.*?</t[dh]>', row, re.DOTALL)
            row_data = [Paragraph(re.sub(r'<.*?>', '', cell).strip() or " ", styles['BodyText']) for cell in cells]
            table_data.append(row_data)

        if table_data and table_data[0]:
            col_count = len(table_data[0])  # Numero di colonne
            col_widths = [width / col_count] * col_count  # Distribuzione equa della larghezza

            table = Table(table_data, colWidths=col_widths)

            # Applica uno stile più leggibile
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))  # Spazio dopo ogni tabella

    # 3. Inserisci il testo Markdown rimanente
    text_html = re.sub(r'<table.*?</table>', '', html_content, flags=re.DOTALL)
    elements.append(Paragraph(text_html, styles['Normal']))

    doc.build(elements)
    print(f"File PDF '{pdf_file}' creato con successo.")
def markdown_to_pdf(markdown_file, output_pdf):
    # Leggi il contenuto del file markdown
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    # Converte il Markdown in HTML
    html_content = markdown.markdown(markdown_content)

    # Creiamo il documento PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    elements = []

    # Aggiungiamo uno stile base per il testo
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    
    # Aggiungiamo il testo principale come paragrafi
    text = re.sub(r'<table.*?</table>', '', html_content, flags=re.DOTALL)  # Rimuoviamo temporaneamente le tabelle per la gestione separata
    p = Paragraph(text, normal_style)
    elements.append(p)

    # Gestiamo le tabelle HTML separatamente
    tables = re.findall(r'<table.*?</table>', html_content, re.DOTALL)

    for table_html in tables:
        # Estrai le righe della tabella
        rows = re.findall(r'<tr.*?</tr>', table_html, re.DOTALL)
        table_data = []
        
        for row in rows:
            # Estrai le celle della riga
            cells = re.findall(r'<t[dh]>.*?</t[dh]>', row, re.DOTALL)
            row_data = [re.sub(r'<.*?>', '', cell).strip() for cell in cells]
            table_data.append(row_data)

        # Crea la tabella con ReportLab
        if table_data:
            table = Table(table_data)

            # Aggiungiamo uno stile alla tabella
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), (0.3, 0.5, 0.8)),  # Colore di sfondo per l'intestazione
                ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Colore del testo per l'intestazione
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),  # Colore di sfondo per le righe
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Griglia delle celle
            ]))

            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))  # Spazio dopo ogni tabella

    # Aggiungiamo il documento PDF
    doc.build(elements)
    print(f"PDF creato con successo: {output_pdf}")
import pdfkit

def convert_html_to_pdf(input_html, output_pdf):
    """
    Converte un file HTML in PDF mantenendo la formattazione delle tabelle.
    
    Args:
        input_html (str): Percorso del file HTML di input.
        output_pdf (str): Percorso del file PDF di output.
    """
    pdfkit.from_file(input_html, output_pdf, options={"enable-local-file-access": ""})
    

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
import pdfkit
import os
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
import pdfkit
import os
def convert_html_to_pdf_with_image(input_html, output_pdf, image_path):
    """
    Converte un file HTML in PDF, inserendo un'immagine PNG all'inizio della pagina
    e posizionando le due tabelle subito dopo senza sovrapposizioni.
    """

    # Dimensioni della pagina
    width, _ = letter
    margin = 72  # Margine di 1 pollice
    img_width = width   # Occupa quasi tutta la larghezza
    img_height = img_width * 2 / 3  # Mantiene le proporzioni

    # Intestazioni delle tabelle
    table1_header = ["First Time", "d", "SEL_staz", "LAeq_staz", "LMax_staz", "SEL_ARPA", "LAeq_ARPA", "LMax_ARPA"]
    #table1_header = ["First Time", "d", "SEL_staz", "SEL_ARPA", "LAeq_staz", "LAeq_ARPA", "LMax_staz", "LMax_ARPA"]
    table2_header = ["Parametro", "Media", "Varianza", "Test K-S", "p-value", "Esito confronto"]

    # Estrai i dati delle tabelle dal file HTML
    table1_data, table2_data = extract_tables_from_html(input_html)

    # Crea il documento finale
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    elements = []

    # Aggiunge l'immagine (grafico) in cima
    img = Image(image_path, width=img_width, height=img_height)
    elements.append(img)
    elements.append(Spacer(1, 20))  # Spazio tra il grafico e la prima tabella

    # Formatta e aggiunge la prima tabella con intestazione
    if table1_data:
        table1 = Table([table1_header] + table1_data)  # Aggiunge l'intestazione ai dati
        table1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table1)
        elements.append(Spacer(1, 30))  # Spazio tra le tabelle

    # Formatta e aggiunge la seconda tabella con intestazione
    if table2_data:
        table2 = Table([table2_header] + table2_data)  # Aggiunge l'intestazione ai dati
        table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table2)

    # Genera il PDF finale con grafico e tabelle
    doc.build(elements)

    print(f"File PDF '{output_pdf}' creato con successo.")

def extract_tables_from_html(html_file):
    """
    Estrae le due tabelle dal file HTML, ignorando le prime due righe.
    Restituisce due liste di liste: una per ogni tabella.
    """
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Trova tutte le tabelle nel file HTML
    tables = soup.find_all("table")

    if len(tables) < 2:
        print("Errore: il file HTML non contiene abbastanza tabelle!")
        return [], []

    # Funzione per estrarre i dati da una tabella
    def extract_table_data(table):
        rows = table.find_all("tr")[2:]  # Ignora le prime due righe
        return [[cell.get_text(strip=True) for cell in row.find_all(["td", "th"])] for row in rows]

    # Estrai dati dalle due tabelle
    table1_data = extract_table_data(tables[0])
    table2_data = extract_table_data(tables[1])

    return table1_data, table2_data
# Esempio di utilizzo

if __name__ == '__main__':
    # Esempio di utilizzo
    image_file = "49_output_events.html.png"
    markdown_file = "49_output_events.md"
    pdf_file = "49_output_relazione.pdf"
    #convert_html_to_pdf("10_output_events.stats.html", "report1.pdf")
    convert_html_to_pdf_with_image("49_output_events.stats.html", "49_report.pdf",image_file)
    #create_pdf_with_image_and_markdown(image_file, markdown_file, pdf_file)