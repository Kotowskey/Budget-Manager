from controller import BudzetController
from textual.app import App
from textual.widgets import Footer, Header

class BudgetApp(App):
    pass

if __name__ == "__main__":
    kontroler = BudzetController()
    BudgetApp().run()
