# curses_view.py
import curses
from datetime import datetime
from typing import Optional, Tuple, Dict

class BudzetCursesView:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Nowy kolor dla potwierdzenia
        self.current_row = 0

    def wyswietl_welcome_screen(self) -> None:
        self.stdscr.clear()
        ascii_art = [
            "  ____  _    _ _____   _____ ______ _______   __  __          _   _          _____ ______ _____  ",
            " |  _ \\| |  | |  __ \\ / ____|  ____|__   __| |  \\/  |   /\\   | \\ | |   /\\   / ____|  ____|  __ \\ ",
            " | |_) | |  | | |  | | |  __| |__     | |    | \\  / |  /  \\  |  \\| |  /  \\ | |  __| |__  | |__) |",
            " |  _ <| |  | | |  | | | |_ |  __|    | |    | |\\/| | / /\\ \\ | . ` | / /\\ \\| | |_ |  __| |  _  / ",
            " | |_) | |__| | |__| | |__| | |____   | |    | |  | |/ ____ \\| |\\  |/ ____ \\ |__| | |____| | \\ \\ ",
            " |____/ \\____/|_____/ \\_____|______|  |_|    |_|  |_/_/    \\_\\_| \\_/_/    \\_\\_____|______|_|  \\_\\",
            "",
            "Kliknij Enter aby rozpocząć"
        ]
        h, w = self.stdscr.getmaxyx()
        for idx, line in enumerate(ascii_art):
            x = max((w // 2) - (len(line) // 2), 0)
            y = max((h // 2) - (len(ascii_art) // 2) + idx, 0)
            try:
                self.stdscr.addstr(y, x, line)
            except curses.error:
                pass
        self.stdscr.refresh()
        while True:
            key = self.stdscr.getch()
            if key in [10, 13, curses.KEY_ENTER]:
                break

    def wyswietl_glowne_menu_kategorii(self) -> None:
        self.stdscr.clear()
        menu = [
            'Transakcje',
            'Podsumowania',
            'Importowanie i eksportowanie',
            'Wyjście'
        ]
        self.wyswietl_menu_opcje(menu)
        self.stdscr.refresh()

    def pobierz_opcje_glownego_menu(self) -> str:
        menu_length = 4
        while True:
            self.wyswietl_glowne_menu_kategorii()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return str(self.current_row + 1)
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
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_transakcje(self) -> str:
        menu_length = 5
        while True:
            self.wyswietl_podmenu_transakcje()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return str(self.current_row + 1)
            self.stdscr.refresh()

    def wyswietl_podmenu_podsumowania(self) -> None:
        self.stdscr.clear()
        menu = [
            'Wyświetl podsumowanie',
            'Generuj raport wydatków',
            'Wyświetl wykresy',
            'Powrót do głównego menu'
        ]
        self.wyswietl_menu_opcje(menu)
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_podsumowania(self) -> str:
        menu_length = 4
        while True:
            self.wyswietl_podmenu_podsumowania()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return str(self.current_row + 1)
            self.stdscr.refresh()

    def wyswietl_podmenu_import_eksport(self) -> None:
        self.stdscr.clear()
        menu = [
            'Eksportuj transakcje do CSV',
            'Importuj transakcje z CSV',
            'Powrót do głównego menu'
        ]
        self.wyswietl_menu_opcje(menu)
        self.stdscr.refresh()

    def pobierz_opcje_podmenu_import_eksport(self) -> str:
        menu_length = 3
        while True:
            self.wyswietl_podmenu_import_eksport()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return str(self.current_row + 1)
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

    def pobierz_opcje(self) -> str:
        # Ta metoda została zastąpiona przez specyficzne metody pobierania opcji dla każdego menu
        pass

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
        self.stdscr.refresh()

    def pobierz_opcje_logowania(self) -> str:
        menu_length = 3
        while True:
            self.wyswietl_ekran_logowania()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return str(self.current_row + 1)
            self.stdscr.refresh()

    def pobierz_dane_logowania(self) -> Tuple[str, str]:
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Login: ")
        login = self.stdscr.getstr(1, 10, 20).decode('utf-8').strip()
        self.stdscr.addstr(2, 1, "Hasło: ")
        haslo = self.stdscr.getstr(2, 10, 20).decode('utf-8').strip()
        curses.noecho()
        return login, haslo

    def pobierz_dane_rejestracji(self) -> Tuple[str, str]:
        return self.pobierz_dane_logowania()

    def pobierz_dane_transakcji(self, edycja: bool = False) -> Optional[dict]:
        curses.echo()
        self.stdscr.clear()
        start_row = 1
        transakcja = {}
        try:
            if not edycja:
                self.stdscr.addstr(start_row, 1, "Typ (przychód/wydatek): ")
                typ = self.stdscr.getstr(start_row, 25, 20).decode('utf-8').strip().lower()
                if typ not in ['przychód', 'wydatek']:
                    raise ValueError("Nieprawidłowy typ transakcji.")
                transakcja['typ'] = typ
                start_row += 1

            self.stdscr.addstr(start_row, 1, "Kwota: ")
            kwota_input = self.stdscr.getstr(start_row, 25, 20).decode('utf-8').strip()
            kwota = float(kwota_input)
            transakcja['kwota'] = kwota
            start_row += 1

            self.stdscr.addstr(start_row, 1, "Kategoria: ")
            kategoria = self.stdscr.getstr(start_row, 25, 20).decode('utf-8').strip()
            if not kategoria:
                raise ValueError("Kategoria nie może być pusta.")
            transakcja['kategoria'] = kategoria
            start_row += 1

            self.stdscr.addstr(start_row, 1, "Opis (opcjonalnie): ")
            opis = self.stdscr.getstr(start_row, 25, 50).decode('utf-8').strip()
            transakcja['opis'] = opis
            start_row += 1

            self.stdscr.addstr(start_row, 1, "Data (YYYY-MM-DD) [opcjonalnie]: ")
            data_input = self.stdscr.getstr(start_row, 35, 10).decode('utf-8').strip()
            if data_input:
                try:
                    datetime.strptime(data_input, '%Y-%m-%d')
                    transakcja['data'] = data_input
                except ValueError:
                    raise ValueError("Nieprawidłowy format daty.")
            else:
                transakcja['data'] = datetime.now().strftime('%Y-%m-%d')
        except ValueError as e:
            self.wyswietl_komunikat(f"Błąd: {e}")
            transakcja = {}
        finally:
            curses.noecho()
        return transakcja if transakcja else None

    def wyswietl_transakcje(self, transakcje: list) -> None:
        self.stdscr.clear()
        if not transakcje:
            self.stdscr.addstr(1, 1, "Brak transakcji.")
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
            footer = f"Strona {current_page + 1}/{total_pages}. Naciśnij 'n' dla następnej strony, 'p' dla poprzedniej lub 'q' aby wyjść."
            self.stdscr.addstr(h-2, 1, footer)
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key in [ord('n'), ord('N')]:
                if current_page < total_pages - 1:
                    current_page += 1
            elif key in [ord('p'), ord('P')]:
                if current_page > 0:
                    current_page -= 1
            elif key in [ord('q'), ord('Q')]:
                break

    def wyswietl_podsumowanie(self, saldo: float) -> None:
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, f"Aktualne saldo: {saldo:.2f} zł")
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_indeks_transakcji(self) -> int:
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Podaj numer transakcji: ")
        indeks_input = self.stdscr.getstr(1, 25, 5).decode('utf-8').strip()
        curses.noecho()
        try:
            indeks = int(indeks_input)
            return indeks
        except ValueError:
            self.wyswietl_komunikat("Nieprawidłowy format numeru.")
            return -1

    def wyswietl_komunikat(self, komunikat: str) -> None:
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, komunikat)
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_limit(self) -> Tuple[Optional[str], float]:
        curses.echo()
        self.stdscr.clear()
        try:
            self.stdscr.addstr(1, 1, "Podaj kategorię: ")
            kategoria = self.stdscr.getstr(1, 20, 20).decode('utf-8').strip()
            if not kategoria:
                raise ValueError("Kategoria nie może być pusta.")
            self.stdscr.addstr(2, 1, "Podaj limit miesięczny: ")
            limit_input = self.stdscr.getstr(2, 25, 20).decode('utf-8').strip()
            limit = float(limit_input)
            if limit <= 0:
                raise ValueError("Limit musi być większy od zera.")
            return kategoria, limit
        except ValueError as e:
            self.wyswietl_komunikat(f"Błąd: {e}")
            return None, 0.0
        finally:
            curses.noecho()

    def potwierdz_eksport(self) -> None:
        self.wyswietl_komunikat("Transakcje zostały wyeksportowane do pliku 'transakcje.csv'.")

    def potwierdz_import(self) -> None:
        self.wyswietl_komunikat("Transakcje zostały zaimportowane z pliku 'transakcje.csv'.")

    def potwierdz_ustawienie_limitu(self, kategoria: str, limit: float) -> None:
        self.wyswietl_komunikat(f"Ustawiono limit {limit:.2f} zł dla kategorii '{kategoria}'.")

    def wyswietl_raport(self, raport: Dict[str, float]) -> None:
        self.stdscr.clear()
        if not raport:
            self.stdscr.addstr(1, 1, "Brak wydatków do wyświetlenia.")
        else:
            self.stdscr.addstr(0, 1, "Raport wydatków według kategorii:")
            row = 1
            for kategoria, suma in raport.items():
                self.stdscr.addstr(row, 1, f"{kategoria}: {suma:.2f} zł")
                row += 1
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_zakres_dat(self) -> Tuple[Optional[str], Optional[str]]:
        curses.echo()
        self.stdscr.clear()
        try:
            self.stdscr.addstr(1, 1, "Podaj datę początkową (YYYY-MM-DD): ")
            start_date = self.stdscr.getstr(1, 40, 10).decode('utf-8').strip()
            datetime.strptime(start_date, '%Y-%m-%d')  # Walidacja
            self.stdscr.addstr(2, 1, "Podaj datę końcową (YYYY-MM-DD): ")
            end_date = self.stdscr.getstr(2, 40, 10).decode('utf-8').strip()
            datetime.strptime(end_date, '%Y-%m-%d')  # Walidacja
            return start_date, end_date
        except ValueError:
            self.wyswietl_komunikat("Nieprawidłowy format daty.")
            return None, None
        finally:
            curses.noecho()

    def wyswietl_wykresy(self, raport: Dict[str, float]) -> None:
        self.stdscr.clear()
        if not raport:
            self.stdscr.addstr(1, 1, "Brak danych do wyświetlenia.")
        else:
            total = sum(raport.values())
            self.stdscr.addstr(0, 1, "Udział kategorii w wydatkach:")
            row = 1
            for kategoria, suma in raport.items():
                procent = (suma / total) * 100 if total > 0 else 0
                wykres = '*' * int(procent // 2)  # Skala wykresu
                self.stdscr.addstr(row, 1, f"{kategoria}: {wykres} ({procent:.2f}%)")
                row += 1
        self.stdscr.refresh()
        self.stdscr.getch()

    def wyswietl_wyjscie(self) -> None:
        ascii_art = [
            "  ____  _    _ _____   _____ ______ _______   __  __          _   _          _____ ______ _____  ",
            " |  _ \\| |  | |  __ \\ / ____|  ____|__   __| |  \\/  |   /\\   | \\ | |   /\\   / ____|  ____|  __ \\ ",
            " | |_) | |  | | |  | | |  __| |__     | |    | \\  / |  /  \\  |  \\| |  /  \\ | |  __| |__  | |__) |",
            " |  _ <| |  | | |  | | | |_ |  __|    | |    | |\\/| | / /\\ \\ | . ` | / /\\ \\| | |_ |  __| |  _  / ",
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
                    self.stdscr.attron(curses.color_pair(2))  # Używamy innego koloru
                    self.stdscr.addstr(y, x, row)
                    self.stdscr.attroff(curses.color_pair(2))
                else:
                    self.stdscr.addstr(y, x, row)
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(menu) - 1:
                self.current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return self.current_row == 0  # 'Tak' to indeks 0
