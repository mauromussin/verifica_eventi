import glob
import os
import re
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import io
from reportlab.pdfgen import canvas
from verifica_eventi_lib.report_eventi import convert_html_to_pdf_with_image

def get_custom_order_for_airport( input_file: str) :

    """
    Estrae l'ordine personalizzato dei PDF in base al codice aeroporto nell'input file.

    Args:
        input_file: Nome del file/contentuto che contiene il codice aeroporto (es. "MXP-1-2024")


    Returns:
        Lista con l'ordine personalizzato dei numeri dei file

    Raises:
        ValueError: Se l'aeroporto non è supportato o manca la configurazione
    """
    # 1. Verifica e estrazione codice aeroporto
    input_upper = input_file.upper()
    AIRPORT_CONFIGS = {
        'MXP': {'custom': [10, 49, 1505, 8, 45, 24, 3, 1519, 1515]},
        'LIN': {'custom': [11, 47, 1]},
        'BGY': {'custom': [5, 10, 15]},
        'VBS': {'custom': [100, 200]}
    }
    SUPPORTED_AIRPORTS = list(AIRPORT_CONFIGS.keys())
    airport_code = None

    for code in SUPPORTED_AIRPORTS:
        if code.upper() in input_upper:
            airport_code = code
            break

    if not airport_code:
        raise ValueError(
            f"Nessun aeroporto valido trovato in '{input_file}'. "
            f"Aeroporti supportati: {supported_airports}"
        )

    # 2. Verifica presenza configurazione
    if airport_code not in AIRPORT_CONFIGS:
        raise ValueError(
            f"Configurazione mancante per l'aeroporto '{airport_code}'. "
            f"Aeroporti configurati: {list(AIRPORT_CONFIGS.keys())}"
        )

    if 'custom' not in AIRPORT_CONFIGS[airport_code]:
        raise ValueError(
            f"Campo 'custom' mancante nella configurazione di '{airport_code}'"
        )

    # 3. Restituisci l'ordine personalizzato
    return AIRPORT_CONFIGS[airport_code]['custom']


def merge_pdfs_with_page_numbers(pdf_files: list, output_path: str, start_page: int = 1):
    """
    Unisce i PDF in un unico file con numerazione progressiva delle pagine

    Args:
        pdf_files: Lista ordinata dei file PDF da unire
        output_path: Percorso del PDF unito in output
        start_page: Numero di partenza per la numerazione
    """
    # 1. Verifica preliminare dei file
    for pdf in pdf_files:
        if not os.path.exists(pdf):
            raise FileNotFoundError(f"File non trovato: {pdf}")
        if os.path.getsize(pdf) == 0:
            raise ValueError(f"File vuoto: {pdf}")

    # 2. Unisci i PDF in un buffer temporaneo
    temp_buffer = io.BytesIO()
    merger = PdfMerger()

    try:
        for pdf in pdf_files:
            with open(pdf, 'rb') as f:
                merger.append(f)
        merger.write(temp_buffer)
    finally:
        merger.close()

    # 3. Prepara la numerazione delle pagine
    temp_buffer.seek(0)
    reader = PdfReader(temp_buffer)
    total_pages = len(reader.pages)

    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    for i in range(total_pages):
        can.setFont("Helvetica", 9)
        can.drawString(540, 20, f"{start_page + i}")
        can.showPage()
    can.save()

    # 4. Fonde la numerazione con il PDF
    packet.seek(0)
    number_pdf = PdfReader(packet)

    if len(number_pdf.pages) != total_pages:
        raise ValueError("Mancata corrispondenza nel numero di pagine")

    writer = PdfWriter()
    for i in range(total_pages):
        page = reader.pages[i]
        page.merge_page(number_pdf.pages[i])
        writer.add_page(page)

    # 5. Salva il risultato finale
    with open(output_path, 'wb') as f:
        writer.write(f)


def get_sort_key(filepath: str, priority: dict) -> int:
    """
    Estrae il numero iniziale dal nome del file e restituisce la priorità corrispondente.

    Args:
        filepath: Percorso del file (es. "/cartella/10_report.html.png")
        priority: Dizionario {numero: indice_priorità} (es. {10: 0, 49: 1})

    Returns:
        int: Indice di priorità (o infinito se il numero non è nel dizionario)

    Example:
        >>> priority = {10: 0, 49: 1}
        >>> get_sort_key("/path/10_file.html.png", priority)
        0
        >>> get_sort_key("/path/99_file.html.png", priority)
        inf
    """
    filename = os.path.basename(filepath)
    match = re.search(r'^(\d+)', filename)  # Cattura numeri all'inizio del nome

    if match:
        num = int(match.group(1))
        return priority.get(num, float('inf'))  # Restituisce la priorità o infinito se non trovato

    return float('inf')  # Caso fallback per file senza numero

def merge_all (input_file, output_folder, start_page: int = 13):
    # prende l'ordine arbitrario delle stazioni per comporre il file PDF unito
    custom_order = get_custom_order_for_airport(input_file)
    priority = {num: idx for idx, num in enumerate(custom_order)}

    image_files_list = sorted(
        glob.glob(os.path.join(output_folder, "*.html.png")),
        key=lambda x: get_sort_key(x, priority)  # Passa `priority` come argomento
    )

    # Estrai il nome base (senza estensioni) e ricostruisci i percorsi
    lista_base_nomi = [
        os.path.join(output_folder, os.path.splitext(os.path.splitext(f)[0])[0] + ".stats.html")
        for f in image_files_list
    ]

    lista_report = [
        os.path.join(output_folder, os.path.splitext(os.path.splitext(f)[0])[0] + ".pdf")
        for f in image_files_list
    ]

    # Crea elenco_file e genera i PDF
    elenco_file = [[img, base] for img, base in zip(image_files_list, lista_base_nomi)]
    for base_html, output_pdf, image_file in zip(lista_base_nomi, lista_report, image_files_list):
        convert_html_to_pdf_with_image(base_html, output_pdf, image_file)
    # Merge dei file a partire da start_page

    final_output = os.path.join(output_folder, "Allegato_completo.pdf")
    try:
        merge_pdfs_with_page_numbers(lista_report, final_output, start_page)
    except Exception as e:
        print(f"Errore durante il merge dei file pdf: {str(e)}")
        # Cancella file inutili
    for file_da_cancellare in lista_base_nomi:
            try:
                os.remove(file_da_cancellare)
                print(f"File {file_da_cancellare} cancellato con successo.")
            except FileNotFoundError:
                print(f"File {file_da_cancellare} non trovato.")
            except Exception as e:
                print(f"Errore durante la cancellazione del file {file_da_cancellare}: {e}")

