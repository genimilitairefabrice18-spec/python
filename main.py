import time
import os
import webbrowser
from threading import Timer
from app import app

def ouvrir_fenetre():
    """Ouvre l'application dans une fenêtre isolée."""
    url = "http://127.0.0.1:8050"
    
    browser_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]

    for path in browser_paths:
        if os.path.exists(path):
            os.system(f'"{path}" --app={url}')
            return

    webbrowser.open(url)

if __name__ == "__main__":
    print("🚀 Lancement de l'application...")
    
    # Programme l'ouverture de la fenêtre dans 1.5 seconde
    Timer(1.5, ouvrir_fenetre).start()
    
    # Lance Flask directement dans le processus principal
    app.run(host="127.0.0.1", port=8050, debug=False)