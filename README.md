# Verifica Eventi Acustici - Analisi e Reportistica

Questo repository contiene script Python per l'analisi e la reportistica di dati relativi alla verifica di eventi acustici.

## Contenuti

1.  **`verifica_eventi_lib/eventi.py`**: Script per l'elaborazione di file di dati e la generazione di un DataFrame contenente informazioni sugli eventi acustici.
2.  **`verifica_eventi_lib/report_eventi.py`**: Script per la creazione di report PDF combinando un'immagine PNG e dati tabellari da un file HTML.
3.  **`main.py`**: Script principale per l'esecuzione sequenziale di `eventi.py` e `report_eventi.py`.

---
### Prerequisiti
- Installare requirements (sono state inserite le versioni funzionanti)
- Installare orca e assicurarsi che sia nel PATH (vedi https://github.com/plotly/orca/releases)

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
* Crea una pagina HTML con il grafico delle timehistory esplorabile con plotly: la codifica è `<id_stazione>_output_events.html`

### Come Utilizzare

Il file di input che contiene tutte le informazioni può essere passato come argomento del file oppure può essere inserito manualmente in fase di esecuzione. Anche la cartella di destinazione dei file PDF può essere passata come argomento oppure viene richiesta in fase di esecuzione.

**Esempio di file di input**

Nome;id;file_staz;file_ARPA;thr;dur;lag  
Arsago Cimitero;10;./Dati_SEA/1009122024.his.txt;Arsago Cimitero 2024.txt;62;17;0  
Casorate - V. M. Rosa;49;./Dati_SEA/4909122024.his.txt;misura_ARPA_Monterosa_9_12_24.txt;58;20;0  
Ferno - via Moncucco;6;./Dati_SEA/0604122024.his.txt;Ferno 2024.txt;60;10;0  
Lonate Cimitero (MM);1505;./Dati_SEA/150504122024.his.txt;misura_ARPA_Lonate_cimitero_4_12_24.txt;67;9;0  
Lonate - via S. Savina;8;./Dati_SEA/0804122024.his.txt;misura_ARPA_Lonate_SSavina_4_12_24.txt;63;10;0  
S. Savina Mobile;1518;;;  
Somma - Morgampo;1519;./Dati_SEA/Temporanea/151910122024.his.txt;misura_ARPA_Morgampo_10_12_24.txt;62;22;0  
Somma - V. Cabagaggio;45;./Dati_SEA/4517092024.his.txt;misura_ARPA_Cabagaggio_17_9_24.txt;60;22;0  
Somma - Maddalena;24;./Dati_SEA/2417092024.his.txt;misura_ARPA_Maddalena_17_9_24.txt;58;20;0  
Somma - Magazzino;3;./Dati_SEA/0309122024.his.txt;misura_ARPA_Magazzino_9_12_24;62;20;0  
Somma - Rodari;1;;;  
Turbigo - Via Plati;1515;./Dati_SEA/151509122024.his.txt;Turbigo 2024.txt;55;8;0  

*NOTA: per quanto riguarda il lag, conviene prima generare tutti i grafici con lag=0 e poi determinare il lag per 
ciascuna stazione*

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


**TODO**
- automatizzare la ricerca di delay tra timehistory
- verificare la possibilità di elaborare file nella intranet
---

Questo README fornisce una panoramica degli script Python presenti nel repository e le istruzioni di base per il loro utilizzo. Per dettagli più specifici sul codice o sulle dipendenze, si rimanda ai commenti all'interno dei file Python stessi.