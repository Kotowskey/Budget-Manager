# model.py
import json
import os
from datetime import datetime
import csv

class Transakcja:
    def __init__(self, kwota, kategoria, typ, opis="", data=None):
        self.kwota = kwota
        self.kategoria = kategoria
        self.typ = typ  # 'przychód' lub 'wydatek'
        self.opis = opis
        self.data = data if data else datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            'kwota': self.kwota,
            'kategoria': self.kategoria,
            'typ': self.typ,
            'opis': self.opis,
            'data': self.data
        }

class BudzetModel:
    def __init__(self):
        self.transakcje = []
        self.plik_danych = 'dane.json'
        self.plik_limity = 'limity.json'
        self.limity = {}
        self.wczytaj_dane()
        self.wczytaj_limity()

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

    def oblicz_saldo(self):
        saldo = 0
        for t in self.transakcje:
            if t.typ.lower() == 'przychód':
                saldo += t.kwota
            elif t.typ.lower() == 'wydatek':
                saldo -= t.kwota
        return saldo

    def filtruj_transakcje_po_dacie(self, start_date, end_date):
        return [
            t for t in self.transakcje
            if start_date <= t.data <= end_date
        ]

    def eksportuj_do_csv(self, nazwa_pliku='transakcje.csv'):
        with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['kwota', 'kategoria', 'typ', 'opis', 'data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for t in self.transakcje:
                writer.writerow(t.to_dict())

    def wczytaj_limity(self):
        if os.path.exists(self.plik_limity):
            with open(self.plik_limity, 'r', encoding='utf-8') as plik:
                self.limity = json.load(plik)
        else:
            self.limity = {}

    def zapisz_limity(self):
        with open(self.plik_limity, 'w', encoding='utf-8') as plik:
            json.dump(self.limity, plik, ensure_ascii=False, indent=4)

    def ustaw_limit(self, kategoria, limit):
        self.limity[kategoria] = limit
        self.zapisz_limity()

    def pobierz_limit(self, kategoria):
        return self.limity.get(kategoria, None)

    def sprawdz_limit(self, kategoria):
        limit = self.pobierz_limit(kategoria)
        if limit is None:
            return True  # Brak limitu
        # Oblicz miesięczne wydatki dla danej kategorii
        current_month = datetime.now().strftime('%Y-%m')
        wydatki = sum(
            t.kwota for t in self.transakcje
            if t.typ.lower() == 'wydatek' and
               t.kategoria == kategoria and
               t.data.startswith(current_month)
        )
        return wydatki + 0.0001 <= limit  # Dodaj mały margines

