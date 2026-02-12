from kivy.app import App
from threading import Thread
from plyer import browser
import time
from backend import app


def iniciar_flask():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


class RastreadorApp(App):
    def build(self):
        # Iniciar Flask en segundo plano
        Thread(target=iniciar_flask, daemon=True).start()

        # Esperar a que Flask levante
        time.sleep(2)

        # Abrir en el navegador del sistema
        browser.open("http://127.0.0.1:5000")

        # Kivy no necesita UI
        return None


if __name__ == "__main__":
    RastreadorApp().run()