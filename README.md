# Verifica Eventi Acustici - Analisi e Reportistica

Questo repository contiene script Python per l'analisi e la reportistica di dati relativi alla verifica di eventi acustici.

## Contenuti

1.  **`verifica_eventi_lib/eventi.py`**: Script per l'elaborazione di file di dati e la generazione di un DataFrame contenente informazioni sugli eventi acustici.
2.  **`verifica_eventi_lib/report_eventi.py`**: Script per la creazione di report PDF combinando un'immagine PNG e dati tabellari da un file HTML.
3.  **`main.py`**: Script principale per l'esecuzione sequenziale di `eventi.py` e `report_eventi.py`.

---

## `verifica_eventi_lib/eventi.py`

Questo script Python ha lo scopo di elaborare un file di dati (ad esempio, un CSV) contenente informazioni sugli eventi acustici e di generare un DataFrame contenente informazioni riassuntive sugli eventi.

### Funzionalità

* Lettura di file di dati in formato CSV.
* Elaborazione dei dati per estrarre informazioni rilevanti sugli eventi acustici.
* Generazione di un DataFrame contenente informazioni riassuntive sugli eventi.

### Come Utilizzare

Le funzioni contenute in questo modulo sono utilizzate dallo script `main.py` per l'elaborazione dei dati.

---

## `verifica_eventi_lib/report_eventi.py`

Questo script Python ha lo scopo di generare un file PDF contenente un'immagine (tipicamente un grafico) e una tabella di dati. Prende in input un file immagine PNG e un file HTML contenente una tabella.

### Funzionalità

* Inserimento Immagine: Inserisce un'immagine PNG centrata nella prima metà di un foglio A4 del PDF.
* Inserimento Tabella HTML: Converte e inserisce la tabella contenuta nel file HTML nella seconda metà del PDF, mantenendo la formattazione di base della tabella HTML.
* Formattazione di Base: Imposta una dimensione del font di 10 punti per il testo nel PDF.
* Unione Elementi: Combina l'immagine e la tabella HTML in un unico file PDF.

### Come Utilizzare

Le funzioni contenute in questo modulo sono utilizzate dallo script `main.py` per la generazione dei report PDF.

---

## `main.py`

Questo script Python contiene le istruzioni principali per eseguire il calcolo degli eventi e la generazione dei report in formato PDF.

### Funzionalità

* Esecuzione sequenziale delle funzioni di `eventi.py` e `report_eventi.py`.
* Gestione dell'input del file di dati e della cartella di output per i report PDF.
* Cancellazione dei file temporanei generati durante l'elaborazione.

### Come Utilizzare

Il file di input che contiene tutte le informazioni può essere passato come argomento del file oppure può essere inserito manualmente in fase di esecuzione. Anche la cartella di destinazione dei file PDF può essere passata come argomento oppure viene richiesta in fase di esecuzione.

**Esempi di esecuzione:**

* `python main.py nome_file_input.csv cartella_output`
* `python main.py nome_file_input.csv` (verrà richiesta la cartella di output in fase di esecuzione)
* `python main.py` (verranno richiesti sia il nome del file di input che la cartella di output in fase di esecuzione)

**Esempi di input in fase di esecuzione:**

* Inserisci la cartella di output per i PDF: `percorso/cartella_output`
* Inserisci il nome del file da elaborare: `nome_file_input.csv`

**Note:**

* Assicurati di avere installato le librerie necessarie: `pandas`, `scipy`, `pdfkit`, `reportlab`, `PyPDF2`, e `Pillow` (`PIL`).
* Potrebbe essere necessario installare anche `wkhtmltopdf`. Consulta la documentazione di `pdfkit` per i dettagli sull'installazione specifica per il tuo sistema operativo.
* I file `.html.png` e `.stats.html` devono trovarsi nella stessa directory di `main.py`.
* I file PDF generati verranno salvati nella cartella di output specificata.
* I file `.stats.html` verranno cancellati dopo la generazione dei PDF.

---

Questo README fornisce una panoramica degli script Python presenti nel repository e le istruzioni di base per il loro utilizzo. Per dettagli più specifici sul codice o sulle dipendenze, si rimanda ai commenti all'interno dei file Python stessi.