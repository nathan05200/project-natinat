import webview
from pathlib import Path

def hello_from_python():
    """Fonction Python exposée à JavaScript."""
    print("La fonction Python a été appelée par JavaScript!")
    return "Bonjour de Python !"

def call_js(window):
    """Appelle une fonction JavaScript une fois la fenêtre chargée."""
    # window.evaluate_js exécute le script JavaScript ; protège si la fonction JS n'existe pas
    try:
        window.evaluate_js("if (window.updateMessage) updateMessage('Message mis à jour par Python !');")
    except Exception:
        pass

def main():
    base = Path(__file__).parent
    template_path = base / "template.html"
    css_path = base / "style.css"

    # Lire template + CSS externes
    html_text = template_path.read_text(encoding="utf-8")
    css_text = css_path.read_text(encoding="utf-8")

    # Injecter le CSS dans le template (garde HTML et CSS séparés sur disque)
    html_content = html_text.replace("<!-- INJECT_CSS -->", f"<style>\n{css_text}\n</style>")

    # Créer la fenêtre webview avec le HTML final
    window = webview.create_window(
        "Guardia — Inscription",
        html=html_content
    )

    # Exposer la fonction Python à JavaScript
    window.expose(hello_from_python)

    # Démarrer l'app et appeler call_js quand la fenêtre est prête
    webview.start(call_js, window)

if __name__ == "__main__":
    main()