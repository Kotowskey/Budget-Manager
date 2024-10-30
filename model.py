import json
import os

class Transakcja:
    def __init__(self, kwota, kategoria, typ, opis=""):
        self.kwota = kwota
        self.kategoria = kategoria
        self.typ = typ  # 'przychód' lub 'wydatek'
        self.opis = opis

    def to_dict(self):
        return {
            'kwota': self.kwota,
            'kategoria': self.kategoria,
            'typ': self.typ,
            'opis': self.opis
        }

class BudzetModel:
    def __init__(self):
        self.transakcje = []
        self.plik_danych = 'dane.json'
        self.wczytaj_dane()

    def dodaj_transakcje(self, transakcja):
        self.transakcje.append(transakcja)
        self.zapisz_dane()

    def usun_transakcje(self, indeks):
        if 0 <= indeks < len(self.transakcje):
            del self.transakcje[indeks]
            self.zapisz_dane()

    def edytuj_transakcje(self, indeks, transakcja):
        if 0 <= indeks < len(self.transakcje):
            self.transakcje[indeks] = transakcja
            self.zapisz_dane()

    def zapisz_dane(self):
        dane = [t.to_dict() for t in self.transakcje]
        with open(self.plik_danych, 'w', encoding='utf-8') as plik:
            json.dump(dane, plik, ensure_ascii=False, indent=4)

    def wczytaj_dane(self):
        if os.path.exists(self.plik_danych):
            with open(self.plik_danych, 'r', encoding='utf-8') as plik:
                dane = json.load(plik)
                self.transakcje = [Transakcja(**t) for t in dane]
        else:
            self.transakcje = []
