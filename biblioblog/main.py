from model.database import Database
from view.app import App

if __name__ == "__main__":
    Database.initialize()
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass