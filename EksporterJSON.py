import json
from Eksporter import Eksporter

class EksporterJSON(Eksporter):
    def eksportuj(self, dane):
        try:
            with open('transakcje.json', mode='w') as file:
                transakcje_dict = [
                    {
                        "data": transakcja.data,
                        "kwota": transakcja.kwota,
                        "typ": transakcja.typ,
                        "kategoria": transakcja.kategoria,
                        "opis": transakcja.opis
                    }
                    for transakcja in dane
                ]
                json.dump(transakcje_dict, file, indent=4)
            print("Dane zostały zapisane do pliku.")
        except Exception as e:
            print(f"Wystąpił błąd podczas eksportu do JSON: {e}")