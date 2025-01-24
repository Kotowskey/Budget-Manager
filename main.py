from controller import BudzetController
from gui import BudzetGUIView
from view import BudzetCursesView
from model import BudzetModel
from budzet_service import BudzetService

def main():
    try:
        selection = input("Wybierz interfejs (1 - TUI, 2 - GUI): ")
        if selection == "1":
            controller = BudzetController()
            controller.uruchom()
        elif selection == "2":
            controller = BudzetController()
            view = BudzetGUIView(controller)
            view.run()
        else:
            print("Nieprawidłowy wybór. Uruchamiam TUI.")
            controller = BudzetController()
            controller.uruchom()
            
    except KeyboardInterrupt:
        print("\nProgram zakończony przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
    finally:
        if 'controller' in locals() and hasattr(controller, 'view') and selection == "1":
            controller.view.zakoncz()

if __name__ == "__main__":
    main()