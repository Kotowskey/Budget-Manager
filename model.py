import os
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime

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
        # Można wysłać powiadomienie albo komunikat w widoku
        pass

    def zapisz_cel(self) -> None:
        os.makedirs(os.path.dirname(self.plik_celu), exist_ok=True)
        try:
            with open(self.plik_celu, 'w', encoding='utf-8') as plik:
                json.dump({
                    'cel_oszczednosci': self.cel_oszczednosci,
                    'obecneOszczednosci': self.obecneOszczednosci
                }, plik, ensure_ascii=False, indent=4)
        except IOError:
            pass

    def wczytaj_cel(self) -> None:
        if os.path.exists(self.plik_celu):
            try:
                with open(self.plik_celu, 'r', encoding='utf-8') as plik:
                    dane = json.load(plik)
                    self.cel_oszczednosci = dane.get('cel_oszczednosci', self.cel_oszczednosci)
                    self.obecneOszczednosci = dane.get('obecneOszczednosci', self.obecneOszczednosci)
            except (IOError, json.JSONDecodeError):
                pass

    def ustaw_nowy_cel(self, nowy_cel: float) -> None:
        self.cel_oszczednosci = nowy_cel
        self.obecneOszczednosci = 0.0
        self.zapisz_cel()

##########################################
# Dane (Model) + proste klasy / dataclass
##########################################

@dataclass
class Transakcja:
    kwota: float
    kategoria: str
    typ: str  # np. "wydatek" lub "przychód"
    opis: str = ""
    data: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))

    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class BudzetModel:
    """
    Klasa przechowująca dane aplikacji (Model) – wyłącznie pola
    oraz ewentualnie najprostsze gettery/settery.
    """
    transakcje: List[Transakcja] = field(default_factory=list)
    limity: Dict[str, float] = field(default_factory=dict)
    wydatki_kategorie: Dict[str, float] = field(default_factory=dict)
    przychody_kategorie: Dict[str, float] = field(default_factory=dict)

    # Użytkownicy
    zalogowany_uzytkownik: Optional[str] = None
    uzytkownicy: Dict[str, str] = field(default_factory=dict)

    # Cel oszczędzania (Obserwator)
    cel_oszczedzania: Optional[Cel] = None
    
    class TransakcjeBuilder:
        def __init__(self):
            self.kwota = 0.0
            self.kategoria = ""
            self.typ = "przychód"  # Domyślny typ
            self.opis = ""
            self.data = None

        def ustaw_kwote(self, kwota: float):
            self.kwota = kwota
            return self

        def ustaw_kategorie(self, kategoria: str):
            self.kategoria = kategoria
            return self

        def ustaw_typ(self, typ: str):
            if typ.lower() not in ["przychód", "wydatek"]:
                raise ValueError("Nieprawidłowy typ transakcji. Dozwolone wartości to: 'przychód' lub 'wydatek'.")
            self.typ = typ.lower()
            return self

        def ustaw_opis(self, opis: str):
            self.opis = opis
            return self

        def ustaw_date(self, data: str):
            self.data = data
            return self

        def buduj(self):
            if not self.data:
                from datetime import datetime
                self.data = datetime.now().strftime('%Y-%m-%d')
                return Transakcja(
                kwota=self.kwota,
                kategoria=self.kategoria,
                typ=self.typ,
                opis=self.opis,
                data=self.data
            )
