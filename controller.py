from model import BudzetModel, Transakcja
from view import BudzetView

class BudzetController:
    def __init__(self):
        self.model = BudzetModel()
        self.view = BudzetView()

    def uruchom(self):
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
                    dane = self.view.pobierz_dane_transakcji(edycja=True)
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
                self.view.wyswietl_komunikat("Do widzenia!")
                break
            else:
                self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def oblicz_saldo(self):
        return self.model.oblicz_saldo()

    def filtruj_transakcje(self):
        start_date = input("Podaj datę początkową (YYYY-MM-DD): ")
        end_date = input("Podaj datę końcową (YYYY-MM-DD): ")
        filtrowane = self.model.filtruj_transakcje_po_dacie(start_date, end_date)
        self.view.wyswietl_transakcje(filtrowane)

    def ustaw_limit_budzetowy(self):
        kategoria, limit = self.view.pobierz_limit()
        if kategoria and limit > 0:
            self.model.ustaw_limit(kategoria, limit)
            self.view.potwierdz_ustawienie_limitu(kategoria, limit)
        else:
            self.view.wyswietl_komunikat("Nieprawidłowe dane. Limit nie został ustawiony.")
