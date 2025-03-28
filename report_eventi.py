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
from PIL import Image as PILImage    

def convert_html_to_pdf_with_image(input_html, output_pdf, image_path):
    """
    Converte un file HTML in PDF, inserendo un'immagine PNG nella stessa pagina della tabella e occupando tutto lo spazio orizzontale.
    """

    options = {
        "enable-local-file-access": "",
        "user-style-sheet": "body { font-size: 10pt; }"
    }

    temp_pdf = "temp.pdf"
    pdfkit.from_file(input_html, temp_pdf, options=options)

    try:
        # Apri il PDF temporaneo
        with open(temp_pdf, "rb") as temp_file:
            reader = PdfReader(temp_file)
            writer = PdfWriter()

            # Ottieni la prima pagina del PDF temporaneo
            page = reader.pages[0]

            # Inserisci l'immagine PNG nella stessa pagina della tabella
            width, height = letter
            img_width = width - 2 * inch  # Occupare tutto lo spazio orizzontale
            img_height = img_width * 2 / 3  # Mantenere le proporzioni
            img_x = inch
            img_y = height - img_height - inch

            # Crea un canvas ReportLab per disegnare l'immagine sulla stessa pagina
            image_temp_pdf = "image_temp.pdf"
            c = canvas.Canvas(image_temp_pdf, pagesize=letter)
            c.drawImage(image_path, img_x, img_y, width=img_width, height=img_height)
            c.save()

            # Unisci la pagina con l'immagine con la pagina della tabella
            with open(image_temp_pdf, "rb") as image_file:
                image_reader = PdfReader(image_file)
                image_page = image_reader.pages[0]
                page.merge_page(image_page)

            # Aggiungi la pagina modificata al writer
            writer.add_page(page)

            # Aggiungi le altre pagine del PDF temporaneo
            for p in reader.pages[1:]:
                writer.add_page(p)

            # Salva il PDF modificato
            with open(output_pdf, "wb") as output:
                writer.write(output)

        print(f"File PDF '{output_pdf}' creato con successo.")

    except PdfReadError as e:
        print(f"Errore durante la lettura del PDF: {e}")
    except FileNotFoundError as e:
        print(f"File non trovato: {e}")
    except Exception as e:
        print(f"Si è verificato un errore inatteso: {e}")
# Esempio di utilizzo

if __name__ == '__main__':
    # Esempio di utilizzo
    image_file = "10_output_events.html.png"
    markdown_file = "10_output_events.md"
    pdf_file = "10_output_relazione.pdf"
    #convert_html_to_pdf("10_output_events.stats.html", "report1.pdf")
    convert_html_to_pdf_with_image("10_output_events.stats.html", "report1.pdf",image_file)
    #create_pdf_with_image_and_markdown(image_file, markdown_file, pdf_file)