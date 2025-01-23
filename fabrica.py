from abc import ABC, abstractmethod
from typing import Dict
from curses_view import BudzetCursesView

class Wykres(ABC):
    @abstractmethod
    def rysuj(self, raport: Dict[str, float], view: BudzetCursesView) -> None:
        pass

class WykresWydatkow(Wykres):
    def rysuj(self, raport: Dict[str, float], view: BudzetCursesView) -> None:
        view.stdscr.clear()
        if not raport:
            view.stdscr.addstr(1, 1, "Brak wydatków do wyświetlenia.")
        else:
            total = sum(raport.values())
            view.stdscr.addstr(0, 1, "Raport wydatków według kategorii:")
            row = 1
            for kategoria, suma in raport.items():
                procent = (suma / total) * 100 if total > 0 else 0
                wykres = '*' * int(procent // 2)
                view.stdscr.addstr(row, 1, f"{kategoria}: {wykres} ({procent:.2f}%)")
                row += 1
        view.wyswietl_footer()
        view.stdscr.refresh()
        view.stdscr.getch()

class WykresPrzychodow(Wykres):
    def rysuj(self, raport: Dict[str, float], view: BudzetCursesView) -> None:
        view.stdscr.clear()
        if not raport:
            view.stdscr.addstr(1, 1, "Brak przychodów do wyświetlenia.")
        else:
            total = sum(raport.values())
            view.stdscr.addstr(0, 1, "Raport przychodów według kategorii:")
            row = 1
            for kategoria, suma in raport.items():
                procent = (suma / total) * 100 if total > 0 else 0
                wykres = '*' * int(procent // 2)
                view.stdscr.addstr(row, 1, f"{kategoria}: {wykres} ({procent:.2f}%)")
                row += 1
        view.wyswietl_footer()
        view.stdscr.refresh()
        view.stdscr.getch()

class FabrykaWykresow:
    @staticmethod
    def utworz_wykres(typ: str) -> Wykres:
        if typ == 'wydatki':
            return WykresWydatkow()
        elif typ == 'przychody':
            return WykresPrzychodow()
        else:
            raise ValueError("Nieznany typ wykresu")
