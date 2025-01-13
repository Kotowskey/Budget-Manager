import csv
from Eksporter import Eksporter

class EksporterCSV(Eksporter):
    def eksportuj(self, dane):
        try:
            with open("transakcje.csv", mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['kwota', 'kategoria', 'typ', 'opis', 'data']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
               
                for t in dane:
                    writer.writerow({
                        "data": t.data,
                        "kwota": t.kwota,
                        "typ": t.typ,
                        "kategoria": t.kategoria,
                        "opis": t.opis
                    })
            print(f"Transakcje wyeksportowane do pliku CSV.")
        except IOError as e:
            print(f"Błąd eksportu do CSV: {e}")