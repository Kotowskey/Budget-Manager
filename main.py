import argparse
from controller import BudzetController
from gui_view import BudzetGUIView
from curses_view import BudzetCursesView

def main():
    parser = argparse.ArgumentParser(description="Aplikacja Budżetowa")
    parser.add_argument("--interface", choices=["gui", "tui"], default="tui", 
                        help="Wybierz interfejs: 'gui' (graficzny) lub 'tui' (terminalowy)")
    args = parser.parse_args()

    controller = BudzetController()
    view = BudzetGUIView(controller) if args.interface == "gui" else BudzetCursesView()
    controller.view = view
    
    view.run() if args.interface == "gui" else controller.uruchom()

if __name__ == "__main__":
    main()