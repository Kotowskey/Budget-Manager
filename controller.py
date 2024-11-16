import curses
from model import BudzetModel, Transakcja
from curses_view import BudzetCursesView

class BudzetController:
    def __init__(self):
        self.model = BudzetModel()
        self.view = BudzetCursesView()

    def uruchom(self):
        try:
            while True:
                self.view.wyswietl_menu()
                opcja = self.view.pobierz_opcje()
                if opcja == '1':
                    dane = self.view.pobierz_dane_transakcji()
                    if dane['typ'].lower() == 'wydatek':
                        if not self.model.sprawdz_limit(dane['kategoria']):
                            self.view.wyswietl_komunikat("Przekroczono limit budżetowy dla tej kategorii!")
                            continue
                    transakcja = Transakcja(**dane)
                    self.model.dodaj_transakcje(transakcja)
                    self.view.wyswietl_komunikat("Transakcja dodana.")
                elif opcja == '2':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                    indeks = self.view.pobierz_indeks_transakcji()
                    if 0 <= indeks < len(self.model.transakcje):
                        transakcja_oryginalna = self.model.transakcje[indeks]
                        self.view.wyswietl_komunikat("Wprowadź nowe dane transakcji:")
                        dane = self.view.pobierz_dane_transakcji(edycja=True)
                        # Utrzymanie oryginalnego typu, jeśli nie jest edytowany
                        dane['typ'] = transakcja_oryginalna.typ
                        if dane['typ'].lower() == 'wydatek':
                            if not self.model.sprawdz_limit(dane['kategoria']):
                                self.view.wyswietl_komunikat("Przekroczono limit budżetowy dla tej kategorii!")
                                continue
                        transakcja = Transakcja(**dane)
                        self.model.edytuj_transakcje(indeks, transakcja)
                        self.view.wyswietl_komunikat("Transakcja zaktualizowana.")
                    else:
                        self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")
                elif opcja == '3':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                    indeks = self.view.pobierz_indeks_transakcji()
                    if 0 <= indeks < len(self.model.transakcje):
                        self.model.usun_transakcje(indeks)
                        self.view.wyswietl_komunikat("Transakcja usunięta.")
                    else:
                        self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")
                elif opcja == '4':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                elif opcja == '5':
                    saldo = self.oblicz_saldo()
                    self.view.wyswietl_podsumowanie(saldo)
                elif opcja == '6':
                    self.model.eksportuj_do_csv()
                    self.view.potwierdz_eksport()
                elif opcja == '7':
                    self.filtruj_transakcje()
                elif opcja == '8':
                    self.ustaw_limit_budzetowy()
                elif opcja == '9':
                    self.model.importuj_z_csv()
                    self.view.potwierdz_import()
                elif opcja == '10':
                    self.generuj_raport()
                elif opcja == '11':
                    self.view.wyswietl_komunikat("Do widzenia!")
                    break
                else:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")
        finally:
            self.view.zakoncz()

    def oblicz_saldo(self):
        saldo = 0
        for t in self.model.transakcje:
            if t.typ.lower() == 'przychód':
                saldo += t.kwota
            elif t.typ.lower() == 'wydatek':
                saldo -= t.kwota
        return saldo

    def filtruj_transakcje(self):
        self.view.stdscr.clear()
        curses.echo()
        self.view.stdscr.addstr(1, 1, "Podaj datę początkową (YYYY-MM-DD): ")
        start_date = self.view.stdscr.getstr(1, 40, 10).decode('utf-8')
        self.view.stdscr.addstr(2, 1, "Podaj datę końcową (YYYY-MM-DD): ")
        end_date = self.view.stdscr.getstr(2, 40, 10).decode('utf-8')
        curses.noecho()
        filtrowane = self.model.filtruj_transakcje_po_dacie(start_date, end_date)
        self.view.wyswietl_transakcje(filtrowane)

    def ustaw_limit_budzetowy(self):
        kategoria, limit = self.view.pobierz_limit()
        if kategoria and limit > 0:
            self.model.ustaw_limit(kategoria, limit)
            self.view.potwierdz_ustawienie_limitu(kategoria, limit)
        else:
            self.view.wyswietl_komunikat("Nieprawidłowe dane. Limit nie został ustawiony.")

    def generuj_raport(self):
        raport = self.model.generuj_raport_wydatkow()
        self.view.wyswietl_raport(raport)

if __name__ == "__main__":
    controller = BudzetController()
    controller.uruchom()
