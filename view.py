# view.py
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich import box

class BudzetView:
    def __init__(self):
        self.console = Console()

    def wyswietl_menu(self):
        menu = Table(title="📊 Budżet Aplikacja", box=box.ROUNDED, expand=True)
        menu.add_column("Opcja", style="cyan", justify="center")
        menu.add_column("Opis", style="magenta")
        menu.add_row("1", "Dodaj transakcję")
        menu.add_row("2", "Edytuj transakcję")
        menu.add_row("3", "Usuń transakcję")
        menu.add_row("4", "Wyświetl transakcje")
        menu.add_row("5", "Wyświetl podsumowanie")
        menu.add_row("6", "Eksportuj transakcje do CSV")
        menu.add_row("7", "Filtruj transakcje według daty")
        menu.add_row("8", "Ustaw limit budżetowy")
        menu.add_row("9", "Wyjście")
        self.console.print(menu)

    def pobierz_opcje(self):
        opcja = Prompt.ask("Wybierz opcję", choices=[str(i) for i in range(1, 10)], default="9")
        return opcja

    def pobierz_dane_transakcji(self, edycja=False):
        typ = "przychód"
        if not edycja:
            typ = Prompt.ask("Typ", choices=["przychód", "wydatek"], default="przychód")
        kwota = Prompt.ask("Kwota", default="0.00", validate=lambda x: self._is_float(x))
        kwota = float(kwota)
        kategoria = Prompt.ask("Kategoria")
        opis = Prompt.ask("Opis (opcjonalnie)", default="")
        data = Prompt.ask("Data (YYYY-MM-DD) [opcjonalnie]", default="")
        return {
            'kwota': kwota,
            'kategoria': kategoria,
            'typ': typ,
            'opis': opis,
            'data': data if data else None
        }

    def wyswietl_transakcje(self, transakcje):
        if not transakcje:
            self.console.print("[yellow]Brak transakcji do wyświetlenia.[/yellow]")
            return
        table = Table(title="💰 Transakcje", box=box.MINIMAL_DOUBLE_HEAD, expand=True)
        table.add_column("Nr", style="cyan", justify="center")
        table.add_column("Data", style="green")
        table.add_column("Typ", style="magenta")
        table.add_column("Kwota", style="yellow", justify="right")
        table.add_column("Kategoria", style="blue")
        table.add_column("Opis", style="white")
        for i, t in enumerate(transakcje):
            typ_colored = "[green]Przychód[/green]" if t.typ.lower() == 'przychód' else "[red]Wydatek[/red]"
            table.add_row(
                str(i),
                t.data,
                typ_colored,
                f"{t.kwota:.2f} zł",
                t.kategoria,
                t.opis
            )
        self.console.print(table)

    def wyswietl_podsumowanie(self, saldo):
        panel = Panel.fit(
            Text(f"Aktualne saldo: [bold]{saldo:.2f} zł[/bold]", style="bold cyan"),
            title="📈 Podsumowanie",
            border_style="green"
        )
        self.console.print(panel)

    def pobierz_indeks_transakcji(self):
        indeks = IntPrompt.ask("Podaj numer transakcji", default=0, show_default=False)
        return indeks

    def wyswietl_komunikat(self, komunikat, success=True):
        color = "green" if success else "red"
        panel = Panel.fit(
            Text(komunikat, style=color),
            border_style=color
        )
        self.console.print(panel)

    def pobierz_limit(self):
        kategoria = Prompt.ask("Podaj kategorię")
        limit = Prompt.ask("Podaj limit miesięczny", default="0.00", validate=lambda x: self._is_float(x))
        return kategoria, float(limit)

    def potwierdz_eksport(self):
        self.wyswietl_komunikat("Transakcje zostały wyeksportowane do pliku 'transakcje.csv'.")

    def potwierdz_ustawienie_limitu(self, kategoria, limit):
        self.wyswietl_komunikat(f"Ustawiono limit {limit:.2f} zł dla kategorii '{kategoria}'.")
    
    def _is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
