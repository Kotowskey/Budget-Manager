import argparse
from controller import BudzetController
from gui_view import BudzetGUIView
from curses_view import BudzetCursesView

def main():
    # Obsługa argumentów wiersza poleceń
    parser = argparse.ArgumentParser(description="Aplikacja Budżetowa")
    parser.add_argument(
        "--interface",
        choices=["gui", "tui"],
        default="gui",
        help="Wybierz interfejs aplikacji: 'gui' dla interfejsu graficznego, 'tui' dla terminalowego (domyślnie: gui)"
    )
    args = parser.parse_args()

    # Inicjalizacja kontrolera i odpowiedniego widoku
    controller = BudzetController()
    if args.interface == "gui":
        controller.view = BudzetGUIView(controller)
        controller.view.run()
    elif args.interface == "tui":
        controller.view = BudzetCursesView()
        controller.uruchom()

if __name__ == "__main__":
    main()
