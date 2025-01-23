from model import BudzetModel, Transakcja
from budzet_service import BudzetService
from curses_view import BudzetCursesView
from fabrica import FabrykaWykresow

class BudzetController:
    def __init__(self) -> None:
        self.model = BudzetModel()               # Puste dane
        self.service = BudzetService(self.model) # Warstwa logiki
        self.view = BudzetCursesView()
        self.zalogowany_uzytkownik = None

    def uruchom(self) -> None:
        try:
            self.view.wyswietl_ekran_powitalny()
            if not self.logowanie():
                return
            while True:
                self.view.wyswietl_glowne_menu_kategorii()
                opcja = self.view.pobierz_opcje_glownego_menu()
                if opcja is None:
                    potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                    if potwierdzenie:
                        self.view.wyswietl_wyjscie()
                        break
                    else:
                        continue

                match opcja:
                    case '1':  # Transakcje
                        self.obsluz_podmenu_transakcje()
                    case '2':  # Podsumowania
                        self.obsluz_podmenu_podsumowania()
                    case '3':  # Limity
                        self.obsluz_podmenu_limity()
                    case '4':  # Cele
                        self.obsluz_podmenu_cele()
                    case '5':  # Import i eksport
                        self.obsluz_podmenu_import_eksport()
                    case '6':  # Wyjście
                        self.view.wyswietl_wyjscie()
                        break
                    case _:
                        self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")
        except Exception as e:
            self.view.wyswietl_komunikat(f"Wystąpił błąd: {e}")
        finally:
            self.view.zakoncz()

    def logowanie(self) -> bool:
        while True:
            self.view.wyswietl_ekran_logowania()
            opcja = self.view.pobierz_opcje_logowania()
            if opcja is None:
                potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                if potwierdzenie:
                    self.view.wyswietl_wyjscie()
                    self.view.zakoncz()
                    return False
                else:
                    continue

            match opcja:
                case '1':  # Logowanie
                    login, haslo = self.view.pobierz_dane_logowania()
                    if login == "" and haslo == "":
                        continue
                    if self.service.zaloguj(login, haslo):
                        self.zalogowany_uzytkownik = login
                        self.view.wyswietl_komunikat(f"Zalogowano jako {login}.")
                        return True
                    else:
                        self.view.wyswietl_komunikat("Nieprawidłowy login lub hasło.")
                case '2':  # Rejestracja
                    login, haslo = self.view.pobierz_dane_rejestracji()
                    if login == "" and haslo == "":
                        continue
                    if self.service.zarejestruj(login, haslo):
                        self.view.wyswietl_komunikat("Rejestracja udana. Możesz się teraz zalogować.")
                    else:
                        self.view.wyswietl_komunikat("Użytkownik o takim loginie już istnieje.")
                case '3':  # Wyjście
                    potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                    if potwierdzenie:
                        self.view.wyswietl_wyjscie()
                        self.view.zakoncz()
                        return False
                    else:
                        continue
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja.")

    # -----------------------------
    # Podmenu Transakcje
    # -----------------------------
    def obsluz_podmenu_transakcje(self) -> None:
        while True:
            self.view.wyswietl_podmenu_transakcje()
            opcja = self.view.pobierz_opcje_podmenu_transakcje()
            if opcja is None:
                break
            match opcja:
                case '1':
                    self.dodaj_transakcje()
                case '2':
                    self.edytuj_transakcje()
                case '3':
                    self.usun_transakcje()
                case '4':
                    self.view.wyswietl_transakcje(self.model.transakcje)
                case '5':
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def dodaj_transakcje(self) -> None:
        dane = self.view.pobierz_dane_transakcji()
        if not dane:
            return
        if dane['typ'] == 'wydatek':
            kwota = dane['kwota']
            kategoria = dane['kategoria']
            if not self.service.sprawdz_limit(kategoria, kwota):
                komunikat = "Przekroczono limit budżetowy dla tej kategorii! Czy chcesz mimo to dodać transakcję?"
                potwierdzenie = self.view.pobierz_potwierdzenie(komunikat)
                if not potwierdzenie:
                    self.view.wyswietl_komunikat("Transakcja nie została dodana.")
                    return
        transakcja = Transakcja(**dane)
        self.service.dodaj_transakcje(transakcja)
        self.view.wyswietl_komunikat("Transakcja dodana.")

    def edytuj_transakcje(self) -> None:
        self.view.wyswietl_transakcje(self.model.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if indeks == -1:
            return
        if 0 <= indeks < len(self.model.transakcje):
            stara = self.model.transakcje[indeks]
            self.view.wyswietl_komunikat("Wprowadź nowe dane transakcji:")
            dane = self.view.pobierz_dane_transakcji(edycja=True)
            if not dane:
                return
            # Zostawiamy oryginalny typ, jeśli tak chcemy
            dane['typ'] = stara.typ
            if dane['typ'] == 'wydatek':
                kwota = dane['kwota']
                kategoria = dane['kategoria']
                # Tymczasowe zdjęcie starej kwoty z kategorii już następuje w serwisie,
                # ale tutaj można sprawdzić limit
                if not self.service.sprawdz_limit(kategoria, kwota):
                    komunikat = ("Przekroczono limit budżetowy!\nCzy chcesz mimo to zaktualizować transakcję?")
                    potwierdzenie = self.view.pobierz_potwierdzenie(komunikat)
                    if not potwierdzenie:
                        self.view.wyswietl_komunikat("Transakcja nie została zaktualizowana.")
                        return
            nowa_transakcja = Transakcja(**dane)
            if self.service.edytuj_transakcje(indeks, nowa_transakcja):
                self.view.wyswietl_komunikat("Transakcja zaktualizowana.")
            else:
                self.view.wyswietl_komunikat("Nieprawidłowy indeks transakcji.")
        else:
            self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")

    def usun_transakcje(self) -> None:
        self.view.wyswietl_transakcje(self.model.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if indeks == -1:
            return
        if self.service.usun_transakcje(indeks):
            self.view.wyswietl_komunikat("Transakcja usunięta.")
        else:
            self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")

    # -----------------------------
    # Podmenu Podsumowania
    # -----------------------------
    def obsluz_podmenu_podsumowania(self) -> None:
        while True:
            self.view.wyswietl_podmenu_podsumowania()
            opcja = self.view.pobierz_opcje_podmenu_podsumowania()
            if opcja is None:
                break
            match opcja:
                case '1':
                    self.wyswietl_podsumowanie()
                case '2':
                    self.obsluz_podmenu_raportow()
                case '3':
                    self.obsluz_podmenu_wykresow()
                case '4':
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def wyswietl_podsumowanie(self) -> None:
        saldo = self.service.oblicz_saldo()
        self.view.wyswietl_podsumowanie(saldo)

    def obsluz_podmenu_raportow(self) -> None:
        while True:
            self.view.wyswietl_podmenu_raportow()
            opcja = self.view.pobierz_opcje_podmenu_raportow()
            if opcja is None:
                break
            match opcja:
                case '1':
                    raport = self.service.generuj_raport_wydatkow()
                    self.view.wyswietl_raport_wydatkow(raport)
                case '2':
                    raport = self.service.generuj_raport_przychodow()
                    self.view.wyswietl_raport_przychodow(raport)
                case '3':
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def obsluz_podmenu_wykresow(self) -> None:
        while True:
            self.view.wyswietl_podmenu_wykresow()
            opcja = self.view.pobierz_opcje_podmenu_wykresow()
            if opcja is None:
                break
            match opcja:
                case '1':
                    raport = self.service.generuj_raport_wydatkow()
                    wykres = FabrykaWykresow.utworz_wykres('wydatki')
                    wykres.rysuj(raport, self.view)
                case '2':
                    raport = self.service.generuj_raport_przychodow()
                    wykres = FabrykaWykresow.utworz_wykres('przychody')
                    wykres.rysuj(raport, self.view)
                case '3':
                    break

    # -----------------------------
    # Podmenu Limity
    # -----------------------------
    def obsluz_podmenu_limity(self) -> None:
        while True:
            self.view.wyswietl_podmenu_limity()
            opcja = self.view.pobierz_opcje_podmenu_limity()
            if opcja is None:
                break
            match opcja:
                case '1':
                    self.ustaw_limit_budzetowy()
                case '2':
                    self.wyswietl_limity()
                case '3':
                    self.usun_limit()
                case '4':
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def ustaw_limit_budzetowy(self) -> None:
        kategoria, limit = self.view.pobierz_limit()
        if kategoria and limit > 0:
            self.service.ustaw_limit(kategoria, limit)
            self.view.potwierdz_ustawienie_limitu(kategoria, limit)
        else:
            self.view.wyswietl_komunikat("Nieprawidłowe dane. Limit nie został ustawiony.")

    def wyswietl_limity(self) -> None:
        limity = self.model.limity
        self.view.wyswietl_limity(limity)

    def usun_limit(self) -> None:
        kategoria = self.view.pobierz_kategorie_do_usuniecia()
        if kategoria is None:
            self.view.wyswietl_komunikat("Anulowano operację.")
            return
        if self.service.usun_limit(kategoria):
            self.view.wyswietl_komunikat(f"Limit dla kategorii '{kategoria}' został usunięty.")
        else:
            self.view.wyswietl_komunikat(f"Limit dla kategorii '{kategoria}' nie istnieje.")

    # -----------------------------
    # Podmenu Cele oszczędności
    # -----------------------------
    def obsluz_podmenu_cele(self) -> None:
        while True:
            cel = self.model.cel_oszczedzania
            if not cel:
                self.view.wyswietl_komunikat("Brak zdefiniowanego celu oszczędnościowego.")
                return
            opcja = self.view.pobierz_opcje_podmenu_cele(cel.cel_oszczednosci, cel.obecneOszczednosci)
            if opcja is None:
                break
            match opcja:
                case '1':
                    self.ustaw_cel_oszczednosci()
                case '2':
                    self.wyswietl_postep_celu()
                case '3':
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    def ustaw_cel_oszczednosci(self) -> None:
        nowy_cel = self.view.pobierz_cel_oszczednosci()
        if nowy_cel is not None and self.model.cel_oszczedzania:
            self.model.cel_oszczedzania.ustaw_nowy_cel(nowy_cel)
            self.view.wyswietl_komunikat(f"Ustawiono nowy cel oszczędności: {nowy_cel} zł")
            self.sprawdz_cel_osiagniety()

    def sprawdz_cel_osiagniety(self) -> None:
        cel = self.model.cel_oszczedzania
        if not cel or cel.cel_oszczednosci == 0:
            return
        procent = (cel.obecneOszczednosci / cel.cel_oszczednosci) * 100
        if procent >= 100:
            self.view.wyswietl_komunikat("Gratulacje! Osiągnąłeś swój cel oszczędnościowy!")

    def wyswietl_postep_celu(self) -> None:
        cel = self.model.cel_oszczedzania
        if not cel or cel.cel_oszczednosci == 0:
            self.view.wyswietl_komunikat("Brak celu do wyświetlenia.")
            return
        procent = (cel.obecneOszczednosci / cel.cel_oszczednosci) * 100
        self.view.wyswietl_postep_celu(procent)

    # -----------------------------
    # Podmenu Import/Eksport
    # -----------------------------
    def obsluz_podmenu_import_eksport(self) -> None:
        while True:
            self.view.wyswietl_podmenu_import_eksport()
            opcja = self.view.pobierz_opcje_podmenu_import_eksport()
            if opcja is None:
                break
            match opcja:
                case '1':  # Eksport CSV
                    try:
                        sciezka_csv = "data/exports/transakcje.csv"
                        self.service.eksportuj_do_csv(sciezka_csv)
                        self.view.potwierdz_eksport('CSV')
                    except Exception as e:
                        self.view.wyswietl_komunikat(f"Błąd podczas eksportu do CSV: {str(e)}")
                case '2':  # Eksport JSON
                    try:
                        sciezka_json = "data/exports/transakcje.json"
                        self.service.eksportuj_do_json(sciezka_json)
                        self.view.potwierdz_eksport('JSON')
                    except Exception as e:
                        self.view.wyswietl_komunikat(f"Błąd podczas eksportu do JSON: {str(e)}")
                case '3':  # Import CSV
                    sciezka_csv = "data/exports/transakcje.csv"
                    if self.service.importuj_z_csv(sciezka_csv):
                        self.view.potwierdz_import()
                    else:
                        self.view.wyswietl_komunikat("Nie udało się zaimportować z CSV.")
                case '4':  # Import JSON
                    sciezka_json = "data/exports/transakcje.json"
                    if self.service.importuj_z_json(sciezka_json):
                        self.view.wyswietl_komunikat("Zaimportowano transakcje z pliku JSON.")
                    else:
                        self.view.wyswietl_komunikat("Nie udało się zaimportować z JSON.")
                case '5':  # Powrót
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")
