import threading
import os
import time
import urllib.request
import webbrowser
from app import app

def start_flask():
    """Lance le serveur Flask en arrière-plan."""
    app.run(port=8000, debug=False, use_reloader=False)

def attendre_flask(url, max_attente=10):
    """Attend que Flask réponde avant d'ouvrir la fenêtre."""
    debut = time.time()
    while time.time() - debut < max_attente:
        try:
            # Essaie de contacter le serveur Flask
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False

def open_desktop_window():
    """Ouvre l'application dans une fenêtre dédiée dès que Flask est prêt."""
    url = "http://127.0.0.1:8000"
    
    print("⏳ Attente du démarrage de Flask...")
    if not attendre_flask(url):
        print("❌ Flask a mis trop de temps à démarrer.")
        return

    print("🚀 Flask est prêt ! Ouverture de l'application Desktop...")
    
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

    # Lancement de la fenêtre Desktop
    open_desktop_window()