# verifica_eventi
 compara gli eventi da file his e da altri file ARPA
# Event Detection and Analysis

This repository contains Python code for detecting and analyzing events based on sound level data. The code reads a file with sound level measurements, identifies events where the sound level exceeds a specified threshold for a certain duration, and calculates various metrics for each event.

## Features

- Identify events based on sound level threshold and duration.
- Calculate Sound Exposure Level (SEL), equivalent sound level (LAeq), and maximum sound level (LMax) for each event.
- Save results to a CSV file.

## Usage

1. **Identify Events**: The `identify_events` function reads the input file and identifies events based on the specified threshold and duration.
2. **Calculate Event Values**: The `calculate_event_values` function calculates SEL, LAeq, and LMax for each event.
3. **Save Results**: The `save_results_to_csv` function saves the calculated values to a CSV file.