# main.py
from controller import BudzetController
from curses_view import BudzetCursesView
from gui_view import BudzetGUIView


def main():
    print("Wybierz tryb pracy:")
    print("1. curses (Konsola)")
    print("2. GUI (Okienkowy)")

    choice = input("Wybór (1/2): ").strip()
    if choice == "1":
        view = BudzetCursesView()
        controller = BudzetController(view)
        controller.uruchom()
    elif choice == "2":
        controller = BudzetController()  # Inicjalizacja bez widoku
        gui = BudzetGUIView(controller)
        controller.set_view(gui)  # Ustawienie widoku po utworzeniu GUI
        gui.run()
    else:
        print("Nieprawidłowy wybór. Zamykam program.")


if __name__ == "__main__":
    main()
