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
                    transakcja = Transakcja(**dane)
                    self.model.dodaj_transakcje(transakcja)
                    self.view.wyswietl_komunikat("Transakcja dodana.")
                elif opcja == '2':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                    indeks = self.view.pobierz_indeks_transakcji()
                    dane = self.view.pobierz_dane_transakcji()
                    transakcja = Transakcja(**dane)
                    self.model.edytuj_transakcje(indeks, transakcja)
                    self.view.wyswietl_komunikat("Transakcja zaktualizowana.")
                elif opcja == '3':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                    indeks = self.view.pobierz_indeks_transakcji()
                    self.model.usun_transakcje(indeks)
                    self.view.wyswietl_komunikat("Transakcja usunięta.")
                elif opcja == '4':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                elif opcja == '5':
                    saldo = self.oblicz_saldo()
                    self.view.wyswietl_podsumowanie(saldo)
                elif opcja == '6':
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
