from controller import BudzetController

def main():
    try:
        controller = BudzetController()
        controller.uruchom()
    except KeyboardInterrupt:
        print("\nProgram zakończony przez użytkownika.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
    finally:
        if hasattr(controller, 'view'):
            controller.view.zakoncz()

if __name__ == "__main__":
    main()