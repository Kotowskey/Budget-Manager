import csv
import json
from abc import ABC, abstractmethod
from typing import List, Dict

##########################################
# Eksporter CSV / JSON (Adapter)
##########################################

class IExporter(ABC):
    @abstractmethod
    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        pass

class EksporterCSV(IExporter):
    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        try:
            with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
                if dane and len(dane) > 0:
                    fieldnames = dane[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(dane)
        except IOError as e:
            raise

class EksporterJSON(IExporter):
    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        try:
            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(dane, plik, ensure_ascii=False, indent=4)
        except IOError as e:
            raise
