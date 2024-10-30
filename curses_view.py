import curses

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
        menu = ['Dodaj transakcję', 'Edytuj transakcję', 'Usuń transakcję', 'Wyświetl transakcje', 'Wyświetl podsumowanie', 'Wyjście']
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
        menu = ['Dodaj transakcję', 'Edytuj transakcję', 'Usuń transakcję', 'Wyświetl transakcje', 'Wyświetl podsumowanie', 'Wyjście']
        while True:
            self.wyswietl_menu_opcje(menu)
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(menu) - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return str(self.current_row + 1)
            self.stdscr.refresh()

    def pobierz_dane_transakcji(self):
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Typ (przychód/wydatek): ")
        typ = self.stdscr.getstr(1, 25, 20).decode('utf-8')
        self.stdscr.addstr(2, 1, "Kwota: ")
        kwota = float(self.stdscr.getstr(2, 25, 20).decode('utf-8'))
        self.stdscr.addstr(3, 1, "Kategoria: ")
        kategoria = self.stdscr.getstr(3, 25, 20).decode('utf-8')
        self.stdscr.addstr(4, 1, "Opis (opcjonalnie): ")
        opis = self.stdscr.getstr(4, 25, 50).decode('utf-8')
        curses.noecho()
        return {'kwota': kwota, 'kategoria': kategoria, 'typ': typ, 'opis': opis}

    def wyswietl_transakcje(self, transakcje):
        self.stdscr.clear()
        if not transakcje:
            self.stdscr.addstr(1, 1, "Brak transakcji.")
            self.stdscr.refresh()
            self.stdscr.getch()
            return
        for i, t in enumerate(transakcje):
            self.stdscr.addstr(i+1, 1, f"{i}. {t.typ.capitalize()} | Kwota: {t.kwota} | Kategoria: {t.kategoria} | Opis: {t.opis}")
        self.stdscr.refresh()
        self.stdscr.getch()

    def wyswietl_podsumowanie(self, saldo):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, f"Aktualne saldo: {saldo} zł")
        self.stdscr.refresh()
        self.stdscr.getch()

    def pobierz_indeks_transakcji(self):
        curses.echo()
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "Podaj numer transakcji: ")
        indeks = int(self.stdscr.getstr(1, 25, 5).decode('utf-8'))
        curses.noecho()
        return indeks

    def wyswietl_komunikat(self, komunikat):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, komunikat)
        self.stdscr.refresh()
        self.stdscr.getch()

    def zakoncz(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
