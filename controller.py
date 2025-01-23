from curses_view import BudzetCursesView
from service import BudzetService
from model import BudzetData, Transakcja

from fabrica import FabrykaWykresow

class BudzetController:
    def __init__(self) -> None:
        # Inicjalizujemy "puste" dane
        self.data = BudzetData()
        # Warstwa logiki (serwis)
        self.service = BudzetService(self.data)
        # Warstwa widoku (UI w curses)
        self.view = BudzetCursesView()
        self.zalogowany_uzytkownik = None

    def uruchom(self) -> None:
        try:
            self.view.wyswietl_ekran_powitalny()  # Wyświetlenie ekranu powitalnego
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

                match opcja:  # Python 3.10+ (match-case)
                    case '1':  # Transakcje
                        self.obsluz_podmenu_transakcje()
                    case '2':  # Podsumowania
                        self.obsluz_podmenu_podsumowania()
                    case '3':  # Limity
                        self.obsluz_podmenu_limity()
                    case '4':  # Cele
                        self.obsluz_podmenu_cele()
                    case '5':  # Importowanie i eksportowanie
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

    ####################################
    # PODMENU: TRANSASKCJE
    ####################################
    def obsluz_podmenu_transakcje(self) -> None:
        while True:
            self.view.wyswietl_podmenu_transakcje()
            opcja = self.view.pobierz_opcje_podmenu_transakcje()

            if opcja is None:
                # Użytkownik nacisnął ESC
                break

            match opcja:
                case '1':
                    self.dodaj_transakcje()
                case '2':
                    self.edytuj_transakcje()
                case '3':
                    self.usun_transakcje()
                case '4':
                    # Wyświetlanie w widoku
                    self.view.wyswietl_transakcje(self.data.transakcje)
                case '5':
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    ####################################
    def dodaj_transakcje(self) -> None:
        dane = self.view.pobierz_dane_transakcji()
        if not dane:
            return

        # Sprawdzanie limitu w serwisie
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
        self.view.wyswietl_transakcje(self.data.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if indeks == -1:
            return  # Anulowano operację

        if 0 <= indeks < len(self.data.transakcje):
            self.view.wyswietl_komunikat("Wprowadź nowe dane transakcji:")
            dane = self.view.pobierz_dane_transakcji(edycja=True)
            if not dane:
                return

            trans_orig = self.data.transakcje[indeks]
            # Typu w tym projekcie nie zmieniamy (niech pozostanie ten sam):
            dane['typ'] = trans_orig.typ

            # Sprawdzanie limitu (jeśli to wydatek)
            if dane['typ'].lower() == 'wydatek':
                kwota = dane['kwota']
                kategoria = dane['kategoria']
                # Najpierw cofniemy starą kwotę w serwisie, więc limit
                # weryfikujemy tak, jakby stara transakcja nie istniała (serwis to obsługuje internalnie).
                # Po wywołaniu edycji transakcji i tak sprawdzi jej wartość
                # i ewentualnie spytamy, czy użytkownik chce kontynuować.
                if not self.service.sprawdz_limit(kategoria, kwota):
                    komunikat = (
                        "Przekroczono limit budżetowy dla tej kategorii!\n"
                        "Czy chcesz mimo to zaktualizować transakcję?"
                    )
                    potwierdzenie = self.view.pobierz_potwierdzenie(komunikat)
                    if not potwierdzenie:
                        self.view.wyswietl_komunikat("Transakcja nie została zaktualizowana.")
                        return

            transakcja_nowa = Transakcja(**dane)
            if self.service.edytuj_transakcje(indeks, transakcja_nowa):
                self.view.wyswietl_komunikat("Transakcja zaktualizowana.")
            else:
                self.view.wyswietl_komunikat("Nie udało się edytować transakcji.")

        else:
            self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")

    def usun_transakcje(self) -> None:
        self.view.wyswietl_transakcje(self.data.transakcje)
        indeks = self.view.pobierz_indeks_transakcji()
        if indeks == -1:
            return  # Anulowano operację

        if self.service.usun_transakcje(indeks):
            self.view.wyswietl_komunikat("Transakcja usunięta.")
        else:
            self.view.wyswietl_komunikat("Nieprawidłowy numer transakcji.")

    ####################################
    # PODMENU: PODSUMOWANIA
    ####################################
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
                    self.generuj_raport_wydatkow()
                case '2':
                    self.generuj_raport_przychodow()
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
                    self.wyswietl_wykres('wydatki')
                case '2':
                    self.wyswietl_wykres('przychody')
                case '3':
                    break

    def generuj_raport_wydatkow(self) -> None:
        raport = self.service.generuj_raport_wydatkow()
        self.view.wyswietl_raport_wydatkow(raport)

    def generuj_raport_przychodow(self) -> None:
        raport = self.service.generuj_raport_przychodow()
        self.view.wyswietl_raport_przychodow(raport)

    def wyswietl_wykres(self, typ_wykresu: str) -> None:
        match typ_wykresu:
            case 'wydatki':
                raport = self.service.generuj_raport_wydatkow()
            case 'przychody':
                raport = self.service.generuj_raport_przychodow()
            case _:
                raport = {}

        wykres = FabrykaWykresow.utworz_wykres(typ_wykresu)
        wykres.rysuj(raport, self.view)

    ####################################
    # PODMENU: LIMITY
    ####################################
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
        limity = self.data.limity
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

    ####################################
    # PODMENU: IMPORT / EKSPORT
    ####################################
    def obsluz_podmenu_import_eksport(self) -> None:
        while True:
            self.view.wyswietl_podmenu_import_eksport()
            opcja = self.view.pobierz_opcje_podmenu_import_eksport()

            if opcja is None:
                break

            match opcja:
                case '1':  # Eksport CSV
                    try:
                        self.service.eksportuj_do_csv()
                        self.view.potwierdz_eksport('CSV')
                    except Exception as e:
                        self.view.wyswietl_komunikat(f"Błąd podczas eksportu do CSV: {str(e)}")
                case '2':  # Eksport JSON
                    try:
                        self.service.eksportuj_do_json()
                        self.view.potwierdz_eksport('JSON')
                    except Exception as e:
                        self.view.wyswietl_komunikat(f"Błąd podczas eksportu do JSON: {str(e)}")
                case '3':  # Import CSV
                    if self.service.importuj_z_csv():
                        self.view.potwierdz_import()
                    else:
                        self.view.wyswietl_komunikat("Nie udało się zaimportować transakcji z pliku 'transakcje.csv'.")
                case '4':  # Import JSON
                    if self.service.importuj_z_json():
                        self.view.wyswietl_komunikat("Transakcje zostały zaimportowane z pliku 'transakcje.json'.")
                    else:
                        self.view.wyswietl_komunikat("Nie udało się zaimportować transakcji z pliku 'transakcje.json'.")
                case '5':  # Powrót
                    break
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja. Spróbuj ponownie.")

    ####################################
    # PODMENU: CELE
    ####################################
    def obsluz_podmenu_cele(self) -> None:
        while True:
            cel = self.data.cel_oszczedzania
            if cel is None:
                # Nie powinno się zdarzyć, bo jest ustawiany przy logowaniu
                break

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
        if nowy_cel is not None:
            self.service.ustaw_nowy_cel(nowy_cel)
            self.view.wyswietl_komunikat(f"Ustawiono nowy cel oszczędności: {nowy_cel} zł")
            self.sprawdz_cel_osiagniety()

    def sprawdz_cel_osiagniety(self) -> None:
        if self.data.cel_oszczedzania is None:
            return
        cel = self.data.cel_oszczedzania
        if cel.cel_oszczednosci > 0:
            procent = (cel.obecneOszczednosci / cel.cel_oszczednosci) * 100
            if procent >= 100:
                self.view.wyswietl_komunikat("Gratulacje! Osiągnąłeś swój cel oszczędnościowy!")
        # Zapis do pliku
        self.service.zapisz_cel()

    def wyswietl_postep_celu(self) -> None:
        if self.data.cel_oszczedzania is None:
            return
        cel = self.data.cel_oszczedzania
        procent = 0
        if cel.cel_oszczednosci > 0:
            procent = (cel.obecneOszczednosci / cel.cel_oszczednosci) * 100
        self.view.wyswietl_postep_celu(procent)

    ####################################
    # LOGOWANIE / WYJŚCIE
    ####################################
    def logowanie(self) -> bool:
        while True:
            self.view.wyswietl_ekran_logowania()
            opcja = self.view.pobierz_opcje_logowania()

            if opcja is None:
                # Użytkownik nacisnął ESC podczas logowania
                potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                if potwierdzenie:
                    self.view.wyswietl_wyjscie()
                    self.view.zakoncz()
                    return False
                else:
                    continue

            match opcja:
                case '1':
                    login, haslo = self.view.pobierz_dane_logowania()
                    if login == "" and haslo == "":
                        continue
                    if self.service.zaloguj(login, haslo):
                        self.zalogowany_uzytkownik = login
                        self.view.wyswietl_komunikat(f"Zalogowano jako {login}.")
                        return True
                    else:
                        self.view.wyswietl_komunikat("Nieprawidłowy login lub hasło.")
                case '2':
                    login, haslo = self.view.pobierz_dane_rejestracji()
                    if login == "" and haslo == "":
                        continue
                    if self.service.zarejestruj(login, haslo):
                        self.view.wyswietl_komunikat("Rejestracja udana. Możesz się teraz zalogować.")
                    else:
                        self.view.wyswietl_komunikat("Użytkownik o takim loginie już istnieje.")
                case '3':
                    potwierdzenie = self.view.pobierz_potwierdzenie("Czy chcesz wyjść z aplikacji?")
                    if potwierdzenie:
                        self.view.wyswietl_wyjscie()
                        self.view.zakoncz()
                        return False
                    else:
                        continue
                case _:
                    self.view.wyswietl_komunikat("Nieprawidłowa opcja.")
