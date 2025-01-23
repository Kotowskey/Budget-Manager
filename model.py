import json
import os
from datetime import datetime
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod

##########################################
# Wzorzec projektowy: OBSERVER (Obserwator)
##########################################

class Obserwator:
    def aktualizuj(self, podmiot: 'Podmiot') -> None:
        raise NotImplementedError

class Podmiot:
    def __init__(self) -> None:
        self.obserwatorzy: List[Obserwator] = []

    def dodaj(self, obserwator: Obserwator) -> None:
        self.obserwatorzy.append(obserwator)

    def usun(self, obserwator: Obserwator) -> None:
        if obserwator in self.obserwatorzy:
            self.obserwatorzy.remove(obserwator)

    def powiadomObserwatorow(self) -> None:
        for obs in self.obserwatorzy:
            obs.aktualizuj(self)

class Dochod(Podmiot):
    def __init__(self) -> None:
        super().__init__()
        self.ostatnia_kwota = 0.0

    def dodajDochod(self, kwota: float) -> None:
        self.ostatnia_kwota = kwota
        self.powiadomObserwatorow()

class Wydatek(Podmiot):
    def __init__(self) -> None:
        super().__init__()
        self.ostatnia_kwota = 0.0

    def dodajWydatek(self, kwota: float) -> None:
        self.ostatnia_kwota = kwota
        self.powiadomObserwatorow()

class Cel(Obserwator):
    def __init__(self, cel_oszczednosci: float, uzytkownik: str) -> None:
        self.cel_oszczednosci = cel_oszczednosci
        self.obecneOszczednosci = 0.0
        self.uzytkownik = uzytkownik
        self.plik_celu = os.path.join('data', 'users', uzytkownik, 'cel_oszczednosci.json')
        self.wczytaj_cel()

    def aktualizuj(self, podmiot: Podmiot) -> None:
        if isinstance(podmiot, Dochod):
            self.obecneOszczednosci += podmiot.ostatnia_kwota
        elif isinstance(podmiot, Wydatek):
            self.obecneOszczednosci -= podmiot.ostatnia_kwota
        self.monitorujPostep()
        self.zapisz_cel()

    def monitorujPostep(self) -> None:
        if self.cel_oszczednosci > 0:
            procent = (self.obecneOszczednosci / self.cel_oszczednosci) * 100
            if procent >= 100:
                self.powiadomCelOsiagniety()

    def powiadomCelOsiagniety(self) -> None:
        pass

    def zapisz_cel(self) -> None:
        os.makedirs(os.path.dirname(self.plik_celu), exist_ok=True)
        try:
            with open(self.plik_celu, 'w', encoding='utf-8') as plik:
                json.dump({
                    'cel_oszczednosci': self.cel_oszczednosci,
                    'obecneOszczednosci': self.obecneOszczednosci
                }, plik, ensure_ascii=False, indent=4)
        except IOError as e:
            pass

    def wczytaj_cel(self) -> None:
        if os.path.exists(self.plik_celu):
            try:
                with open(self.plik_celu, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    self.cel_oszczednosci = dane.get('cel_oszczednosci', self.cel_oszczednosci)
                    self.obecneOszczednosci = dane.get('obecneOszczednosci', self.obecneOszczednosci)
            except (IOError, json.JSONDecodeError) as e:
                pass

    def ustaw_nowy_cel(self, nowy_cel: float) -> None:
        self.cel_oszczednosci = nowy_cel
        self.obecneOszczednosci = 0.0
        self.zapisz_cel()

##########################################
# Wzorzec projektowy: ADAPTER
##########################################

class UniwersalnyInterfejsEksportu(ABC):
    @abstractmethod
    def eksportuj(self, dane: Any, nazwa_pliku: str) -> None:
        pass

class AdapterEksportu(UniwersalnyInterfejsEksportu):
    def __init__(self, eksporter: Any) -> None:
        self.eksporter = eksporter

    def eksportuj(self, dane: Any, nazwa_pliku: str) -> None:
        pass

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

class AdapterEksportuCSV(AdapterEksportu):
    def __init__(self, eksporter: EksporterCSV) -> None:
        super().__init__(eksporter)

    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        self.eksporter.eksportujDoCSV(dane, nazwa_pliku)

class AdapterEksportuJSON(AdapterEksportu):
    def __init__(self, eksporter: EksporterJSON) -> None:
        super().__init__(eksporter)

    def eksportuj(self, dane: List[Dict], nazwa_pliku: str) -> None:
        self.eksporter.eksportujDoJSON(dane, nazwa_pliku)

class EksportDanych:
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
            raise ValueError("Nie ustawiono eksportera")

@dataclass
class Transakcja:
    kwota: float
    kategoria: str
    typ: str
    opis: str = ""
    data: str = datetime.now().strftime('%Y-%m-%d')

    def to_dict(self) -> Dict:
        return asdict(self)

class BudzetModel:
    def __init__(self) -> None:
        self.data_dir = 'data'
        self.users_dir = os.path.join(self.data_dir, 'users')
        self.exports_dir = os.path.join(self.data_dir, 'exports')
        self.create_directories()

        self.transakcje: List[Transakcja] = []
        self.uzytkownicy_plik: str = os.path.join(self.users_dir, 'uzytkownicy.json')
        self.limity: Dict[str, float] = {}
        self.wydatki_kategorie: Dict[str, float] = {}
        self.przychody_kategorie: Dict[str, float] = {}
        self.zalogowany_uzytkownik: Optional[str] = None
        self.uzytkownicy: Dict[str, str] = self.wczytaj_uzytkownikow()
        
        self.eksport_danych = EksportDanych()
        self.dochod = Dochod()
        self.wydatek = Wydatek()
        self.cel_oszczedzania: Optional[Cel] = None

    def create_directories(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.users_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)

    def zaloguj(self, login: str, haslo: str) -> bool:
        if login in self.uzytkownicy and self.uzytkownicy[login] == haslo:
            self.zalogowany_uzytkownik = login
            user_dir = os.path.join(self.users_dir, login)
            os.makedirs(user_dir, exist_ok=True)
            
            self.plik_danych = os.path.join(user_dir, 'dane.json')
            self.plik_limity = os.path.join(user_dir, 'limity.json')
            
            self.cel_oszczedzania = Cel(10000.0, login)
            self.dochod.dodaj(self.cel_oszczedzania)
            self.wydatek.dodaj(self.cel_oszczedzania)
            
            self.wczytaj_dane()
            self.wczytaj_limity()
            self.oblicz_wydatki_kategorie()
            self.oblicz_przychody_kategorie()
            return True
        return False

    def zarejestruj(self, login: str, haslo: str) -> bool:
        if login not in self.uzytkownicy:
            self.uzytkownicy[login] = haslo
            self.zapisz_uzytkownikow()
            return True
        return False

    def wczytaj_uzytkownikow(self) -> Dict[str, str]:
        if os.path.exists(self.uzytkownicy_plik):
            try:
                with open(self.uzytkownicy_plik, 'r', encoding='utf-8') as plik:
                    return json.load(plik)
            except (IOError, json.JSONDecodeError) as e:
                return {}
        return {}

    def zapisz_uzytkownikow(self) -> None:
        os.makedirs(os.path.dirname(self.uzytkownicy_plik), exist_ok=True)
        try:
            with open(self.uzytkownicy_plik, 'w', encoding='utf-8') as plik:
                json.dump(self.uzytkownicy, plik, ensure_ascii=False, indent=4)
        except IOError as e:
            pass

    def dodaj_transakcje(self, transakcja: Transakcja) -> None:
        self.transakcje.append(transakcja)
        if transakcja.typ.lower() == 'wydatek':
            self.wydatki_kategorie[transakcja.kategoria] = self.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.wydatek.dodajWydatek(transakcja.kwota)
        elif transakcja.typ.lower() == 'przychód':
            self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.dochod.dodajDochod(transakcja.kwota)

        self.zapisz_dane()

    def usun_transakcje(self, indeks: int) -> bool:
        if 0 <= indeks < len(self.transakcje):
            transakcja = self.transakcje.pop(indeks)
            if transakcja.typ.lower() == 'wydatek':
                self.wydatki_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.wydatki_kategorie[transakcja.kategoria] <= 0:
                    del self.wydatki_kategorie[transakcja.kategoria]
                self.wydatek.dodajWydatek(-transakcja.kwota)
            elif transakcja.typ.lower() == 'przychód':
                self.przychody_kategorie[transakcja.kategoria] -= transakcja.kwota
                if self.przychody_kategorie[transakcja.kategoria] <= 0:
                    del self.przychody_kategorie[transakcja.kategoria]
                self.dochod.dodajDochod(-transakcja.kwota)
            self.zapisz_dane()
            return True
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
                self.wydatek.dodajWydatek(transakcja.kwota)
            elif transakcja.typ.lower() == 'przychód':
                self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                self.dochod.dodajDochod(transakcja.kwota)

            self.transakcje[indeks] = transakcja
            self.zapisz_dane()
            return True
        return False

    def zapisz_dane(self) -> None:
        if hasattr(self, 'plik_danych'):
            os.makedirs(os.path.dirname(self.plik_danych), exist_ok=True)
            try:
                dane = [t.to_dict() for t in self.transakcje]
                with open(self.plik_danych, 'w', encoding='utf-8') as plik:
                    json.dump(dane, plik, ensure_ascii=False, indent=4)
            except IOError as e:
                pass

    def wczytaj_dane(self) -> None:
        if hasattr(self, 'plik_danych') and os.path.exists(self.plik_danych):
            try:
                with open(self.plik_danych, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    self.transakcje = [Transakcja(**t) for t in dane]
            except (IOError, json.JSONDecodeError) as e:
                self.transakcje = []
        else:
            self.transakcje = []

    def oblicz_saldo(self) -> float:
        saldo = sum(t.kwota if t.typ.lower() == 'przychód' else -t.kwota for t in self.transakcje)
        return saldo

    def filtruj_transakcje_po_dacie(self, data_poczatkowa: str, data_koncowa: str) -> List[Transakcja]:
        filtrowane = [
            t for t in self.transakcje
            if data_poczatkowa <= t.data <= data_koncowa
        ]
        return filtrowane

    def eksportuj_do_csv(self, nazwa_pliku: str = None) -> None:
        if nazwa_pliku is None:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.csv')
        try:
            dane = [t.to_dict() for t in self.transakcje]
            self.eksport_danych.ustawEksporter(self.eksport_danych.eksporter_csv)
            self.eksport_danych.eksportujDane(dane, nazwa_pliku)
        except Exception as e:
            raise

    def eksportuj_do_json(self, nazwa_pliku: str = None) -> None:
        if nazwa_pliku is None:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.json')
        try:
            dane = [t.to_dict() for t in self.transakcje]
            self.eksport_danych.ustawEksporter(self.eksport_danych.eksporter_json)
            self.eksport_danych.eksportujDane(dane, nazwa_pliku)
        except Exception as e:
            raise

    def importuj_z_csv(self, nazwa_pliku: str = None) -> bool:
        if nazwa_pliku is None:
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
                        self.transakcje.append(transakcja)
                        if transakcja.typ.lower() == 'wydatek':
                            self.wydatki_kategorie[transakcja.kategoria] = self.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.wydatek.dodajWydatek(transakcja.kwota)
                        elif transakcja.typ.lower() == 'przychód':
                            self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.dochod.dodajDochod(transakcja.kwota)

                self.zapisz_dane()
                return True
            except (IOError, ValueError) as e:
                return False
        else:
            return False

    def importuj_z_json(self, nazwa_pliku: str = None) -> bool:
        if nazwa_pliku is None:
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
                        self.transakcje.append(transakcja)
                        if transakcja.typ.lower() == 'wydatek':
                            self.wydatki_kategorie[transakcja.kategoria] = self.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.wydatek.dodajWydatek(transakcja.kwota)
                        elif transakcja.typ.lower() == 'przychód':
                            self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
                            self.dochod.dodajDochod(transakcja.kwota)

                self.zapisz_dane()
                return True
            except (IOError, json.JSONDecodeError) as e:
                return False
        else:
            return False

    def wczytaj_limity(self) -> None:
        if hasattr(self, 'plik_limity') and os.path.exists(self.plik_limity):
            try:
                with open(self.plik_limity, 'r', encoding='utf-8') as plik:
                    self.limity = json.load(plik)
            except (IOError, json.JSONDecodeError) as e:
                self.limity = {}
        else:
            self.limity = {}

    def zapisz_limity(self) -> None:
        if hasattr(self, 'plik_limity'):
            os.makedirs(os.path.dirname(self.plik_limity), exist_ok=True)
            try:
                with open(self.plik_limity, 'w', encoding='utf-8') as plik:
                    json.dump(self.limity, plik, ensure_ascii=False, indent=4)
            except IOError as e:
                pass

    def ustaw_limit(self, kategoria: str, limit: float) -> None:
        self.limity[kategoria] = limit
        self.zapisz_limity()

    def pobierz_limit(self, kategoria: str) -> Optional[float]:
        return self.limity.get(kategoria)

    def usun_limit(self, kategoria: str) -> bool:
        if kategoria in self.limity:
            del self.limity[kategoria]
            self.zapisz_limity()
            return True
        return False

    def sprawdz_limit(self, kategoria: str, kwota: float) -> bool:
        limit = self.pobierz_limit(kategoria)
        if limit is None:
            return True
        wydatki = self.wydatki_kategorie.get(kategoria, 0)
        return (wydatki + kwota) <= limit

    def generuj_raport_wydatkow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.transakcje:
            if t.typ.lower() == 'wydatek':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        return raport

    def generuj_raport_przychodow(self) -> Dict[str, float]:
        raport: Dict[str, float] = {}
        for t in self.transakcje:
            if t.typ.lower() == 'przychód':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        return raport

    def oblicz_wydatki_kategorie(self) -> None:
        self.wydatki_kategorie = {}
        for t in self.transakcje:
            if t.typ.lower() == 'wydatek':
                self.wydatki_kategorie[t.kategoria] = self.wydatki_kategorie.get(t.kategoria, 0) + t.kwota

    def oblicz_przychody_kategorie(self) -> None:
        self.przychody_kategorie = {}
        for t in self.transakcje:
            if t.typ.lower() == 'przychód':
                self.przychody_kategorie[t.kategoria] = self.przychody_kategorie.get(t.kategoria, 0) + t.kwota
