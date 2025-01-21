# view.py
import curses
from datetime import datetime
from typing import Optional, Tuple, Dict

ESC = 27  # Stała dla klawisza ESC


class BudzetCursesView:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Nowy kolor dla potwierdzenia
        self.current_row = 0

    def wyswietl_ekran_powitalny(self) -> None:
        self.stdscr.clear()
        ascii_art = [
            "  ____  _    _ _____   _____ ______ _______   __  __          _   _          _____ ______ _____  ",
            " |  _ \\| |  | |  __ \\ / ____|  ____|__   __| |  \\/  |   /\\   | \\ | |   /\\   / ____|  ____|  __ \\ ",
            " | |_) | |  | | |  | | |  __| |__     | |    | \\  / |  /  \\  |  \\| |  /  \\ | |  __| |__  | |__) |",
            " |  _ <| |  | | |  | | | |_ |  __|    | |    | |\\/| | / /\\ \\ | .  | / /\\ \\| | |_ |  __| |  _  / ",
            " | |_) | |__| | |__| | |__| | |____   | |    | |  | |/ ____ \\| |\\  |/ ____ \\ |__| | |____| | \\ \\ ",
            " |____/ \\____/|_____/ \\_____|______|  |_|    |_|  |_/_/    \\_\\_| \\_/_/    \\_\\_____|______|_|  \\_\\",
            "",
            "Kliknij Enter aby rozpocząć"
        ]
        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()
            for idx, line in enumerate(ascii_art):
                x = max((w // 2) - (len(line) // 2), 0)
                y = max((h // 2) - (len(ascii_art) // 2) + idx, 0)
                try:
                    self.stdscr.addstr(y, x, line)
                except curses.error:
                    pass
            self.stdscr.refresh()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk in [10, 13, curses.KEY_ENTER]:
                break
            elif wcisniety_przycisk == ESC:
                self.wyswietl_wyjscie()
                self.zakoncz()
                exit()

    def wyswietl_glowne_menu_kategorii(self) -> None:
        self.stdscr.clear()
        menu = [
            'Transakcje',
            'Podsumowania',
            'Limity',
            'Cele',  
            'Importowanie i eksportowanie',
            'Wyjście'
        ]
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_glownego_menu(self) -> Optional[str]:
        menu_length = 6 
        while True:
            self.wyswietl_glowne_menu_kategorii()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def wyswietl_podmenu_limity(self) -> None:
        self.stdscr.clear()
        menu = [
            'Ustaw limit',
            'Wyświetl limity',
            'Usuń limit',
            'Powrót do głównego menu'
        ]
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_limity(self) -> Optional[str]:
        menu_length = 4
        while True:
            self.wyswietl_podmenu_limity()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def wyswietl_podmenu_transakcje(self) -> None:
        self.stdscr.clear()
        menu = [
            'Dodaj transakcję',
            'Edytuj transakcję',
            'Usuń transakcję',
            'Wyświetl transakcje',
            'Powrót do głównego menu'
        ]
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_transakcje(self) -> Optional[str]:
        menu_length = 5
        while True:
            self.wyswietl_podmenu_transakcje()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def wyswietl_podmenu_podsumowania(self) -> None:
        self.stdscr.clear()
        menu = [
            'Wyświetl podsumowanie',
            'Tworzenie raportów',
            'Generowanie wykresów',
            'Powrót do głównego menu'
        ]
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_podsumowania(self) -> Optional[str]:
        menu_length = 4
        while True:
            self.wyswietl_podmenu_podsumowania()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def wyswietl_podmenu_raportow(self) -> None:
        self.stdscr.clear()
        menu = [
            'Generuj raport wydatków',
            'Generuj raport przychodów',
            'Powrót do menu Podsumowania'
        ]
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_raportow(self) -> Optional[str]:
        menu_length = 3
        while True:
            self.wyswietl_podmenu_raportow()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def wyswietl_podmenu_wykresow(self) -> None:
        self.stdscr.clear()
        menu = [
            'Wyświetl wykres wydatków',
            'Wyświetl wykres przychodów',
            'Powrót do menu Podsumowania'
        ]
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_wykresow(self) -> Optional[str]:
        menu_length = 3
        while True:
            self.wyswietl_podmenu_wykresow()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def wyswietl_menu_opcje(self, menu: list) -> None:
        h, w = self.stdscr.getmaxyx()
        for idx, row in enumerate(menu):
            x = max((w // 2) - (len(row) // 2), 0)
            y = max((h // 2) - (len(menu) // 2) + idx, 0)
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)

    def wyswietl_ekran_logowania(self) -> None:
        self.stdscr.clear()
        header = "Wybierz profil użytkownika, aby kontynuować"
        menu = [
            'Logowanie',
            'Rejestracja',
            'Wyjście'
        ]
        h, w = self.stdscr.getmaxyx()
        header_x = max((w // 2) - (len(header) // 2), 0)
        header_y = max((h // 2) - (len(menu) // 2) - 2, 0)
        try:
            self.stdscr.addstr(header_y, header_x, header, curses.A_BOLD | curses.A_UNDERLINE)
        except curses.error:
            pass
        for idx, row in enumerate(menu):
            x = max((w // 2) - (len(row) // 2), 0)
            y = max((h // 2) - (len(menu) // 2) + idx, 0)
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_logowania(self) -> Optional[str]:
        menu_length = 3
        while True:
            self.wyswietl_ekran_logowania()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def pobierz_dane_logowania(self) -> Tuple[str, str]:
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Login: ")
        login = self.pobierz_input(1, 20, 20)
        if login is None:
            curses.noecho()
            return "", ""
        self.stdscr.addstr(2, 1, "Hasło: ")
        haslo = self.pobierz_input(2, 20, 20)
        curses.noecho()
        if haslo is None:
            return "", ""
        return login, haslo

    def pobierz_dane_rejestracji(self) -> Tuple[str, str]:
        return self.pobierz_dane_logowania()

    def pobierz_input(self, y: int, x_start: int, max_length: int) -> Optional[str]:
        input_str = ""
        self.stdscr.move(y, x_start)
        self.stdscr.clrtoeol()
        while True:
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk in [10, 13]: 
                break
            elif wcisniety_przycisk == ESC:
                return None
            elif wcisniety_przycisk in [curses.KEY_BACKSPACE, 127, 8]:
                if len(input_str) > 0:
                    input_str = input_str[:-1]
                    self.stdscr.delch(y, x_start + len(input_str))
            elif wcisniety_przycisk >= 32 and len(input_str) < max_length:
                input_str += chr(wcisniety_przycisk)
                self.stdscr.addch(y, x_start + len(input_str) - 1, wcisniety_przycisk)
        if input_str == "":
            return None
        return input_str.strip()

    def pobierz_dane_transakcji(self, edycja: bool = False) -> Optional[dict]:
        curses.echo()
        self.stdscr.clear()
        start_row = 1
        transakcja = {}
        try:
            if not edycja:
                self.stdscr.addstr(start_row, 1, "Typ (przychód/wydatek): ")
                typ = self.pobierz_input(start_row, 25, 20)
                if typ is None:
                    raise ValueError("Anulowano operację.")
                typ = typ.lower()
                if typ not in ['przychód', 'wydatek']:
                    raise ValueError("Nieprawidłowy typ transakcji.")
                transakcja['typ'] = typ
                start_row += 1

            self.stdscr.addstr(start_row, 1, "Kwota: ")
            kwota_input = self.pobierz_input(start_row, 15, 20)
            if kwota_input is None:
                raise ValueError("Anulowano operację.")
            kwota = float(kwota_input)
            transakcja['kwota'] = kwota
            start_row += 1

            self.stdscr.addstr(start_row, 1, "Kategoria: ")
            kategoria = self.pobierz_input(start_row, 15, 20)
            if kategoria is None or not kategoria:
                raise ValueError("Kategoria nie może być pusta.")
            transakcja['kategoria'] = kategoria
            start_row += 1

            self.stdscr.addstr(start_row, 1, "Opis (opcjonalnie): ")
            opis = self.pobierz_input(start_row, 25, 50)
            if opis is None:
                opis = ""
            transakcja['opis'] = opis
            start_row += 1

            self.stdscr.addstr(start_row, 1, "Data (YYYY-MM-DD) [opcjonalnie]: ")
            data_input = self.pobierz_input(start_row, 35, 10)
            if data_input is None:
                transakcja['data'] = datetime.now().strftime('%Y-%m-%d')
            else:
                try:
                    datetime.strptime(data_input, '%Y-%m-%d')
                    transakcja['data'] = data_input
                except ValueError:
                    raise ValueError("Nieprawidłowy format daty.")
        except ValueError as e:
            self.wyswietl_komunikat(f"{e}")
            transakcja = {}
        finally:
            curses.noecho()
        return transakcja if transakcja else None

    def wyswietl_transakcje(self, transakcje: list) -> None:
        self.stdscr.clear()
        if not transakcje:
            self.stdscr.addstr(1, 1, "Brak transakcji.")
            self.wyswietl_footer()
            self.stdscr.refresh()
            self.stdscr.getch()
            return
        header = "Nr | Data       | Typ      | Kwota    | Kategoria     | Opis"
        self.stdscr.addstr(0, 1, header)
        self.stdscr.addstr(1, 1, "-" * len(header))
        h, w = self.stdscr.getmaxyx()
        per_page = h - 4
        total_pages = (len(transakcje) + per_page - 1) // per_page
        current_page = 0

        while True:
            self.stdscr.clear()
            self.stdscr.addstr(0, 1, header)
            self.stdscr.addstr(1, 1, "-" * len(header))
            start = current_page * per_page
            end = start + per_page
            for i, t in enumerate(transakcje[start:end], start=start):
                linia = f"{i}. | {t.data} | {t.typ.capitalize():8} | {t.kwota:9.2f} | {t.kategoria:13} | {t.opis}"
                try:
                    self.stdscr.addstr(i - start + 2, 1, linia)
                except curses.error:
                    break
            footer = f"Strona {current_page + 1}/{total_pages}. Naciśnij 'n' dla następnej strony, 'p' dla poprzedniej, 'q' aby wyjść lub ESC aby anulować."
            self.stdscr.addstr(h-3, 1, footer)
            self.wyswietl_footer()
            self.stdscr.refresh()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk in [ord('n'), ord('N')]:
                if current_page < total_pages - 1:
                    current_page += 1
            elif wcisniety_przycisk in [ord('p'), ord('P')]:
                if current_page > 0:
                    current_page -= 1
            elif wcisniety_przycisk in [ord('q'), ord('Q'), ESC]:
                break

    def wyswietl_podsumowanie(self, saldo: float) -> None:
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, f"Aktualne saldo: {saldo:.2f} zł")
        self.wyswietl_footer()
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_indeks_transakcji(self) -> int:
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Podaj numer transakcji: ")
        indeks_input = self.pobierz_input(1, 30, 5)
        curses.noecho()
        if indeks_input is None:
            return -1
        try:
            indeks = int(indeks_input)
            return indeks
        except ValueError:
            self.wyswietl_komunikat("Nieprawidłowy format numeru.")
            return -1

    def wyswietl_komunikat(self, komunikat: str) -> None:
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, komunikat)
        self.wyswietl_footer()
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_limit(self) -> Tuple[Optional[str], float]:
        curses.echo()
        self.stdscr.clear()
        try:
            self.stdscr.addstr(1, 1, "Podaj kategorię: ")
            kategoria = self.pobierz_input(1, 20, 20)
            if kategoria is None:
                raise ValueError("Anulowano operację.")
            self.stdscr.addstr(2, 1, "Podaj limit: ")
            limit_input = self.pobierz_input(2, 25, 20)
            if limit_input is None:
                raise ValueError("Anulowano operację.")
            limit = float(limit_input)
            if limit <= 0:
                raise ValueError("Limit musi być większy od zera.")
            return kategoria, limit
        except ValueError as e:
            self.wyswietl_komunikat(f"{e}")
            return None, 0.0
        finally:
            curses.noecho()

    
    def potwierdz_eksport(self, format_pliku: str = '') -> None:
        """Wyświetla potwierdzenie eksportu"""
        nazwa_pliku = 'transakcje.csv' if format_pliku.lower() == 'csv' else 'transakcje.json'
        self.wyswietl_komunikat(f"Transakcje zostały wyeksportowane do pliku '{nazwa_pliku}'.")

    def potwierdz_import(self) -> None:
        self.wyswietl_komunikat("Transakcje zostały zaimportowane z pliku 'transakcje.csv'.")

    def potwierdz_ustawienie_limitu(self, kategoria: str, limit: float) -> None:
        self.wyswietl_komunikat(f"Ustawiono limit {limit:.2f} zł dla kategorii '{kategoria}'.")

    def wyswietl_raport_wydatkow(self, raport: Dict[str, float]) -> None:
        self.stdscr.clear()
        if not raport:
            self.stdscr.addstr(1, 1, "Brak wydatków do wyświetlenia.")
        else:
            self.stdscr.addstr(0, 1, "Raport wydatków według kategorii:")
            row = 1
            for kategoria, suma in raport.items():
                self.stdscr.addstr(row, 1, f"{kategoria}: {suma:.2f} zł")
                row += 1
        self.wyswietl_footer()
        self.stdscr.refresh()
        self.stdscr.getch()

    def wyswietl_raport_przychodow(self, raport: Dict[str, float]) -> None:
        self.stdscr.clear()
        if not raport:
            self.stdscr.addstr(1, 1, "Brak przychodów do wyświetlenia.")
        else:
            self.stdscr.addstr(0, 1, "Raport przychodów według kategorii:")
            row = 1
            for kategoria, suma in raport.items():
                self.stdscr.addstr(row, 1, f"{kategoria}: {suma:.2f} zł")
                row += 1
        self.wyswietl_footer()
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_zakres_dat(self) -> Tuple[Optional[str], Optional[str]]:
        curses.echo()
        self.stdscr.clear()
        try:
            self.stdscr.addstr(1, 1, "Podaj datę początkową (YYYY-MM-DD): ")
            data_poczatkowa = self.pobierz_input(1, 40, 10)
            if data_poczatkowa is None:
                raise ValueError("Anulowano operację.")
            datetime.strptime(data_poczatkowa, '%Y-%m-%d')  # Walidacja
            self.stdscr.addstr(2, 1, "Podaj datę końcową (YYYY-MM-DD): ")
            data_koncowa = self.pobierz_input(2, 40, 10)
            if data_koncowa is None:
                raise ValueError("Anulowano operację.")
            datetime.strptime(data_koncowa, '%Y-%m-%d')  # Walidacja
            return data_poczatkowa, data_koncowa
        except ValueError as e:
            self.wyswietl_komunikat(f"{e}")
            return None, None
        finally:
            curses.noecho()


    def wyswietl_wyjscie(self) -> None:
        ascii_art = [
            "  ____  _    _ _____   _____ ______ _______   __  __          _   _          _____ ______ _____  ",
            " |  _ \\| |  | |  __ \\ / ____|  ____|__   __| |  \\/  |   /\\   | \\ | |   /\\   / ____|  ____|  __ \\ ",
            " | |_) | |  | | |  | | |  __| |__     | |    | \\  / |  /  \\  |  \\| |  /  \\ | |  __| |__  | |__) |",
            " |  _ <| |  | | |  | | | |_ |  __|    | |    | |\\/| | / /\\ \\ | .  | / /\\ \\| | |_ |  __| |  _  / ",
            " | |_) | |__| | |__| | |__| | |____   | |    | |  | |/ ____ \\| |\\  |/ ____ \\ |__| | |____| | \\ \\ ",
            " |____/ \\____/|_____/ \\_____|______|  |_|    |_|  |_/_/    \\_\\_| \\_/_/    \\_\\_____|______|_|  \\_\\",
            "",
            "Wylogowano oraz zamknięto program"
        ]
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        for idx, line in enumerate(ascii_art):
            x = max((w // 2) - (len(line) // 2), 0)
            y = max((h // 2) - (len(ascii_art) // 2) + idx, 0)
            try:
                self.stdscr.addstr(y, x, line)
            except curses.error:
                pass
        self.stdscr.refresh()
        self.stdscr.getch()

    def zakoncz(self) -> None:
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def pobierz_potwierdzenie(self, komunikat: str) -> bool:
        menu = ['Tak', 'Nie']
        self.current_row = 0
        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()
            try:
                self.stdscr.addstr(1, max((w // 2) - (len(komunikat) // 2), 0), komunikat)
            except curses.error:
                pass
            for idx, row in enumerate(menu):
                x = max((w // 2) - (len(row) // 2), 0)
                y = max((h // 2) - 1 + idx, 0)
                if idx == self.current_row:
                    self.stdscr.attron(curses.color_pair(2))
                    self.stdscr.addstr(y, x, row)
                    self.stdscr.attroff(curses.color_pair(2))
                else:
                    self.stdscr.addstr(y, x, row)
            self.wyswietl_footer()
            self.stdscr.refresh()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < len(menu) - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                return self.current_row == 0
            elif wcisniety_przycisk == ESC:
                return False

    def wyswietl_footer(self) -> None:
        h, w = self.stdscr.getmaxyx()
        footer_text = "BUDGET MANAGER"
        try:
            self.stdscr.addstr(h - 1, max((w // 2) - (len(footer_text) // 2), 0), footer_text, curses.A_DIM)
        except curses.error:
            pass

    def wyswietl_limity(self, limity: Dict[str, float]) -> None:
        self.stdscr.clear()
        if not limity:
            self.stdscr.addstr(1, 1, "Brak ustawionych limitów.")
        else:
            self.stdscr.addstr(0, 1, "Aktualne limity:")
            row = 1
            for kategoria, limit in limity.items():
                self.stdscr.addstr(row, 1, f"{kategoria}: {limit:.2f} zł")
                row += 1
        self.wyswietl_footer()
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_kategorie_do_usuniecia(self) -> Optional[str]:
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Podaj kategorię, dla której chcesz usunąć limit: ")
        kategoria = self.pobierz_input(1, 55, 20)
        curses.noecho()
        if kategoria is None or kategoria.strip() == "":
            return None
        return kategoria.strip()

    def wyswietl_podmenu_import_eksport(self) -> None:
            self.stdscr.clear()
            menu = [
                'Eksportuj transakcje do CSV',
                'Eksportuj transakcje do JSON',
                'Importuj transakcje z CSV',
                'Importuj transakcje z JSON',
                'Powrót do głównego menu'
            ]
            self.wyswietl_menu_opcje(menu)
            self.wyswietl_footer()
            self.stdscr.refresh()

    def pobierz_opcje_podmenu_import_eksport(self) -> Optional[str]:
        menu_length = 5  # Zaktualizowana długość menu
        while True:
            self.wyswietl_podmenu_import_eksport()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                return str(self.current_row + 1)
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def pobierz_opcje_podmenu_import_eksport(self) -> Optional[str]:
        menu_length = 5
        while True:
            self.wyswietl_podmenu_import_eksport()
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                return str(self.current_row + 1)
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def wyswietl_podmenu_cele(self, cel_oszczednosci: float, obecneOszczednosci: float) -> None:
        self.stdscr.clear()
        menu = [
            'Ustaw cel oszczędności',
            'Wyświetl postęp celu',
            'Powrót do głównego menu'
        ]
        self.stdscr.addstr(0, 1, f"Aktualny cel oszczędności: {cel_oszczednosci:.2f} zł")
        self.stdscr.addstr(1, 1, f"Obecne oszczędności: {obecneOszczednosci:.2f} zł")
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_cele(self, cel_oszczednosci: float, obecneOszczednosci: float) -> Optional[str]:
        menu_length = 3
        while True:
            self.wyswietl_podmenu_cele(cel_oszczednosci, obecneOszczednosci)
            wcisniety_przycisk = self.stdscr.getch()
            if wcisniety_przycisk == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif wcisniety_przycisk == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif wcisniety_przycisk in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif wcisniety_przycisk == ESC:
                return None
            self.stdscr.refresh()

    def pobierz_cel_oszczednosci(self) -> Optional[float]:
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Podaj nowy cel oszczędności (w zł): ")
        cel_input = self.pobierz_input(1, 35, 20)
        curses.noecho()
        if cel_input is None:
            return None
        try:
            cel = float(cel_input)
            if cel <= 0:
                raise ValueError("Cel musi być większy od zera.")
            return cel
        except ValueError:
            self.wyswietl_komunikat("Nieprawidłowy format celu.")
            return None

    def wyswietl_postep_celu(self, procent: float) -> None:
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, f"Postęp w realizacji celu oszczędności: {procent:.2f}%")
        if procent >= 100:
            self.stdscr.addstr(2, 1, "Gratulacje! Osiągnąłeś swój cel oszczędnościowy!", curses.A_BOLD)
        self.wyswietl_footer()
        self.stdscr.refresh()
        self.stdscr.getch()

    def wyswietl_menu_formatu_eksportu(self) -> None:
        """Wyświetla menu wyboru formatu eksportu"""
        self.stdscr.clear()
        menu = [
            'Eksportuj do CSV',
            'Eksportuj do JSON',
            'Powrót'
        ]
        h, w = self.stdscr.getmaxyx()
        header = "=== Wybierz format eksportu ==="
        try:
            self.stdscr.addstr(0, max((w // 2) - (len(header) // 2), 0), header)
        except curses.error:
            pass
        
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()
    
