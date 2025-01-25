import os
import json
from typing import List

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
