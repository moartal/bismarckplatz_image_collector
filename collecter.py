import cv2
import time
import os
from datetime import datetime

# Stream-URL
stream_url = "https://stream.bismarckplatz.r-kom.de/"

# Basisverzeichnis für die Bilder
base_directory = "/mnt/undertaker/image_data"

# Intervall zwischen den Bildern (in Sekunden)
interval = 20 * 60  # 20 Minuten


def get_daily_directory(base_directory):
    """
    Gibt das Verzeichnis für den aktuellen Tag zurück und erstellt es, falls es nicht existiert.
    """
    # Aktuelles Datum im Format DD-MM-YYYY
    today = datetime.now().strftime("%d-%m-%Y")
    daily_directory = os.path.join(base_directory, today)
    
    # Verzeichnis erstellen, falls es nicht existiert
    os.makedirs(daily_directory, exist_ok=True)
    
    return daily_directory


def capture_image(stream_url, output_directory):
    """
    Nimmt ein Bild vom Stream auf und speichert es im angegebenen Verzeichnis.
    """
    try:
        # Stream öffnen
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            print("Fehler: Stream konnte nicht geöffnet werden.")
            return
        
        # Einzelnes Frame lesen
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%H-%M-%S")
            filename = os.path.join(output_directory, f"bismarckplatz_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Bild gespeichert: {filename}")
        else:
            print("Fehler: Kein Bild vom Stream erhalten.")
        
        cap.release()
    except Exception as e:
        print(f"Fehler beim Aufnehmen des Bildes: {e}")


# Hauptschleife für das Speichern der Bilder
try:
    while True:
        # Holen des Tagesverzeichnisses
        daily_directory = get_daily_directory(base_directory)
        
        # Bild aufnehmen und speichern
        capture_image(stream_url, daily_directory)
        
        # Warten bis zum nächsten Intervall
        time.sleep(interval)
except KeyboardInterrupt:
    print("Programm beendet.")
