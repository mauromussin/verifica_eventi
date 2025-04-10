# verifica_eventi
 compara gli eventi da file his e da altri file ARPA
# Event Detection and Analysis

This repository contains Python code for detecting and analyzing events based on sound level data. The code reads a file with sound level measurements, identifies events where the sound level exceeds a specified threshold for a certain duration, and calculates various metrics for each event.
# Verifica Eventi Acustici - Analisi e Reportistica

Questo repository contiene due script Python per l'analisi e la reportistica di dati relativi alla verifica di eventi acustici.

## Contenuti

1.  **`report_eventi.py`**: Script per la creazione di report PDF combinando un'immagine PNG e dati tabellari da un file HTML.
2.  **`analisi_distribuzioni.py`**: Script per confrontare statisticamente le distribuzioni di parametri acustici tra diverse sorgenti (Gestore vs. ARPA) e generare un report HTML con tabelle e risultati di test statistici.

---

## `report_eventi.py`

Questo script Python ha lo scopo di generare un file PDF contenente un'immagine (tipicamente un grafico) e una tabella di dati. Prende in input un file immagine PNG e un file HTML contenente una tabella.

### Funzionalità

* **Inserimento Immagine:** Inserisce un'immagine PNG centrata nella prima metà di un foglio A4 del PDF.
* **Inserimento Tabella HTML:** Converte e inserisce la tabella contenuta nel file HTML nella seconda metà del PDF, mantenendo la formattazione di base della tabella HTML.
* **Formattazione di Base:** Imposta una dimensione del font di 10 punti per il testo nel PDF.
* **Unione Elementi:** Combina l'immagine e la tabella HTML in un unico file PDF.
* **Automazione:** Permette di processare più coppie di file immagine (`.html.png`) e dati (`.stats.html`) presenti nella stessa directory, generando un report PDF per ciascuna coppia.

### Come Utilizzare

1.  Assicurarsi di avere installato le librerie necessarie: `pdfkit`, `reportlab`, `PyPDF2`, e `Pillow` (`PIL`). Puoi installarle con:
    ```bash
    pip install pdfkit reportlab PyPDF2 Pillow
    ```
    Potrebbe essere necessario installare anche `wkhtmltopdf`. Consulta la documentazione di `pdfkit` per i dettagli sull'installazione specifica per il tuo sistema operativo.
2.  Posizionare i file immagine (`.html.png`) e i file HTML contenenti le tabelle (`.stats.html`) nella stessa directory dello script `report_eventi.py`.
3.  Eseguire lo script `report_eventi.py`:
    ```bash
    python report_eventi.py
    ```
4.  Per ogni coppia di file `<nomefile>.stats.html` e `<nomefile>.html.png` trovata, verrà generato un file PDF chiamato `<nomefile>.report.pdf` nella stessa directory.

---

## `analisi_distribuzioni.py`

Questo script Python analizza un set di dati contenuto in un DataFrame (tipicamente caricato da un file CSV o Excel) per confrontare le distribuzioni di parametri acustici misurati da due diverse fonti: il Gestore e l'ARPA.

### Funzionalità

* **Riordinamento Colonne:** Definisce un ordine specifico per le colonne nel DataFrame.
* **Calcolo Statistiche Descriptive:** Calcola la media e la varianza per le colonne relative ai parametri acustici (`SEL`, `LAeq`, `LMax`) misurati da entrambe le fonti.
* **Test di Kolmogorov-Smirnov:** Applica il test statistico di Kolmogorov-Smirnov per verificare se le distribuzioni delle misurazioni tra il Gestore e l'ARPA per ciascun parametro sono significativamente diverse.
* **Generazione Report HTML:** Crea un file HTML contenente:
    * Una tabella che mostra i dati degli eventi in parallelo.
    * Una tabella riassuntiva con le medie, le varianze, il risultato del test K-S (statistica e p-value) e una conclusione sulla similarità o diversità delle distribuzioni per ciascun parametro acustico confrontato.
* **Etichette Personalizzate:** Utilizza etichette più descrittive per le colonne nella tabella riassuntiva (es. "SEL Gestore" invece di "SEL\_staz").

### Come Utilizzare

1.  Assicurarsi di avere installato le librerie necessarie: `pandas` e `scipy`. Puoi installarle con:
    ```bash
    pip install pandas scipy
    ```
2.  Preparare un file di dati (ad esempio, un CSV o un Excel) che contenga le colonne con i dati degli eventi acustici, inclusi i parametri "SEL\_staz", "LAeq\_staz", "LMax\_staz", "SEL\_ARPA", "LAeq\_ARPA", "LMax\_ARPA".
3.  Modificare lo script `analisi_distribuzioni.py` per caricare correttamente il tuo file di dati nel DataFrame `df`. Ad esempio, se il tuo file è un CSV chiamato `dati_eventi.csv`, potresti usare:
    ```python
    import pandas as pd
    # ...
    df = pd.read_csv('dati_eventi.csv')
    # ...
    ```
4.  Eseguire lo script `analisi_distribuzioni.py`, fornendo il nome desiderato per il file di output (senza estensione) come argomento alla funzione `confronta_distribuzioni`:
    ```bash
    python analisi_distribuzioni.py
    ```
    All'interno dello script dovrai chiamare la funzione, ad esempio:
    ```python
    # Esempio di utilizzo (aggiungere alla fine dello script o in un blocco if __name__ == "__main__":)
    import pandas as pd
    from scipy import stats

    # ... (definizione della funzione confronta_distribuzioni) ...

    if __name__ == "__main__":
        # Carica i tuoi dati qui
        data = {'First Time': [...], 'd': [...], 'SEL_staz': [...], 'LAeq_staz': [...], 'LMax_staz': [...], 'SEL_ARPA': [...], 'LAeq_ARPA': [...], 'LMax_ARPA': [...] }
        df = pd.DataFrame(data)
        output_file_name = "confronto_acustico"
        confronta_distribuzioni(df, output_file_name)
    ```
5.  Verrà generato un file HTML chiamato `<nome_output>.stats.html` nella stessa directory contenente i risultati dell'analisi.

---

Questo README fornisce una panoramica dei due script Python presenti nel repository e le istruzioni di base per il loro utilizzo. Per dettagli più specifici sul codice o sulle dipendenze, si rimanda ai commenti all'interno dei file Python stessi.