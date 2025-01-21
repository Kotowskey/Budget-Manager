# model.py
import json
import os
from datetime import datetime
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
import logging
from abc import ABC, abstractmethod

# Konfiguracja logowania
logging.basicConfig(
    filename='budzet_app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

##########################################
# Wzorzec projektowy: OBSERVER (Obserwator)
##########################################

class Obserwator:
    def aktualizuj(self, podmiot: 'Podmiot') -> None:
        """Metoda wywoływana gdy podmiot zmienia stan"""
        raise NotImplementedError

class Podmiot:
    def __init__(self) -> None:
        self.obserwatorzy: List[Obserwator] = []

    def dodaj(self, obserwator: Obserwator) -> None:
        """Dodaje obserwatora do listy"""
        self.obserwatorzy.append(obserwator)

    def usun(self, obserwator: Obserwator) -> None:
        """Usuwa obserwatora z listy"""
        if obserwator in self.obserwatorzy:
            self.obserwatorzy.remove(obserwator)

    def powiadomObserwatorow(self) -> None:
        """Powiadamia wszystkich obserwatorów o zmianie"""
        for obs in self.obserwatorzy:
            obs.aktualizuj(self)

class Dochod(Podmiot):
    def __init__(self) -> None:
        super().__init__()
        self.ostatnia_kwota = 0.0

    def dodajDochod(self, kwota: float) -> None:
        """Dodaje nowy dochód i powiadamia obserwatorów"""
        self.ostatnia_kwota = kwota
        self.powiadomObserwatorow()

class Wydatek(Podmiot):
    def __init__(self) -> None:
        super().__init__()
        self.ostatnia_kwota = 0.0

    def dodajWydatek(self, kwota: float) -> None:
        """Dodaje nowy wydatek i powiadamia obserwatorów"""
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
        """Aktualizuje stan oszczędności na podstawie nowych transakcji"""
        if isinstance(podmiot, Dochod):
            self.obecneOszczednosci += podmiot.ostatnia_kwota
        elif isinstance(podmiot, Wydatek):
            self.obecneOszczednosci -= podmiot.ostatnia_kwota
        self.monitorujPostep()
        self.zapisz_cel()

    def monitorujPostep(self) -> None:
        """Monitoruje postęp w osiąganiu celu oszczędnościowego"""
        if self.cel_oszczednosci > 0:
            procent = (self.obecneOszczednosci / self.cel_oszczednosci) * 100
            logging.info(f"Postęp w realizacji celu oszczędności: {procent:.2f}%")
            if procent >= 100:
                self.powiadomCelOsiagniety()

    def powiadomCelOsiagniety(self) -> None:
        """Powiadamia o osiągnięciu celu oszczędnościowego"""
        logging.info("Gratulacje! Osiągnąłeś swój cel oszczędnościowy!")

    def zapisz_cel(self) -> None:
        """Zapisuje stan celu do pliku"""
        os.makedirs(os.path.dirname(self.plik_celu), exist_ok=True)
        try:
            with open(self.plik_celu, 'w', encoding='utf-8') as plik:
                json.dump({
                    'cel_oszczednosci': self.cel_oszczednosci,
                    'obecneOszczednosci': self.obecneOszczednosci
                }, plik, ensure_ascii=False, indent=4)
        except IOError as e:
            logging.error(f"Błąd zapisu celu oszczędności: {e}")

    def wczytaj_cel(self) -> None:
        """Wczytuje stan celu z pliku"""
        if os.path.exists(self.plik_celu):
            try:
                with open(self.plik_celu, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    self.cel_oszczednosci = dane.get('cel_oszczednosci', self.cel_oszczednosci)
                    self.obecneOszczednosci = dane.get('obecneOszczednosci', self.obecneOszczednosci)
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Błąd wczytywania celu oszczędności: {e}")

    def ustaw_nowy_cel(self, nowy_cel: float) -> None:
        """Ustawia nowy cel oszczędnościowy"""
        self.cel_oszczednosci = nowy_cel
        self.obecneOszczednosci = 0.0
        self.zapisz_cel()

##########################################
# Wzorzec projektowy: ADAPTER
##########################################

class UniwersalnyInterfejsEksportu(ABC):
    @abstractmethod
    def eksportuj(self, dane: Any, nazwa_pliku: str) -> None:
        """Interfejs dla eksportu danych"""
        pass

class AdapterEksportu(UniwersalnyInterfejsEksportu):
    def __init__(self, eksporter: Any) -> None:
        self.eksporter = eksporter

    def eksportuj(self, dane: Any, nazwa_pliku: str) -> None:
        pass

class EksporterCSV:
    def eksportujDoCSV(self, dane: List[Dict], nazwa_pliku: str) -> None:
        """Eksportuje dane do pliku CSV"""
        try:
            with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
                if dane and len(dane) > 0:
                    fieldnames = dane[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in dane:
                        writer.writerow(row)
            logging.info(f"Dane wyeksportowane do pliku CSV: {nazwa_pliku}")
        except IOError as e:
            logging.error(f"Błąd eksportu do CSV: {e}")
            raise

class EksporterJSON:
    def eksportujDoJSON(self, dane: List[Dict], nazwa_pliku: str) -> None:
        """Eksportuje dane do pliku JSON"""
        try:
            with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                json.dump(dane, plik, ensure_ascii=False, indent=4)
            logging.info(f"Dane wyeksportowane do pliku JSON: {nazwa_pliku}")
        except IOError as e:
            logging.error(f"Błąd eksportu do JSON: {e}")
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

##########################################
# Klasy modelu budżetu
##########################################

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
    def __init__(self) -> None:
        # Inicjalizacja struktury katalogów
        self.data_dir = 'data'
        self.users_dir = os.path.join(self.data_dir, 'users')
        self.exports_dir = os.path.join(self.data_dir, 'exports')
        self.create_directories()

        # Podstawowe atrybuty
        self.transakcje: List[Transakcja] = []
        self.uzytkownicy_plik: str = os.path.join(self.users_dir, 'uzytkownicy.json')
        self.limity: Dict[str, float] = {}
        self.wydatki_kategorie: Dict[str, float] = {}
        self.przychody_kategorie: Dict[str, float] = {}
        self.zalogowany_uzytkownik: Optional[str] = None
        self.uzytkownicy: Dict[str, str] = self.wczytaj_uzytkownikow()
        
        # Inicjalizacja komponentów
        self.eksport_danych = EksportDanych()
        self.dochod = Dochod()
        self.wydatek = Wydatek()
        self.cel_oszczedzania: Optional[Cel] = None

        logging.info("Inicjalizacja modelu budżetu zakończona.")

    def create_directories(self) -> None:
        """Tworzy wymagane katalogi na dane"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.users_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)
        logging.info("Utworzono katalogi na dane aplikacji")

    def zaloguj(self, login: str, haslo: str) -> bool:
        """Loguje użytkownika i inicjalizuje jego dane"""
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
            logging.info(f"Zalogowano użytkownika: {login}")
            return True
        logging.warning(f"Nieudane logowanie dla użytkownika: {login}")
        return False

    def zarejestruj(self, login: str, haslo: str) -> bool:
        """Rejestruje nowego użytkownika"""
        if login not in self.uzytkownicy:
            self.uzytkownicy[login] = haslo
            self.zapisz_uzytkownikow()
            logging.info(f"Zarejestrowano nowego użytkownika: {login}")
            return True
        logging.warning(f"Próba rejestracji istniejącego użytkownika: {login}")
        return False

    def wczytaj_uzytkownikow(self) -> Dict[str, str]:
        """Wczytuje dane użytkowników z pliku"""
        if os.path.exists(self.uzytkownicy_plik):
            try:
                with open(self.uzytkownicy_plik, 'r', encoding='utf-8') as plik:
                    return json.load(plik)
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Błąd wczytywania użytkowników: {e}")
                return {}
        return {}

    def zapisz_uzytkownikow(self) -> None:
        """Zapisuje dane użytkowników do pliku"""
        os.makedirs(os.path.dirname(self.uzytkownicy_plik), exist_ok=True)
        try:
            with open(self.uzytkownicy_plik, 'w', encoding='utf-8') as plik:
                json.dump(self.uzytkownicy, plik, ensure_ascii=False, indent=4)
        except IOError as e:
            logging.error(f"Błąd zapisu użytkowników: {e}")

    def dodaj_transakcje(self, transakcja: Transakcja) -> None:
        """Dodaje nową transakcję i aktualizuje statystyki"""
        self.transakcje.append(transakcja)
        if transakcja.typ.lower() == 'wydatek':
            self.wydatki_kategorie[transakcja.kategoria] = self.wydatki_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.wydatek.dodajWydatek(transakcja.kwota)
        elif transakcja.typ.lower() == 'przychód':
            self.przychody_kategorie[transakcja.kategoria] = self.przychody_kategorie.get(transakcja.kategoria, 0) + transakcja.kwota
            self.dochod.dodajDochod(transakcja.kwota)

        self.zapisz_dane()
        logging.info(f"Dodano transakcję: {transakcja}")

    def usun_transakcje(self, indeks: int) -> bool:
        """Usuwa transakcję o podanym indeksie"""
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
            logging.info(f"Usunięto transakcję: {transakcja}")
            return True
        logging.warning(f"Próba usunięcia nieistniejącej transakcji o indeksie: {indeks}")
        return False

    def edytuj_transakcje(self, indeks: int, transakcja: Transakcja) -> bool:
        """Edytuje istniejącą transakcję"""
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
            logging.info(f"Edytowano transakcję na indeksie {indeks}: {transakcja}")
            return True
        logging.warning(f"Próba edycji nieistniejącej transakcji o indeksie: {indeks}")
        return False

    def zapisz_dane(self) -> None:
        """Zapisuje transakcje do pliku"""
        if hasattr(self, 'plik_danych'):
            os.makedirs(os.path.dirname(self.plik_danych), exist_ok=True)
            try:
                dane = [t.to_dict() for t in self.transakcje]
                with open(self.plik_danych, 'w', encoding='utf-8') as plik:
                    json.dump(dane, plik, ensure_ascii=False, indent=4)
                logging.debug("Dane zapisane do pliku.")
            except IOError as e:
                logging.error(f"Błąd zapisu danych: {e}")

    def wczytaj_dane(self) -> None:
        """Wczytuje transakcje z pliku"""
        if hasattr(self, 'plik_danych') and os.path.exists(self.plik_danych):
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

    def oblicz_saldo(self) -> float:
        """Oblicza aktualne saldo"""
        saldo = sum(t.kwota if t.typ.lower() == 'przychód' else -t.kwota for t in self.transakcje)
        logging.debug(f"Obliczone saldo: {saldo}")
        return saldo

    def filtruj_transakcje_po_dacie(self, data_poczatkowa: str, data_koncowa: str) -> List[Transakcja]:
        """Filtruje transakcje według zakresu dat"""
        filtrowane = [
            t for t in self.transakcje
            if data_poczatkowa <= t.data <= data_koncowa
        ]
        logging.debug(f"Filtrowano transakcje od {data_poczatkowa} do {data_koncowa}: {len(filtrowane)} znalezionych.")
        return filtrowane

    def eksportuj_do_csv(self, nazwa_pliku: str = None) -> None:
        """Eksportuje transakcje do pliku CSV"""
        if nazwa_pliku is None:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.csv')
        try:
            dane = [t.to_dict() for t in self.transakcje]
            self.eksport_danych.ustawEksporter(self.eksport_danych.eksporter_csv)
            self.eksport_danych.eksportujDane(dane, nazwa_pliku)
        except Exception as e:
            logging.error(f"Błąd podczas eksportu do CSV: {e}")
            raise

    def eksportuj_do_json(self, nazwa_pliku: str = None) -> None:
        """Eksportuje transakcje do pliku JSON"""
        if nazwa_pliku is None:
            nazwa_pliku = os.path.join(self.exports_dir, 'transakcje.json')
        try:
            dane = [t.to_dict() for t in self.transakcje]
            self.eksport_danych.ustawEksporter(self.eksport_danych.eksporter_json)
            self.eksport_danych.eksportujDane(dane, nazwa_pliku)
        except Exception as e:
            logging.error(f"Błąd podczas eksportu do JSON: {e}")
            raise

    def importuj_z_csv(self, nazwa_pliku: str = None) -> bool:
        """Importuje transakcje z pliku CSV"""
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
                logging.info(f"Transakcje zaimportowane z pliku CSV: {nazwa_pliku}")
                return True
            except (IOError, ValueError) as e:
                logging.error(f"Błąd importu z CSV: {e}")
                return False
        else:
            logging.warning(f"Plik CSV do importu nie istnieje: {nazwa_pliku}")
            return False

    def importuj_z_json(self, nazwa_pliku: str = None) -> bool:
        """Importuje transakcje z pliku JSON"""
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
                logging.info(f"Transakcje zaimportowane z pliku JSON: {nazwa_pliku}")
                return True
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Błąd importu z JSON: {e}")
                return False
        else:
            logging.warning(f"Plik JSON do importu nie istnieje: {nazwa_pliku}")
            return False

    def wczytaj_limity(self) -> None:
        """Wczytuje limity budżetowe z pliku"""
        if hasattr(self, 'plik_limity') and os.path.exists(self.plik_limity):
            try:
                with open(self.plik_limity, 'r', encoding='utf-8') as plik:
                    self.limity = json.load(plik)
                logging.debug("Limity wczytane z pliku.")
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Błąd wczytywania limitów: {e}")
                self.limity = {}
        else:
            self.limity = {}

    def zapisz_limity(self) -> None:
        """Zapisuje limity budżetowe do pliku"""
        if hasattr(self, 'plik_limity'):
            os.makedirs(os.path.dirname(self.plik_limity), exist_ok=True)
            try:
                with open(self.plik_limity, 'w', encoding='utf-8') as plik:
                    json.dump(self.limity, plik, ensure_ascii=False, indent=4)
                logging.debug("Limity zapisane do pliku.")
            except IOError as e:
                logging.error(f"Błąd zapisu limitów: {e}")

    def ustaw_limit(self, kategoria: str, limit: float) -> None:
        """Ustawia limit dla kategorii"""
        self.limity[kategoria] = limit
        self.zapisz_limity()
        logging.info(f"Ustawiono limit dla kategorii '{kategoria}': {limit} zł")

    def pobierz_limit(self, kategoria: str) -> Optional[float]:
        """Pobiera limit dla kategorii"""
        return self.limity.get(kategoria)

    def usun_limit(self, kategoria: str) -> bool:
        """Usuwa limit dla kategorii"""
        if kategoria in self.limity:
            del self.limity[kategoria]
            self.zapisz_limity()
            logging.info(f"Usunięto limit dla kategorii '{kategoria}'")
            return True
        return False

    def sprawdz_limit(self, kategoria: str, kwota: float) -> bool:
        """Sprawdza czy transakcja nie przekracza limitu"""
        limit = self.pobierz_limit(kategoria)
        if limit is None:
            return True
        wydatki = self.wydatki_kategorie.get(kategoria, 0)
        return (wydatki + kwota) <= limit

    def generuj_raport_wydatkow(self) -> Dict[str, float]:
        """Generuje raport wydatków według kategorii"""
        raport: Dict[str, float] = {}
        for t in self.transakcje:
            if t.typ.lower() == 'wydatek':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        logging.debug("Generowanie raportu wydatków zakończone.")
        return raport

    def generuj_raport_przychodow(self) -> Dict[str, float]:
        """Generuje raport przychodów według kategorii"""
        raport: Dict[str, float] = {}
        for t in self.transakcje:
            if t.typ.lower() == 'przychód':
                raport[t.kategoria] = raport.get(t.kategoria, 0) + t.kwota
        logging.debug("Generowanie raportu przychodów zakończone.")
        return raport

    def oblicz_wydatki_kategorie(self) -> None:
        """Oblicza sumę wydatków dla każdej kategorii"""
        self.wydatki_kategorie = {}
        for t in self.transakcje:
            if t.typ.lower() == 'wydatek':
                self.wydatki_kategorie[t.kategoria] = self.wydatki_kategorie.get(t.kategoria, 0) + t.kwota
        logging.debug("Obliczono wydatki dla każdej kategorii.")

    def oblicz_przychody_kategorie(self) -> None:
        """Oblicza sumę przychodów dla każdej kategorii"""
        self.przychody_kategorie = {}
        for t in self.transakcje:
            if t.typ.lower() == 'przychód':
                self.przychody_kategorie[t.kategoria] = self.przychody_kategorie.get(t.kategoria, 0) + t.kwota
        logging.debug("Obliczono przychody dla każdej kategorii.")