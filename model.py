import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from abc import ABC, abstractmethod

###########################
# OBSERVER (Obserwator)
###########################

class Obserwator:
    """
    Prosta klasa interfejsu obserwatora.
    """
    def aktualizuj(self, podmiot: 'Podmiot') -> None:
        raise NotImplementedError


class Podmiot:
    """
    Klasa bazowa dla podmiotu (subject) w wzorcu Observer.
    Przechowuje listę obserwatorów i powiadamia ich o zmianach.
    """
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
    """
    Klasa reprezentująca dochód (przychód).
    """
    def __init__(self) -> None:
        super().__init__()
        self.ostatnia_kwota = 0.0

    def ustaw_kwote(self, kwota: float):
        """
        Ustawia kwotę dochodu i powiadamia obserwatorów o zmianie.
        """
        self.ostatnia_kwota = kwota
        self.powiadomObserwatorow()


class Wydatek(Podmiot):
    """
    Klasa reprezentująca wydatek.
    """
    def __init__(self) -> None:
        super().__init__()
        self.ostatnia_kwota = 0.0

    def ustaw_kwote(self, kwota: float):
        """
        Ustawia kwotę wydatku i powiadamia obserwatorów o zmianie.
        """
        self.ostatnia_kwota = kwota
        self.powiadomObserwatorow()


class Cel(Obserwator):
    """
    Klasa reprezentująca cel oszczędnościowy.
    """
    def __init__(self, cel_oszczednosci: float, uzytkownik: str) -> None:
        self._cel_oszczednosci = cel_oszczednosci
        self._obecneOszczednosci = 0.0
        self._uzytkownik = uzytkownik
        # W modelu przechowujemy tylko informację o pliku z celem.
        # Logika zapisu/odczytu w pliku przeniesiona do serwisu.
        self.plik_celu = os.path.join('data', 'users', uzytkownik, 'cel_oszczednosci.json')

    @property
    def cel_oszczednosci(self) -> float:
        return self._cel_oszczednosci

    @cel_oszczednosci.setter
    def cel_oszczednosci(self, nowy_cel: float):
        self._cel_oszczednosci = nowy_cel

    @property
    def obecneOszczednosci(self) -> float:
        return self._obecneOszczednosci

    @obecneOszczednosci.setter
    def obecneOszczednosci(self, nowa_kwota: float):
        self._obecneOszczednosci = nowa_kwota

    @property
    def uzytkownik(self) -> str:
        return self._uzytkownik

    def aktualizuj(self, podmiot: Podmiot) -> None:
        """
        Po aktualizacji (np. dodaniu przychodu lub wydatku),
        zmienia się kwota obserwowanych oszczędności.
        """
        if isinstance(podmiot, Dochod):
            self._obecneOszczednosci += podmiot.ostatnia_kwota
        elif isinstance(podmiot, Wydatek):
            self._obecneOszczednosci -= podmiot.ostatnia_kwota

    def __repr__(self) -> str:
        return f"Cel(cel={self._cel_oszczednosci}, obecne={self._obecneOszczednosci})"


###########################
# DANE (MODELE)
###########################

@dataclass
class Transakcja:
    """
    Klasa danych reprezentująca pojedynczą transakcję.
    """
    kwota: float
    kategoria: str
    typ: str       # 'wydatek' lub 'przychód'
    opis: str = ""
    data: str = datetime.now().strftime('%Y-%m-%d')

    def to_dict(self) -> Dict:
        return asdict(self)


class BudzetData:
    """
    Prosta klasa przechowująca dane dla naszego budżetu:
    - transakcje
    - limity
    - użytkownicy
    - zalogowany użytkownik
    - kategorię wydatków i przychodów
    - obiekt Cel do obsługi oszczędności
    - obiekty Dochod i Wydatek, do których podpina się Cel
    """
    def __init__(self) -> None:
        self._transakcje: List[Transakcja] = []
        self._limity: Dict[str, float] = {}
        self._wydatki_kategorie: Dict[str, float] = {}
        self._przychody_kategorie: Dict[str, float] = {}
        self._uzytkownicy: Dict[str, str] = {}
        self._zalogowany_uzytkownik: Optional[str] = None

        # Observer pattern
        self.dochod = Dochod()
        self.wydatek = Wydatek()
        # Domyślnie brak celu, zostanie ustawiony po zalogowaniu
        self._cel_oszczedzania: Optional[Cel] = None

    # Gettery i settery
    @property
    def transakcje(self) -> List[Transakcja]:
        return self._transakcje

    @transakcje.setter
    def transakcje(self, value: List[Transakcja]):
        self._transakcje = value

    @property
    def limity(self) -> Dict[str, float]:
        return self._limity

    @limity.setter
    def limity(self, value: Dict[str, float]):
        self._limity = value

    @property
    def wydatki_kategorie(self) -> Dict[str, float]:
        return self._wydatki_kategorie

    @wydatki_kategorie.setter
    def wydatki_kategorie(self, value: Dict[str, float]):
        self._wydatki_kategorie = value

    @property
    def przychody_kategorie(self) -> Dict[str, float]:
        return self._przychody_kategorie

    @przychody_kategorie.setter
    def przychody_kategorie(self, value: Dict[str, float]):
        self._przychody_kategorie = value

    @property
    def uzytkownicy(self) -> Dict[str, str]:
        return self._uzytkownicy

    @uzytkownicy.setter
    def uzytkownicy(self, value: Dict[str, str]):
        self._uzytkownicy = value

    @property
    def zalogowany_uzytkownik(self) -> Optional[str]:
        return self._zalogowany_uzytkownik

    @zalogowany_uzytkownik.setter
    def zalogowany_uzytkownik(self, value: Optional[str]):
        self._zalogowany_uzytkownik = value

    @property
    def cel_oszczedzania(self) -> Optional[Cel]:
        return self._cel_oszczedzania

    @cel_oszczedzania.setter
    def cel_oszczedzania(self, value: Optional[Cel]):
        self._cel_oszczedzania = value

    def __repr__(self) -> str:
        return (
            f"BudzetData(\n"
            f"  transakcje={len(self._transakcje)},\n"
            f"  limity={self._limity},\n"
            f"  wydatki_kategorie={self._wydatki_kategorie},\n"
            f"  przychody_kategorie={self._przychody_kategorie},\n"
            f"  uzytkownicy={list(self._uzytkownicy.keys())},\n"
            f"  zalogowany={self._zalogowany_uzytkownik},\n"
            f"  cel={self._cel_oszczedzania}\n)"
        )
