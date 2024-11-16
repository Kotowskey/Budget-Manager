# curses_view.py
import curses
from datetime import datetime

class BudzetCursesView:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.current_row = 0

    def wyswietl_menu(self):
        self.stdscr.clear()
        menu = [
            'Dodaj transakcję',
            'Edytuj transakcję',
            'Usuń transakcję',
            'Wyświetl transakcje',
            'Wyświetl podsumowanie',
            'Eksportuj transakcje do CSV',
            'Filtruj transakcje według daty',
            'Ustaw limit budżetowy',
            'Importuj transakcje z CSV',
            'Generuj raport wydatków',
            'Wyjście'
        ]
        self.wyswietl_menu_opcje(menu)
        self.stdscr.refresh()

    def wyswietl_menu_opcje(self, menu):
        h, w = self.stdscr.getmaxyx()
        for idx, row in enumerate(menu):
            x = w//2 - len(row)//2
            y = h//2 - len(menu)//2 + idx
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)

    def pobierz_opcje(self):
        menu_length = 11  # Aktualna liczba opcji w menu
        while True:
            self.wyswietl_menu_opcje([
                'Dodaj transakcję',
                'Edytuj transakcję',
                'Usuń transakcję',
                'Wyświetl transakcje',
                'Wyświetl podsumowanie',
                'Eksportuj transakcje do CSV',
                'Filtruj transakcje według daty',
                'Ustaw limit budżetowy',
                'Importuj transakcje z CSV',
                'Generuj raport wydatków',
                'Wyjście'
            ])
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return str(self.current_row + 1)
            self.stdscr.refresh()

    def pobierz_dane_transakcji(self, edycja=False):
        curses.echo()
        self.stdscr.clear()
        start_row = 1
        if not edycja:
            self.stdscr.addstr(start_row, 1, "Typ (przychód/wydatek): ")
            typ = self.stdscr.getstr(start_row, 25, 20).decode('utf-8')
            start_row += 1
        else:
            typ = None  # Typ nie jest edytowany
        self.stdscr.addstr(start_row, 1, "Kwota: ")
        kwota_input = self.stdscr.getstr(start_row, 25, 20).decode('utf-8')
        try:
            kwota = float(kwota_input)
        except ValueError:
            kwota = 0.0
        start_row += 1
        self.stdscr.addstr(start_row, 1, "Kategoria: ")
        kategoria = self.stdscr.getstr(start_row, 25, 20).decode('utf-8')
        start_row += 1
        self.stdscr.addstr(start_row, 1, "Opis (opcjonalnie): ")
        opis = self.stdscr.getstr(start_row, 25, 50).decode('utf-8')
        start_row += 1
        self.stdscr.addstr(start_row, 1, "Data (YYYY-MM-DD) [opcjonalnie]: ")
        data_input = self.stdscr.getstr(start_row, 35, 10).decode('utf-8')
        data = data_input if data_input else datetime.now().strftime('%Y-%m-%d')
        curses.noecho()

        transakcja = {
            'kwota': kwota,
            'kategoria': kategoria,
            'typ': typ if typ else 'przychód',  # Domyślnie 'przychód' jeśli edycja
            'opis': opis,
            'data': data
        }
        return transakcja

    def wyswietl_transakcje(self, transakcje):
        self.stdscr.clear()
        if not transakcje:
            self.stdscr.addstr(1, 1, "Brak transakcji.")
            self.stdscr.refresh()
            self.stdscr.getch()
            return
        header = "Nr | Data       | Typ      | Kwota    | Kategoria     | Opis"
        self.stdscr.addstr(0, 1, header)
        self.stdscr.addstr(1, 1, "-" * len(header))
        for i, t in enumerate(transakcje):
            linia = f"{i}. | {t.data} | {t.typ.capitalize():8} | {t.kwota:9.2f} | {t.kategoria:13} | {t.opis}"
            try:
                self.stdscr.addstr(i+2, 1, linia)
            except curses.error:
                # Zapobiega błędom, gdy lista jest dłuższa niż wysokość ekranu
                break
        self.stdscr.refresh()
        self.stdscr.getch()

    def wyswietl_podsumowanie(self, saldo):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, f"Aktualne saldo: {saldo:.2f} zł")
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_indeks_transakcji(self):
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Podaj numer transakcji: ")
        indeks_input = self.stdscr.getstr(1, 25, 5).decode('utf-8')
        try:
            indeks = int(indeks_input)
        except ValueError:
            indeks = -1  # Nieprawidłowy indeks
        curses.noecho()
        return indeks

    def wyswietl_komunikat(self, komunikat):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, komunikat)
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_limit(self):
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Podaj kategorię: ")
        kategoria = self.stdscr.getstr(1, 20, 20).decode('utf-8')
        self.stdscr.addstr(2, 1, "Podaj limit miesięczny: ")
        limit_input = self.stdscr.getstr(2, 25, 20).decode('utf-8')
        try:
            limit = float(limit_input)
        except ValueError:
            limit = 0.0
        curses.noecho()
        return kategoria, limit

    def potwierdz_eksport(self):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Transakcje zostały wyeksportowane do pliku 'transakcje.csv'.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def potwierdz_import(self):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Transakcje zostały zaimportowane z pliku 'transakcje.csv'.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def potwierdz_ustawienie_limitu(self, kategoria, limit):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, f"Ustawiono limit {limit:.2f} zł dla kategorii '{kategoria}'.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def wyswietl_raport(self, raport):
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

    def zakoncz(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
