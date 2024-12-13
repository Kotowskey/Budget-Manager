import curses
from datetime import datetime
from typing import Optional, Tuple, Dict

ESC = 27  # Stała dla klawisza ESC

class BudzetCursesView:
    def __init__(self):
        self.controller = None  # Będziemy ustawiać w momencie uruchomienia trybu curses
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.current_row = 0

    def run(self):
        # Główna pętla curses
        self.wyswietl_welcome_screen()
        # Przykładowo logowanie „na sztywno”
        self.controller.model.zaloguj("admin","admin")
        # Po zalogowaniu przechodzimy do menu
        self.glowna_petla()

    def glowna_petla(self):
        while True:
            opcja = self.pobierz_opcje_glownego_menu()
            if opcja is None:
                # ESC - wyjście
                self.wyswietl_wyjscie()
                self.zakoncz()
                break
            elif opcja == '5':
                # Wyjście
                self.wyswietl_wyjscie()
                self.zakoncz()
                break
            else:
                # Obsługa innych opcji pominięta dla uproszczenia
                pass

    # Usunięto kod przełączający na GUI

    def wyswietl_welcome_screen(self) -> None:
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
            key = self.stdscr.getch()
            if key in [10, 13, curses.KEY_ENTER]:
                break
            elif key == ESC:
                self.wyswietl_wyjscie()
                self.zakoncz()
                exit()

    def wyswietl_glowne_menu_kategorii(self) -> None:
        self.stdscr.clear()
        menu = [
            'Transakcje',
            'Podsumowania',
            'Limity',
            'Importowanie i eksportowanie',
            'Wyjście'
        ]
        self.wyswietl_menu_opcje(menu)
        self.wyswietl_footer()
        self.stdscr.refresh()

    def pobierz_opcje_glownego_menu(self) -> Optional[str]:
        menu_length = 5
        while True:
            self.wyswietl_glowne_menu_kategorii()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < menu_length - 1:
                self.current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                opcja = str(self.current_row + 1)
                self.current_row = 0
                return opcja
            elif key == ESC:
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

    def wyswietl_footer(self) -> None:
        h, w = self.stdscr.getmaxyx()
        footer_text = "BUDGET MANAGER"
        try:
            self.stdscr.addstr(h - 1, max((w // 2) - (len(footer_text) // 2), 0), footer_text, curses.A_DIM)
        except curses.error:
            pass

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
