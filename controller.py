# controller.py
import curses
from model import BudzetModel, Transakcja
from curses_view import BudzetCursesView
from typing import Optional

class BudzetController:
    def __init__(self) -> None:
        self.model = BudzetModel()
        self.view = BudzetCursesView()

    def uruchom(self) -> None:
        try:
            while True:
                self.view.wyswietl_menu()
                opcja = self.view.pobierz_opcje()
                if opcja == '1':
                    self.dodaj_transakcje()
                elif opcja == '2':
                    self.edytuj_transakcje()
                elif opcja == '3':
                    self.usun_transakcje()
                elif opcja == '4':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                elif opcja == '5':
                    self.wyswietl_podsumowanie()
                elif opcja == '6':
                    self.eksportuj_transakcje()
                elif opcja == '7':
                    self.filtruj_transakcje()
                elif opcja == '8':
                    self.ustaw_limit_budzetowy()
                elif opcja == '9':
                    self.importuj_transakcje()
                elif opcja == '10':
                    self.generuj_raport()
                elif opcja == '11':
                    self.view.wyswietl_komunikat("Do widzenia!")
                    break
                else:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")
        finally:
            self.view.zakoncz()

    def dodaj_transakcje(self) -> None:
        dane = self.view.pobierz_dane_transakcji()
        if not dane:
            return
        if dane['typ'] == 'wydatek':
            if not self.model.sprawdz_limit(dane['kategoria']):
                self.view.wyswietl_komunikat("Przekroczono limit budżetowy dla tej kategorii!")
                return
        transakcja = Transakcja(**dane)
        self.model.dodaj_transakcje(transakcja)
        self.view.wyswietl_komunikat("Transakcja dodana.")

    def edytuj_transakcje(self) -> None:
        self.view.wyswietl_transakcje(self.model.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if 0 <= indeks < len(self.model.transakcje):
            transakcja_oryginalna = self.model.transakcje[indeks]
            self.view.wyswietl_komunikat("Wprowadź nowe dane transakcji:")
            dane = self.view.pobierz_dane_transakcji(edycja=True)
            if not dane:
                return
            dane['typ'] = transakcja_oryginalna.typ  # Utrzymanie oryginalnego typu
            if dane['typ'] == 'wydatek':
                if not self.model.sprawdz_limit(dane['kategoria']):
                    self.view.wyswietl_komunikat("Przekroczono limit budżetowy dla tej kategorii!")
                    return
            transakcja = Transakcja(**dane)
            self.model.edytuj_transakcje(indeks, transakcja)
            self.view.wyswietl_komunikat("Transakcja zaktualizowana.")
        else:
            self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")

    def usun_transakcje(self) -> None:
        self.view.wyswietl_transakcje(self.model.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if self.model.usun_transakcje(indeks):
            self.view.wyswietl_komunikat("Transakcja usunięta.")
        else:
            self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")

    def wyswietl_podsumowanie(self) -> None:
        saldo = self.model.oblicz_saldo()
        self.view.wyswietl_podsumowanie(saldo)

    def eksportuj_transakcje(self) -> None:
        self.model.eksportuj_do_csv()
        self.view.potwierdz_eksport()

    def importuj_transakcje(self) -> None:
        self.model.importuj_z_csv()
        self.view.potwierdz_import()

    def filtruj_transakcje(self) -> None:
        start_date, end_date = self.view.pobierz_zakres_dat()
        if not start_date or not end_date:
            self.view.wyswietl_komunikat("Nieprawidłowy zakres dat.")
            return
        filtrowane = self.model.filtruj_transakcje_po_dacie(start_date, end_date)
        self.view.wyswietl_transakcje(filtrowane)

    def ustaw_limit_budzetowy(self) -> None:
        kategoria, limit = self.view.pobierz_limit()
        if kategoria and limit > 0:
            self.model.ustaw_limit(kategoria, limit)
            self.view.potwierdz_ustawienie_limitu(kategoria, limit)
        else:
            self.view.wyswietl_komunikat("Nieprawidłowe dane. Limit nie został ustawiony.")

    def generuj_raport(self) -> None:
        raport = self.model.generuj_raport_wydatkow()
        self.view.wyswietl_raport(raport)
