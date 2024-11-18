# model.py
import json
import os
from datetime import datetime
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import logging

# Konfiguracja logowania
logging.basicConfig(
    filename='budzet_app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class Transakcja:
    kwota: float
    kategoria: str
    typ: str  # 'przychód' lub 'wydatek'
    opis: str = ""
    data: str = datetime.now().strftime('%Y-%m-%d')

    def to_dict(self) -> Dict:
        return asdict(self)

class BudzetModel:
    def __init__(self):
        self.transakcje: List[Transakcja] = []
        self.uzytkownicy_plik: str = 'uzytkownicy.json'
        self.limity: Dict[str, float] = {}
        self.wydatki_kategorie: Dict[str, float] = {}
        self.przychody_kategorie: Dict[str, float] = {}
        self.zalogowany_uzytkownik: Optional[str] = None
        self.uzytkownicy: Dict[str, str] = self.wczytaj_uzytkownikow()
        logging.info("Inicjalizacja modelu budżetu zakończona.")

    def zaloguj(self, login: str, haslo: str) -> bool:
        if login in self.uzytkownicy and self.uzytkownicy[login] == haslo:
            self.zalogowany_uzytkownik = login
            self.plik_danych = f'dane_{login}.json'
            self.plik_limity = f'limity_{login}.json'
            self.wczytaj_dane()
            self.wczytaj_limity()
            self.oblicz_wydatki_kategorie()
            self.oblicz_przychody_kategorie()
            logging.info(f"Zalogowano użytkownika: {login}")
            return True
        logging.warning(f"Nieudane logowanie dla użytkownika: {login}")
        return False

    def zarejestruj(self, login: str, haslo: str) -> bool:
        if login not in self.uzytkownicy:
            self.uzytkownicy[login] = haslo
            self.zapisz_uzytkownikow()
            logging.info(f"Zarejestrowano nowego użytkownika: {login}")
            return True
        logging.warning(f"Próba rejestracji istniejącego użytkownika: {login}")
        return False

    def wczytaj_uzytkownikow(self) -> Dict[str, str]:
        if os.path.exists(self.uzytkownicy_plik):
            try:
                with open(self.uzytkownicy_plik, 'r', encoding='utf-8') as plik:
                    uzytkownicy = json.load(plik)
                return uzytkownicy
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Błąd wczytywania użytkowników: {e}")
                return {}
        else:
            return {}

    def zapisz_uzytkownikow(self) -> None:
        try:
            with open(self.uzytkownicy_plik, 'w', encoding='utf-8') as plik:
                json.dump(self.uzytkownicy, plik, ensure_ascii=False, indent=4)
            logging.debug("Użytkownicy zapisani do pliku.")
        except IOError as e:
            logging.error(f"Błąd zapisu użytkowników: {e}")

    def dodaj_transakcje(self, transakcja: Transakcja) -> None:
        self.transakcje.append(transakcja)
        if transakcja.typ.lower() == 'wydatek':
            self.wydatki_kategorie[transakcja.kategoria] = self.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
        elif transakcja.typ.lower() == 'przychód':
            self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
        self.zapisz_dane()
        logging.info(f"Dodano transakcję: {transakcja}")

    def usun_transakcje(self, indeks: int) -> bool:
        if 0 <= indeks < len(self.transakcje):
            transakcja = self.transakcje.pop(indeks)
            if transakcja.typ.lower() == 'wydatek':
                self.wydatki_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.wydatki_kategorie[transakcja.kategoria] <= 0:
                    del self.wydatki_kategorie[transakcja.kategoria]
            elif transakcja.typ.lower() == 'przychód':
                self.przychody_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.przychody_kategorie[transakcja.kategoria] <= 0:
                    del self.przychody_kategorie[transakcja.kategoria]
            self.zapisz_dane()
            logging.info(f"Usunięto transakcję: {transakcja}")
            return True
        logging.warning(f"Próba usunięcia nieistniejącej transakcji o indeksie: {indeks}")
        return False

    def edytuj_transakcje(self, indeks: int, transakcja: Transakcja) -> bool:
        if 0 <= indeks < len(self.transakcje):
            transakcja_stara = self.transakcje[indeks]
            if transakcja_stara.typ.lower() == 'wydatek':
                self.wydatki_kategorie[transakcja_stara.kategoria] -= transakcja_stara.kwota
                if self.wydatki_kategorie[transakcja_stara.kategoria] <= 0:
                    del self.wydatki_kategorie[transakcja_stara.kategoria]
            elif transakcja_stara.typ.lower() == 'przychód':
                self.przychody_kategorie[transakcja_stara.kategoria] -= transakcja_stara.kwota
                if self.przychody_kategorie[transakcja_stara.kategoria] <= 0:
                    del self.przychody_kategorie[transakcja_stara.kategoria]
            if transakcja.typ.lower() == 'wydatek':
                self.wydatki_kategorie[transakcja.kategoria] = self.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            elif transakcja.typ.lower() == 'przychód':
                self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.transakcje[indeks] = transakcja
            self.zapisz_dane()
            logging.info(f"Edytowano transakcję na indeksie {indeks}: {transakcja}")
            return True
        logging.warning(f"Próba edycji nieistniejącej transakcji o indeksie: {indeks}")
        return False

    def zapisz_dane(self) -> None:
        dane = [t.to_dict() for t in self.transakcje]
        try:
            with open(self.plik_danych, 'w', encoding='utf-8') as plik:
                json.dump(dane, plik, ensure_ascii=False, indent=4)
            logging.debug("Dane zapisane do pliku.")
        except IOError as e:
            logging.error(f"Błąd zapisu danych: {e}")

    def wczytaj_dane(self) -> None:
        if os.path.exists(self.plik_danych):
            try:
                with open(self.plik_danych, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    self.transakcje = [Transakcja(**t) for t in dane]
                logging.debug("Dane wczytane z pliku.")
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Błąd wczytywania danych: {e}")
                self.transakcje = []
        else:
            self.transakcje = []
            logging.debug("Plik danych nie istnieje. Inicjalizacja pustej listy transakcji.")

    def oblicz_saldo(self) -> float:
        saldo = sum(t.kwota if t.typ.lower() == 'przychód' else -t.kwota for t in self.transakcje)
        logging.debug(f"Obliczone saldo: {saldo}")
        return saldo

    def filtruj_transakcje_po_dacie(self, start_date: str, end_date: str) -> List[Transakcja]:
        filtrowane = [
            t for t in self.transakcje
            if start_date <= t.data <= end_date
        ]
        logging.debug(f"Filtrowano transakcje od {start_date} do {end_date}: {len(filtrowane)} znalezionych.")
        return filtrowane

    def eksportuj_do_csv(self, nazwa_pliku: str = 'transakcje.csv') -> None:
        try:
            with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['kwota', 'kategoria', 'typ', 'opis', 'data']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for t in self.transakcje:
                    writer.writerow(t.to_dict())
            logging.info(f"Transakcje wyeksportowane do pliku CSV: {nazwa_pliku}")
        except IOError as e:
            logging.error(f"Błąd eksportu do CSV: {e}")

    def importuj_z_csv(self, nazwa_pliku: str = 'transakcje.csv') -> bool:
        if os.path.exists(nazwa_pliku):
            try:
                with open(nazwa_pliku, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        transakcja = Transakcja(
                            kwota=float(row['kwota']),
                            kategoria=row['kategoria'],
                            typ=row['typ'],
                            opis=row.get('opis', ''),
                            data=row.get('data', datetime.now().strftime('%Y-%m-%d'))
                        )
                        self.transakcje.append(transakcja)
                        if transakcja.typ.lower() == 'wydatek':
                            self.wydatki_kategorie[transakcja.kategoria] = self.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                        elif transakcja.typ.lower() == 'przychód':
                            self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                self.zapisz_dane()
                logging.info(f"Transakcje zaimportowane z pliku CSV: {nazwa_pliku}")
                return True
            except (IOError, ValueError) as e:
                logging.error(f"Błąd importu z CSV: {e}")
                return False
        else:
            logging.warning(f"Plik CSV do importu nie istnieje: {nazwa_pliku}")
            return False

    def wczytaj_limity(self) -> None:
        if os.path.exists(self.plik_limity):
            try:
                with open(self.plik_limity, 'r', encoding='utf-8') as plik:
                    self.limity = json.load(plik)
                logging.debug("Limity wczytane z pliku.")
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Błąd wczytywania limitów: {e}")
                self.limity = {}
        else:
            self.limity = {}
            logging.debug("Plik limitów nie istnieje. Inicjalizacja pustych limitów.")

    def zapisz_limity(self) -> None:
        try:
            with open(self.plik_limity, 'w', encoding='utf-8') as plik:
                json.dump(self.limity, plik, ensure_ascii=False, indent=4)
            logging.debug("Limity zapisane do pliku.")
        except IOError as e:
            logging.error(f"Błąd zapisu limitów: {e}")

    def ustaw_limit(self, kategoria: str, limit: float) -> None:
        self.limity[kategoria] = limit
        self.zapisz_limity()
        logging.info(f"Ustawiono limit dla kategorii '{kategoria}': {limit} zł")

    def pobierz_limit(self, kategoria: str) -> Optional[float]:
        limit = self.limity.get(kategoria)
        logging.debug(f"Pobrano limit dla kategorii '{kategoria}': {limit}")
        return limit

    def usun_limit(self, kategoria: str) -> bool:
        if kategoria in self.limity:
            del self.limity[kategoria]
            self.zapisz_limity()
            logging.info(f"Usunięto limit dla kategorii '{kategoria}'")
            return True
        else:
            logging.warning(f"Próba usunięcia nieistniejącego limitu dla kategorii '{kategoria}'")
            return False

    def sprawdz_limit(self, kategoria: str, kwota: float) -> bool:
        limit = self.pobierz_limit(kategoria)
        if limit is None:
            logging.debug(f"Brak limitu dla kategorii '{kategoria}'.")
            return True  # Brak limitu
        wydatki = self.wydatki_kategorie.get(kategoria, 0)
        sprawdzony = (wydatki + kwota) <= limit
        logging.debug(f"Sprawdzanie limitu dla '{kategoria}': {wydatki} + {kwota} <= {limit} -> {sprawdzony}")
        return sprawdzony

    def generuj_raport_wydatkow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.transakcje:
            if t.typ.lower() == 'wydatek':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        logging.debug("Generowanie raportu wydatków zakończone.")
        return raport

    def generuj_raport_przychodow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.transakcje:
            if t.typ.lower() == 'przychód':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        logging.debug("Generowanie raportu przychodów zakończone.")
        return raport

    def oblicz_wydatki_kategorie(self) -> None:
        self.wydatki_kategorie = {}
        for t in self.transakcje:
            if t.typ.lower() == 'wydatek':
                self.wydatki_kategorie[t.kategoria] = self.wydatki_kategorie.get(t.kategoria, 0) + t.kwota
        logging.debug("Obliczono wydatki dla każdej kategorii.")

    def oblicz_przychody_kategorie(self) -> None:
        self.przychody_kategorie = {}
        for t in self.transakcje:
            if t.typ.lower() == 'przychód':
                self.przychody_kategorie[t.kategoria] = self.przychody_kategorie.get(t.kategoria, 0) + t.kwota
        logging.debug("Obliczono przychody dla każdej kategorii.")
