import csv
import json
from abc import ABC, abstractmethod
from typing import List, Dict

##########################################
# Wzorzec projektowy: ADAPTER
##########################################

# Interfejs docelowy, który jest oczekiwany przez klienta
class IExporter(ABC):
    @abstractmethod
    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        pass

# Klasa adaptowana (Adaptee) dla formatu CSV
class CsvExporter:
    def export_to_csv(self, dane: List[Dict], nazwa_pliku: str) -> None:
        try:
            with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
                if dane and len(dane) > 0:
                    fieldnames = dane[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(dane)
        except IOError as e:
            raise

# Klasa adaptowana (Adaptee) dla formatu JSON
class JsonExporter:
    def export_to_json(self, dane: List[Dict], nazwa_pliku: str) -> None:
        try:
            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(dane, plik, ensure_ascii=False, indent=4)
        except IOError as e:
            raise

# Adapter dla formatu CSV
class EksporterCSV(IExporter):
    def __init__(self):
        self._csv_exporter = CsvExporter()

    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        self._csv_exporter.export_to_csv(dane, nazwa_pliku)

# Adapter dla formatu JSON
class EksporterJSON(IExporter):
    def __init__(self):
        self._json_exporter = JsonExporter()

    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        self._json_exporter.export_to_json(dane, nazwa_pliku)