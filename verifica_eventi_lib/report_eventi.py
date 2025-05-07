#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 10:13:39 2025

@author: mauro
"""
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
import markdown
import io
import re
from PyPDF2.errors import PdfReadError
from reportlab.lib import colors
import pdfkit
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
import pdfkit
import os


def merge_pdfs(pdf_files, output_file):
    """
    Unisce più file PDF in un unico file

    Args:
        pdf_files (list): Lista di percorsi dei file PDF da unire
        output_file (str): Percorso del file PDF di output
    """
    merger = PdfMerger()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(output_file)
    merger.close()
    print(f"File PDF uniti con successo in '{output_file}'")


def add_page_numbers(input_pdf, output_pdf):
    """
    Aggiunge i numeri di pagina a un PDF esistente

    Args:
        input_pdf (str): Percorso del PDF originale
        output_pdf (str): Percorso per il nuovo PDF numerato
    """
    # Leggi il PDF originale
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Crea un buffer per i numeri di pagina
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    for page_num in range(len(reader.pages)):
        # Crea il testo per il numero di pagina
        can.setFont("Helvetica", 9)
        can.drawString(190 * mm, 10 * mm, f"Pagina {page_num + 1}")
        can.showPage()

    can.save()

    # Unisci i numeri di pagina al PDF originale
    packet.seek(0)
    number_pdf = PdfReader(packet)

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        if page_num < len(number_pdf.pages):
            page.merge_page(number_pdf.pages[page_num])
        writer.add_page(page)

    # Salva il nuovo PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)
    print(f"Numeri di pagina aggiunti a '{output_pdf}'")


def create_pdf_with_image_and_markdown(image_path, markdown_path, pdf_file):
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
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
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
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
    


def convert_html_to_pdf_with_image(input_html, output_pdf, image_path):
    """
    Converte un file HTML in PDF, inserendo un'immagine PNG all'inizio della pagina
    e posizionando le due tabelle subito dopo senza sovrapposizioni.
    """

    # Dimensioni della pagina
    width, _ = letter
    margin = 72  # Margine di 1 pollice
    img_width = width   # Occupa quasi tutta la larghezza
    img_height = img_width * 1 / 2  # Mantiene le proporzioni

    # Intestazioni delle tabelle
    #table1_header = ["First Time", "d", "SEL_staz", "LAeq_staz", "LMax_staz", "SEL_ARPA", "LAeq_ARPA", "LMax_ARPA"]
    #table1_header = ["Data e Ora", "SEL Gestore", "SEL ARPA", "LAeq Gestore", "LAeq ARPA", "LAmax Gestore", "LAmax ARPA"]
    table1_header = [
       ["Data e Ora", "SEL", "", "LAeq", "", "LAmax", ""],
       ["", "Gestore", "ARPA", "Gestore", "ARPA", "Gestore", "ARPA"]
   ]
    table2_header = ["Parametro", "Media", "Varianza", "Test K-S", "p-value", "Esito confronto"]

    # Estrai i dati delle tabelle dal file HTML
    table1_data, table2_data = extract_tables_from_html(input_html)

    # Crea il documento finale
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    elements = []

    # Aggiunge l'immagine (grafico) in cima
    img = Image(image_path, width=img_width, height=img_height)
    elements.append(img)
    elements.append(Spacer(1, 20))  # Spazio tra il grafico e la prima tabella

    # Formatta e aggiunge la prima tabella con intestazione
    if table1_data:
       table1 = Table(table1_header + table1_data, repeatRows=2)  # Aggiunge l'intestazione ai dati e ripete le prime due righe
       table1.setStyle(TableStyle([
           ('SPAN', (1, 0), (2, 0)),  # Unisce le celle "SEL"
           ('SPAN', (3, 0), (4, 0)),  # Unisce le celle "LAeq"
           ('SPAN', (5, 0), (6, 0)),  # Unisce le celle "LAmax"
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
    def extract_table_data(table, riordina=False):
        rows = table.find_all("tr")[1:]  # Ignora la prima riga
        data = [[cell.get_text(strip=True) for cell in row.find_all(["td", "th"])] for row in rows]
        if riordina:
            # Riordina i dati secondo l'ordine desiderato
            reordered_data = []
            for row in data:
                reordered_row = [row[0],  row[2], row[5], row[3], row[6], row[4], row[7]]
                reordered_data.append(reordered_row)
            return reordered_data
        else:
            return data

    # Estrai dati dalle due tabelle
    table1_data = extract_table_data(tables[0], riordina=True)
    table2_data = extract_table_data(tables[1])

    return table1_data, table2_data


