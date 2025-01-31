import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from model import BudzetModel, Transakcja
from observer import Dochod, Wydatek, Cel
from adapter import IExporter, EksporterCSV, EksporterJSON
from builder import TransakcjaBuilder


##########################################
# Warstwa logiki (serwis)
##########################################

class BudzetService:
    def __init__(self, model: BudzetModel) -> None:
        self.model = model
        self.data_dir = 'data'
        self.users_dir = os.path.join(self.data_dir, 'users')
        self.exports_dir = os.path.join(self.data_dir, 'exports')
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.users_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)

        self.uzytkownicy_plik: str = os.path.join(self.users_dir, 'uzytkownicy.json')
        self.dochod = Dochod()
        self.wydatek = Wydatek()
        self.plik_danych: Optional[str] = None
        self.plik_limity: Optional[str] = None

    def zaloguj(self, login: str, haslo: str) -> bool:
        if not self.model.uzytkownicy:
            self.model.uzytkownicy = self.wczytaj_uzytkownikow()

        if login in self.model.uzytkownicy and self.model.uzytkownicy[login] == haslo:
            self.model.zalogowany_uzytkownik = login
            user_dir = os.path.join(self.users_dir, login)
            os.makedirs(user_dir, exist_ok=True)
            self.plik_danych = os.path.join(user_dir, 'dane.json')
            self.plik_limity = os.path.join(user_dir, 'limity.json')
            self.model.cel_oszczedzania = Cel(10000.0, login)
            self.dochod.dodaj(self.model.cel_oszczedzania)
            self.wydatek.dodaj(self.model.cel_oszczedzania)
            self.wczytaj_dane()
            self.wczytaj_limity()
            self.oblicz_wydatki_kategorie()
            self.oblicz_przychody_kategorie()
            return True
        return False

    def zarejestruj(self, login: str, haslo: str) -> bool:
        if not self.model.uzytkownicy:
            self.model.uzytkownicy = self.wczytaj_uzytkownikow()

        if login not in self.model.uzytkownicy:
            self.model.uzytkownicy[login] = haslo
            self.zapisz_uzytkownikow()
            return True
        return False

    def wczytaj_uzytkownikow(self) -> Dict[str, str]:
        if os.path.exists(self.uzytkownicy_plik):
            try:
                with open(self.uzytkownicy_plik, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                return {}
        return {}

    def zapisz_uzytkownikow(self) -> None:
        os.makedirs(os.path.dirname(self.uzytkownicy_plik), exist_ok=True)
        try:
            with open(self.uzytkownicy_plik, 'w', encoding='utf-8') as f:
                json.dump(self.model.uzytkownicy, f, ensure_ascii=False, indent=4)
        except IOError:
            pass

    def dodaj_transakcje(self, transakcja: Transakcja) -> None:
        self.model.transakcje.append(transakcja)
        if transakcja.typ.lower() == 'wydatek':
            self.model.wydatki_kategorie[transakcja.kategoria] = \
                self.model.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.wydatek.dodajWydatek(transakcja.kwota)
        elif transakcja.typ.lower() == 'przychód':
            self.model.przychody_kategorie[transakcja.kategoria] = \
                self.model.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.dochod.dodajDochod(transakcja.kwota)
        self.zapisz_dane()

    def edytuj_transakcje(self, indeks: int, nowa_transakcja: Transakcja) -> bool:
        if 0 <= indeks < len(self.model.transakcje):
            stara = self.model.transakcje[indeks]
            if stara.typ.lower() == 'wydatek':
                self.model.wydatki_kategorie[stara.kategoria] -= stara.kwota
                if self.model.wydatki_kategorie[stara.kategoria] <= 0:
                    del self.model.wydatki_kategorie[stara.kategoria]
            elif stara.typ.lower() == 'przychód':
                self.model.przychody_kategorie[stara.kategoria] -= stara.kwota
                if self.model.przychody_kategorie[stara.kategoria] <= 0:
                    del self.model.przychody_kategorie[stara.kategoria]

            if nowa_transakcja.typ.lower() == 'wydatek':
                self.model.wydatki_kategorie[nowa_transakcja.kategoria] = \
                    self.model.wydatki_kategorie.get(nowa_transakcja.kategoria, 0) + nowa_transakcja.kwota
                self.wydatek.dodajWydatek(nowa_transakcja.kwota)
            elif nowa_transakcja.typ.lower() == 'przychód':
                self.model.przychody_kategorie[nowa_transakcja.kategoria] = \
                    self.model.przychody_kategorie.get(nowa_transakcja.kategoria, 0) + nowa_transakcja.kwota
                self.dochod.dodajDochod(nowa_transakcja.kwota)

            self.model.transakcje[indeks] = nowa_transakcja
            self.zapisz_dane()
            return True
        return False

    def usun_transakcje(self, indeks: int) -> bool:
        if 0 <= indeks < len(self.model.transakcje):
            transakcja = self.model.transakcje.pop(indeks)
            if transakcja.typ.lower() == 'wydatek':
                self.model.wydatki_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.model.wydatki_kategorie[transakcja.kategoria] <= 0:
                    del self.model.wydatki_kategorie[transakcja.kategoria]
                self.wydatek.dodajWydatek(-transakcja.kwota)
            elif transakcja.typ.lower() == 'przychód':
                self.model.przychody_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.model.przychody_kategorie[transakcja.kategoria] <= 0:
                    del self.model.przychody_kategorie[transakcja.kategoria]
                self.dochod.dodajDochod(-transakcja.kwota)
            self.zapisz_dane()
            return True
        return False

    def zapisz_dane(self) -> None:
        if self.plik_danych:
            os.makedirs(os.path.dirname(self.plik_danych), exist_ok=True)
            try:
                dane = [t.to_dict() for t in self.model.transakcje]
                with open(self.plik_danych, 'w', encoding='utf-8') as f:
                    json.dump(dane, f, ensure_ascii=False, indent=4)
            except IOError:
                pass

    def wczytaj_dane(self) -> None:
        if self.plik_danych and os.path.exists(self.plik_danych):
            try:
                with open(self.plik_danych, 'r', encoding='utf-8') as f:
                    dane = json.load(f)
                    self.model.transakcje = [Transakcja(**t) for t in dane]
            except (IOError, json.JSONDecodeError):
                self.model.transakcje = []
        else:
            self.model.transakcje = []

    def wczytaj_limity(self) -> None:
        if self.plik_limity and os.path.exists(self.plik_limity):
            try:
                with open(self.plik_limity, 'r', encoding='utf-8') as f:
                    self.model.limity = json.load(f)
            except (IOError, json.JSONDecodeError):
                self.model.limity = {}
        else:
            self.model.limity = {}

    def zapisz_limity(self) -> None:
        if self.plik_limity:
            os.makedirs(os.path.dirname(self.plik_limity), exist_ok=True)
            try:
                with open(self.plik_limity, 'w', encoding='utf-8') as f:
                    json.dump(self.model.limity, f, ensure_ascii=False, indent=4)
            except IOError:
                pass

    def ustaw_limit(self, kategoria: str, limit: float) -> None:
        self.model.limity[kategoria] = limit
        self.zapisz_limity()

    def pobierz_limit(self, kategoria: str) -> Optional[float]:
        return self.model.limity.get(kategoria)

    def usun_limit(self, kategoria: str) -> bool:
        if kategoria in self.model.limity:
            del self.model.limity[kategoria]
            self.zapisz_limity()
            return True
        return False

    def sprawdz_limit(self, kategoria: str, kwota: float) -> bool:
        limit = self.pobierz_limit(kategoria)
        if limit is None:
            return True
        wydatki = self.model.wydatki_kategorie.get(kategoria, 0)
        return (wydatki + kwota) <= limit

    def oblicz_saldo(self) -> float:
        return sum(
            t.kwota if t.typ.lower() == 'przychód' else -t.kwota
            for t in self.model.transakcje
        )

    def oblicz_wydatki_kategorie(self) -> None:
        self.model.wydatki_kategorie = {}
        for t in self.model.transakcje:
            if t.typ.lower() == 'wydatek':
                self.model.wydatki_kategorie[t.kategoria] = \
                    self.model.wydatki_kategorie.get(t.kategoria, 0) + t.kwota

    def oblicz_przychody_kategorie(self) -> None:
        self.model.przychody_kategorie = {}
        for t in self.model.transakcje:
            if t.typ.lower() == 'przychód':
                self.model.przychody_kategorie[t.kategoria] = \
                    self.model.przychody_kategorie.get(t.kategoria, 0) + t.kwota

    def generuj_raport_wydatkow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.model.transakcje:
            if t.typ.lower() == 'wydatek':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        return raport

    def generuj_raport_przychodow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.model.transakcje:
            if t.typ.lower() == 'przychód':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        return raport

    def eksportuj_do_csv(self, nazwa_pliku: str) -> None:
        dane = [t.to_dict() for t in self.model.transakcje]
        eksporter = EksporterCSV()
        eksporter.eksportuj(dane, nazwa_pliku)

    def eksportuj_do_json(self, nazwa_pliku: str) -> None:
        dane = [t.to_dict() for t in self.model.transakcje]
        eksporter = EksporterJSON()
        eksporter.eksportuj(dane, nazwa_pliku)

    def importuj_z_csv(self, nazwa_pliku: str) -> bool:
        if os.path.exists(nazwa_pliku):
            try:
                with open(nazwa_pliku, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        transakcja = (
                            TransakcjaBuilder()
                            .set_kwota(float(row['kwota']))
                            .set_kategoria(row['kategoria'])
                            .set_typ(row['typ'])
                            .set_opis(row.get('opis', ''))
                            .set_data(row.get('data', datetime.now().strftime('%Y-%m-%d')))
                            .build()
                        )
                        self.model.transakcje.append(transakcja)
                        if transakcja.typ.lower() == 'wydatek':
                            self.model.wydatki_kategorie[transakcja.kategoria] = \
                                self.model.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.wydatek.dodajWydatek(transakcja.kwota)
                        else:
                            self.model.przychody_kategorie[transakcja.kategoria] = \
                                self.model.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.dochod.dodajDochod(transakcja.kwota)
                self.zapisz_dane()
                return True
            except (IOError, ValueError):
                return False
        return False

    def importuj_z_json(self, nazwa_pliku: str) -> bool:
        if os.path.exists(nazwa_pliku):
            try:
                with open(nazwa_pliku, 'r', encoding='utf-8') as f:
                    dane = json.load(f)
                    for rekord in dane:
                        transakcja = (
                            TransakcjaBuilder()
                            .set_kwota(float(rekord['kwota']))
                            .set_kategoria(rekord['kategoria'])
                            .set_typ(rekord['typ'])
                            .set_opis(rekord.get('opis', ''))
                            .set_data(rekord.get('data', datetime.now().strftime('%Y-%m-%d')))
                            .build()
                        )
                        self.model.transakcje.append(transakcja)
                        if transakcja.typ.lower() == 'wydatek':
                            self.model.wydatki_kategorie[transakcja.kategoria] = \
                                self.model.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.wydatek.dodajWydatek(transakcja.kwota)
                        else:
                            self.model.przychody_kategorie[transakcja.kategoria] = \
                                self.model.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.dochod.dodajDochod(transakcja.kwota)
                self.zapisz_dane()
                return True
            except (IOError, json.JSONDecodeError):
                return False
        return False
