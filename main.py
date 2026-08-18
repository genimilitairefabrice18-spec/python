import threading
import os
import time
import webbrowser
from app import app

def start_flask():
    """Lance le serveur Flask en arrière-plan."""
    app.run(port=8000, debug=False, use_reloader=False)

def open_desktop_window():
    """Ouvre l'application dans une fenêtre dédiée."""
    time.sleep(3)  # Passe de 1 à 3 secondes pour laisser le temps à Flask
    url = "http://127.0.0.1:8000"
    ...
    
    # Liste des chemins possibles pour les navigateurs en mode --app
    browser_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]

    # Cherche le premier navigateur disponible et l'ouvre en mode App
    for path in browser_paths:
        if os.path.exists(path):
            os.system(f'"{path}" --app={url}')
            return

    # Si aucun navigateur compatible n'est trouvé, ouvre le navigateur par défaut
    webbrowser.open(url)

if __name__ == "__main__":
    # Démarrage de Flask dans un thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    print("🚀 Lancement de FabSchool Desktop...")
    
    # Lancement de la fenêtre Desktop
    open_desktop_window()