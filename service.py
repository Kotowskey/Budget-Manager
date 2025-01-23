import json
import os
import csv
from datetime import datetime
from typing import List, Dict, Optional, Any

from model import BudzetData, Transakcja, Cel, Dochod, Wydatek

###################################
# ADAPTER do eksportu (CSV / JSON)
###################################

class UniwersalnyInterfejsEksportu:
    def eksportuj(self, dane: Any, nazwa_pliku: str) -> None:
        raise NotImplementedError


class EksporterCSV:
    def eksportujDoCSV(self, dane: List[Dict], nazwa_pliku: str) -> None:
        try:
            with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
                if dane and len(dane) > 0:
                    fieldnames = dane[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in dane:
                        writer.writerow(row)
        except IOError as e:
            raise


class EksporterJSON:
    def eksportujDoJSON(self, dane: List[Dict], nazwa_pliku: str) -> None:
        try:
            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(dane, plik, ensure_ascii=False, indent=4)
        except IOError as e:
            raise


class AdapterEksportuCSV(UniwersalnyInterfejsEksportu):
    def __init__(self, eksporter: EksporterCSV) -> None:
        self.eksporter = eksporter

    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        self.eksporter.eksportujDoCSV(dane, nazwa_pliku)


class AdapterEksportuJSON(UniwersalnyInterfejsEksportu):
    def __init__(self, eksporter: EksporterJSON) -> None:
        self.eksporter = eksporter

    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        self.eksporter.eksportujDoJSON(dane, nazwa_pliku)


class EksportDanych:
    """
    Klasa opakowująca różne adaptery eksportu, umożliwia wygodny wybór formatu.
    """
    def __init__(self) -> None:
        self.eksporter: Optional[UniwersalnyInterfejsEksportu] = None
        self.eksporter_csv = AdapterEksportuCSV(EksporterCSV())
        self.eksporter_json = AdapterEksportuJSON(EksporterJSON())

    def ustawEksporter(self, eksporter: UniwersalnyInterfejsEksportu) -> None:
        self.eksporter = eksporter

    def eksportujDane(self, dane: List[Dict], nazwa_pliku: str) -> None:
        if self.eksporter:
            self.eksporter.eksportuj(dane, nazwa_pliku)
        else:
            raise ValueError("Nie ustawiono eksportera.")


#######################################
# BIZNESOWA WARSTWA LOGIKI (SERWIS)
#######################################

class BudzetService:
    def __init__(self, data: BudzetData) -> None:
        """
        W konstruktorze otrzymujemy obiekt BudzetData,
        który przechowuje wewnętrznie wszystkie dane.
        """
        self.data = data
        self.data_dir = 'data'
        self.users_dir = os.path.join(self.data_dir, 'users')
        self.exports_dir = os.path.join(self.data_dir, 'exports')
        self.uzytkownicy_plik: str = os.path.join(self.users_dir, 'uzytkownicy.json')
        self.eksport_danych = EksportDanych()

        # Pola do plików zalogowanego użytkownika
        self.plik_danych: Optional[str] = None
        self.plik_limity: Optional[str] = None

        self.create_directories()

    def create_directories(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.users_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)

    ###################################
    # LOGOWANIE / REJESTRACJA UŻYTK.
    ###################################
    def zaloguj(self, login: str, haslo: str) -> bool:
        # Wczytujemy listę użytkowników, jeżeli jeszcze nie wczytana
        if not self.data.uzytkownicy:
            self.data.uzytkownicy = self.wczytaj_uzytkownikow()

        if login in self.data.uzytkownicy and self.data.uzytkownicy[login] == haslo:
            self.data.zalogowany_uzytkownik = login

            user_dir = os.path.join(self.users_dir, login)
            os.makedirs(user_dir, exist_ok=True)
            self.plik_danych = os.path.join(user_dir, 'dane.json')
            self.plik_limity = os.path.join(user_dir, 'limity.json')

            # Tworzymy domyślny cel (może być wczytany później z pliku)
            cel = Cel(10000.0, login)
            self.data.cel_oszczedzania = cel

            # Podpinamy cel do obiektów Dochod i Wydatek
            self.data.dochod.dodaj(cel)
            self.data.wydatek.dodaj(cel)

            # Wczytujemy dane i limity z plików
            self.wczytaj_dane()
            self.wczytaj_limity()
            self._oblicz_wydatki_kategorie()
            self._oblicz_przychody_kategorie()

            # Wczytanie stanu celu (oszczędności) z pliku
            self.wczytaj_cel()

            return True
        return False

    def zarejestruj(self, login: str, haslo: str) -> bool:
        if not self.data.uzytkownicy:
            self.data.uzytkownicy = self.wczytaj_uzytkownikow()

        if login not in self.data.uzytkownicy:
            self.data.uzytkownicy[login] = haslo
            self.zapisz_uzytkownikow()
            return True
        return False

    def wczytaj_uzytkownikow(self) -> Dict[str, str]:
        if os.path.exists(self.uzytkownicy_plik):
            try:
                with open(self.uzytkownicy_plik, 'r', encoding='utf-8') as plik:
                    return json.load(plik)
            except (IOError, json.JSONDecodeError):
                return {}
        return {}

    def zapisz_uzytkownikow(self) -> None:
        os.makedirs(os.path.dirname(self.uzytkownicy_plik), exist_ok=True)
        try:
            with open(self.uzytkownicy_plik, 'w', encoding='utf-8') as plik:
                json.dump(self.data.uzytkownicy, plik, ensure_ascii=False, indent=4)
        except IOError:
            pass

    ###################################
    # OPERACJE NA DANYCH
    ###################################
    def dodaj_transakcje(self, transakcja: Transakcja) -> None:
        self.data.transakcje.append(transakcja)

        if transakcja.typ.lower() == 'wydatek':
            # Zwiększamy bilans dla kategorii
            self.data.wydatki_kategorie[transakcja.kategoria] = \
                self.data.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            # Powiadamiamy obserwatorów
            self.data.wydatek.ustaw_kwote(transakcja.kwota)

        elif transakcja.typ.lower() == 'przychód':
            self.data.przychody_kategorie[transakcja.kategoria] = \
                self.data.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.data.dochod.ustaw_kwote(transakcja.kwota)

        self.zapisz_dane()

    def usun_transakcje(self, indeks: int) -> bool:
        if 0 <= indeks < len(self.data.transakcje):
            transakcja = self.data.transakcje.pop(indeks)

            if transakcja.typ.lower() == 'wydatek':
                self.data.wydatki_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.data.wydatki_kategorie[transakcja.kategoria] <= 0:
                    del self.data.wydatki_kategorie[transakcja.kategoria]
                # "Cofa" się wartość w obserwatorze
                self.data.wydatek.ustaw_kwote(-transakcja.kwota)

            elif transakcja.typ.lower() == 'przychód':
                self.data.przychody_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.data.przychody_kategorie[transakcja.kategoria] <= 0:
                    del self.data.przychody_kategorie[transakcja.kategoria]
                self.data.dochod.ustaw_kwote(-transakcja.kwota)

            self.zapisz_dane()
            return True
        return False

    def edytuj_transakcje(self, indeks: int, transakcja_nowa: Transakcja) -> bool:
        if 0 <= indeks < len(self.data.transakcje):
            transakcja_stara = self.data.transakcje[indeks]

            # Cofamy starą transakcję
            if transakcja_stara.typ.lower() == 'wydatek':
                self.data.wydatki_kategorie[transakcja_stara.kategoria] -= transakcja_stara.kwota
                if self.data.wydatki_kategorie[transakcja_stara.kategoria] <= 0:
                    del self.data.wydatki_kategorie[transakcja_stara.kategoria]
                self.data.wydatek.ustaw_kwote(-transakcja_stara.kwota)

            elif transakcja_stara.typ.lower() == 'przychód':
                self.data.przychody_kategorie[transakcja_stara.kategoria] -= transakcja_stara.kwota
                if self.data.przychody_kategorie[transakcja_stara.kategoria] <= 0:
                    del self.data.przychody_kategorie[transakcja_stara.kategoria]
                self.data.dochod.ustaw_kwote(-transakcja_stara.kwota)

            # Aktualizujemy na nową transakcję
            self.data.transakcje[indeks] = transakcja_nowa

            if transakcja_nowa.typ.lower() == 'wydatek':
                self.data.wydatki_kategorie[transakcja_nowa.kategoria] = \
                    self.data.wydatki_kategorie.get(transakcja_nowa.kategoria, 0) + transakcja_nowa.kwota
                self.data.wydatek.ustaw_kwote(transakcja_nowa.kwota)

            elif transakcja_nowa.typ.lower() == 'przychód':
                self.data.przychody_kategorie[transakcja_nowa.kategoria] = \
                    self.data.przychody_kategorie.get(transakcja_nowa.kategoria, 0) + transakcja_nowa.kwota
                self.data.dochod.ustaw_kwote(transakcja_nowa.kwota)

            self.zapisz_dane()
            return True
        return False

    def oblicz_saldo(self) -> float:
        """
        Suma wszystkich przychodów - suma wszystkich wydatków.
        """
        saldo = sum(t.kwota if t.typ.lower() == 'przychód' else -t.kwota 
                    for t in self.data.transakcje)
        return saldo

    def filtruj_transakcje_po_dacie(self, data_poczatkowa: str, data_koncowa: str) -> List[Transakcja]:
        """
        Zwraca listę transakcji mieszczących się w zadanym zakresie dat.
        """
        return [
            t for t in self.data.transakcje
            if data_poczatkowa <= t.data <= data_koncowa
        ]

    ###################################
    # ODCZYT / ZAPIS DANYCH
    ###################################
    def zapisz_dane(self) -> None:
        """
        Zapisuje wszystkie transakcje do pliku JSON specificznego dla zalogowanego użytkownika.
        """
        if self.plik_danych:
            os.makedirs(os.path.dirname(self.plik_danych), exist_ok=True)
            try:
                dane = [t.to_dict() for t in self.data.transakcje]
                with open(self.plik_danych, 'w', encoding='utf-8') as plik:
                    json.dump(dane, plik, ensure_ascii=False, indent=4)
            except IOError:
                pass

    def wczytaj_dane(self) -> None:
        if self.plik_danych and os.path.exists(self.plik_danych):
            try:
                with open(self.plik_danych, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    self.data.transakcje = [Transakcja(**t) for t in dane]
            except (IOError, json.JSONDecodeError):
                self.data.transakcje = []
        else:
            self.data.transakcje = []

    ###################################
    # ODCZYT / ZAPIS LIMITÓW
    ###################################
    def wczytaj_limity(self) -> None:
        if self.plik_limity and os.path.exists(self.plik_limity):
            try:
                with open(self.plik_limity, 'r', encoding='utf-8') as plik:
                    self.data.limity = json.load(plik)
            except (IOError, json.JSONDecodeError):
                self.data.limity = {}
        else:
            self.data.limity = {}

    def zapisz_limity(self) -> None:
        if self.plik_limity:
            os.makedirs(os.path.dirname(self.plik_limity), exist_ok=True)
            try:
                with open(self.plik_limity, 'w', encoding='utf-8') as plik:
                    json.dump(self.data.limity, plik, ensure_ascii=False, indent=4)
            except IOError:
                pass

    ###################################
    # OPERACJE NA LIMITACH
    ###################################
    def ustaw_limit(self, kategoria: str, limit: float) -> None:
        self.data.limity[kategoria] = limit
        self.zapisz_limity()

    def pobierz_limit(self, kategoria: str) -> Optional[float]:
        return self.data.limity.get(kategoria)

    def usun_limit(self, kategoria: str) -> bool:
        if kategoria in self.data.limity:
            del self.data.limity[kategoria]
            self.zapisz_limity()
            return True
        return False

    def sprawdz_limit(self, kategoria: str, kwota: float) -> bool:
        """
        True, jeśli po dodaniu kwoty do kategorii nie przekroczymy ustalonego limitu,
        lub jeśli limit nie jest ustawiony.
        """
        limit = self.pobierz_limit(kategoria)
        if limit is None:
            return True
        wydatki = self.data.wydatki_kategorie.get(kategoria, 0)
        return (wydatki + kwota) <= limit

    ###################################
    # RAPORTY
    ###################################
    def generuj_raport_wydatkow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.data.transakcje:
            if t.typ.lower() == 'wydatek':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        return raport

    def generuj_raport_przychodow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.data.transakcje:
            if t.typ.lower() == 'przychód':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        return raport

    def _oblicz_wydatki_kategorie(self) -> None:
        self.data.wydatki_kategorie = {}
        for t in self.data.transakcje:
            if t.typ.lower() == 'wydatek':
                self.data.wydatki_kategorie[t.kategoria] = \
                    self.data.wydatki_kategorie.get(t.kategoria, 0) + t.kwota

    def _oblicz_przychody_kategorie(self) -> None:
        self.data.przychody_kategorie = {}
        for t in self.data.transakcje:
            if t.typ.lower() == 'przychód':
                self.data.przychody_kategorie[t.kategoria] = \
                    self.data.przychody_kategorie.get(t.kategoria, 0) + t.kwota

    ###################################
    # OBSŁUGA CELU (ZAPIS / ODCZYT)
    ###################################
    def zapisz_cel(self) -> None:
        if self.data.cel_oszczedzania is not None:
            os.makedirs(os.path.dirname(self.data.cel_oszczedzania.plik_celu), exist_ok=True)
            try:
                with open(self.data.cel_oszczedzania.plik_celu, 'w', encoding='utf-8') as plik:
                    json.dump({
                        'cel_oszczednosci': self.data.cel_oszczedzania.cel_oszczednosci,
                        'obecneOszczednosci': self.data.cel_oszczedzania.obecneOszczednosci
                    }, plik, ensure_ascii=False, indent=4)
            except IOError:
                pass

    def wczytaj_cel(self) -> None:
        if self.data.cel_oszczedzania is None:
            return
        if os.path.exists(self.data.cel_oszczedzania.plik_celu):
            try:
                with open(self.data.cel_oszczedzania.plik_celu, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    self.data.cel_oszczedzania.cel_oszczednosci = dane.get('cel_oszczednosci', 10000.0)
                    self.data.cel_oszczedzania.obecneOszczednosci = dane.get('obecneOszczednosci', 0.0)
            except (IOError, json.JSONDecodeError):
                pass

    def ustaw_nowy_cel(self, nowy_cel: float) -> None:
        if self.data.cel_oszczedzania is not None:
            self.data.cel_oszczedzania.cel_oszczednosci = nowy_cel
            self.data.cel_oszczedzania.obecneOszczednosci = 0.0
            self.zapisz_cel()

    ###################################
    # EKSPORT / IMPORT
    ###################################
    def eksportuj_do_csv(self, nazwa_pliku: str = None) -> None:
        if not nazwa_pliku:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.csv')
        dane = [t.to_dict() for t in self.data.transakcje]
        self.eksport_danych.ustawEksporter(self.eksport_danych.eksporter_csv)
        self.eksport_danych.eksportujDane(dane, nazwa_pliku)

    def eksportuj_do_json(self, nazwa_pliku: str = None) -> None:
        if not nazwa_pliku:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.json')
        dane = [t.to_dict() for t in self.data.transakcje]
        self.eksport_danych.ustawEksporter(self.eksport_danych.eksporter_json)
        self.eksport_danych.eksportujDane(dane, nazwa_pliku)

    def importuj_z_csv(self, nazwa_pliku: str = None) -> bool:
        if not nazwa_pliku:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.csv')
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
                        self.dodaj_transakcje(transakcja)
                return True
            except (IOError, ValueError):
                return False
        return False

    def importuj_z_json(self, nazwa_pliku: str = None) -> bool:
        if not nazwa_pliku:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.json')
        if os.path.exists(nazwa_pliku):
            try:
                with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    for rekord in dane:
                        transakcja = Transakcja(
                            kwota=float(rekord['kwota']),
                            kategoria=rekord['kategoria'],
                            typ=rekord['typ'],
                            opis=rekord.get('opis', ''),
                            data=rekord.get('data', datetime.now().strftime('%Y-%m-%d'))
                        )
                        self.dodaj_transakcje(transakcja)
                return True
            except (IOError, json.JSONDecodeError):
                return False
        return False
