# controller.py
from model import BudzetModel, Transakcja
from curses_view import BudzetCursesView

class BudzetController:
    def __init__(self) -> None:
        self.model = BudzetModel()
        self.view = BudzetCursesView()
        self.zalogowany_uzytkownik = None

    def uruchom(self) -> None:
        try:
            self.view.wyswietl_welcome_screen()  # Wyświetlenie ekranu powitalnego
            if not self.logowanie():
                return  # Jeśli użytkownik anulował logowanie, zakończ aplikację
            while True:
                self.view.wyswietl_glowne_menu_kategorii()
                opcja = self.view.pobierz_opcje_glownego_menu()
                if opcja is None:
                    # Użytkownik nacisnął ESC na głównym menu, pytamy czy chce wyjść
                    potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                    if potwierdzenie:
                        self.view.wyswietl_wyjscie()
                        break
                    else:
                        continue
                if opcja == '1':  # Transakcje
                    self.obsluz_podmenu_transakcje()
                elif opcja == '2':  # Podsumowania
                    self.obsluz_podmenu_podsumowania()
                elif opcja == '3':  # Importowanie i eksportowanie
                    self.obsluz_podmenu_import_eksport()
                elif opcja == '4':  # Wyjście
                    self.view.wyswietl_wyjscie()
                    break
                else:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")
        except Exception as e:
            self.view.wyswietl_komunikat(f"Wystąpił błąd: {e}")
        finally:
            self.view.zakoncz()

    def obsluz_podmenu_transakcje(self) -> None:
        while True:
            self.view.wyswietl_podmenu_transakcje()
            opcja = self.view.pobierz_opcje_podmenu_transakcje()
            if opcja is None:
                # Użytkownik nacisnął ESC, wracamy do głównego menu
                break
            if opcja == '1':
                self.dodaj_transakcje()
            elif opcja == '2':
                self.edytuj_transakcje()
            elif opcja == '3':
                self.usun_transakcje()
            elif opcja == '4':
                self.view.wyswietl_transakcje(self.model.transakcje)
            elif opcja == '5':
                break
            else:
                self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def obsluz_podmenu_podsumowania(self) -> None:
        while True:
            self.view.wyswietl_podmenu_podsumowania()
            opcja = self.view.pobierz_opcje_podmenu_podsumowania()
            if opcja is None:
                # Użytkownik nacisnął ESC, wracamy do głównego menu
                break
            if opcja == '1':
                self.wyswietl_podsumowanie()
            elif opcja == '2':
                self.generuj_raport_wydatkow()
            elif opcja == '3':
                self.generuj_raport_przychodow()
            elif opcja == '4':
                self.wyswietl_wykresy()
            elif opcja == '5':
                break
            else:
                self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def obsluz_podmenu_import_eksport(self) -> None:
        while True:
            self.view.wyswietl_podmenu_import_eksport()
            opcja = self.view.pobierz_opcje_podmenu_import_eksport()
            if opcja is None:
                # Użytkownik nacisnął ESC, wracamy do głównego menu
                break
            if opcja == '1':
                self.eksportuj_transakcje()
            elif opcja == '2':
                self.importuj_transakcje()
            elif opcja == '3':
                break
            else:
                self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def logowanie(self) -> bool:
        while True:
            self.view.wyswietl_ekran_logowania()
            opcja = self.view.pobierz_opcje_logowania()
            if opcja is None:
                # Użytkownik nacisnął ESC podczas logowania, pytamy czy chce wyjść
                potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                if potwierdzenie:
                    self.view.wyswietl_wyjscie()
                    self.view.zakoncz()
                    return False
                else:
                    continue
            if opcja == '1':
                login, haslo = self.view.pobierz_dane_logowania()
                if login == "" and haslo == "":
                    # Użytkownik anulował operację logowania
                    continue
                if self.model.zaloguj(login, haslo):
                    self.zalogowany_uzytkownik = login
                    self.view.wyswietl_komunikat(f"Zalogowano jako {login}.")
                    return True
                else:
                    self.view.wyswietl_komunikat("Nieprawidłowy login lub hasło.")
            elif opcja == '2':
                login, haslo = self.view.pobierz_dane_rejestracji()
                if login == "" and haslo == "":
                    # Użytkownik anulował operację rejestracji
                    continue
                if self.model.zarejestruj(login, haslo):
                    self.view.wyswietl_komunikat("Rejestracja udana. Możesz się teraz zalogować.")
                else:
                    self.view.wyswietl_komunikat("Użytkownik o takim loginie już istnieje.")
            elif opcja == '3':
                potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                if potwierdzenie:
                    self.view.wyswietl_wyjscie()
                    self.view.zakoncz()
                    return False
                else:
                    continue
            else:
                self.view.wyswietl_komunikat("Nieprawidłowa opcja.")

    def dodaj_transakcje(self) -> None:
        dane = self.view.pobierz_dane_transakcji()
        if not dane:
            return
        if dane['typ'] == 'wydatek':
            kwota = dane['kwota']
            kategoria = dane['kategoria']
            if not self.model.sprawdz_limit(kategoria, kwota):
                komunikat = "Przekroczono limit budżetowy dla tej kategorii!\nCzy chcesz mimo to dodać transakcję?"
                potwierdzenie = self.view.pobierz_potwierdzenie(komunikat)
                if not potwierdzenie:
                    self.view.wyswietl_komunikat("Transakcja nie została dodana.")
                    return
        transakcja = Transakcja(**dane)
        self.model.dodaj_transakcje(transakcja)
        self.view.wyswietl_komunikat("Transakcja dodana.")

    def edytuj_transakcje(self) -> None:
        self.view.wyswietl_transakcje(self.model.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if indeks == -1:
            return  # Anulowano operację
        if 0 <= indeks < len(self.model.transakcje):
            transakcja_oryginalna = self.model.transakcje[indeks]
            self.view.wyswietl_komunikat("Wprowadź nowe dane transakcji:")
            dane = self.view.pobierz_dane_transakcji(edycja=True)
            if not dane:
                return
            dane['typ'] = transakcja_oryginalna.typ  # Utrzymanie oryginalnego typu
            if dane['typ'] == 'wydatek':
                kwota = dane['kwota']
                kategoria = dane['kategoria']
                # Sprawdzenie, czy dodanie nowej kwoty przekroczy limit, uwzględniając oryginalny wydatek
                # Najpierw usuwamy oryginalny wydatek z kategorii, aby sprawdzić nowy
                self.model.wydatki_kategorie[transakcja_oryginalna.kategoria] -= transakcja_oryginalna.kwota
                if self.model.wydatki_kategorie[transakcja_oryginalna.kategoria] <= 0:
                    del self.model.wydatki_kategorie[transakcja_oryginalna.kategoria]
                if not self.model.sprawdz_limit(kategoria, kwota):
                    komunikat = "Przekroczono limit budżetowy dla tej kategorii!\nCzy chcesz mimo to zaktualizować transakcję?"
                    potwierdzenie = self.view.pobierz_potwierdzenie(komunikat)
                    if not potwierdzenie:
                        # Przywracamy oryginalny wydatek w kategorii
                        self.model.wydatki_kategorie[transakcja_oryginalna.kategoria] = self.model.wydatki_kategorie.get(transakcja_oryginalna.kategoria, 0) + transakcja_oryginalna.kwota
                        self.view.wyswietl_komunikat("Transakcja nie została zaktualizowana.")
                        return
            self.model.edytuj_transakcje(indeks, Transakcja(**dane))
            self.view.wyswietl_komunikat("Transakcja zaktualizowana.")
        else:
            self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")

    def usun_transakcje(self) -> None:
        self.view.wyswietl_transakcje(self.model.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if indeks == -1:
            return  # Anulowano operację
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

    def generuj_raport_wydatkow(self) -> None:
        raport = self.model.generuj_raport_wydatkow()
        self.view.wyswietl_raport_wydatkow(raport)

    def generuj_raport_przychodow(self) -> None:
        raport = self.model.generuj_raport_przychodow()
        self.view.wyswietl_raport_przychodow(raport)

    def wyswietl_wykresy(self) -> None:
        raport_wydatkow = self.model.generuj_raport_wydatkow()
        raport_przychodow = self.model.generuj_raport_przychodow()
        # Możesz wyświetlić osobne wykresy dla wydatków i przychodów lub połączyć je w jednym
        # Tutaj wyświetlimy tylko wykres wydatków jako przykład
        self.view.wyswietl_wykresy(raport_wydatkow)
