# controllers/GestoreSistema.py
import os
import json
import schedule
from datetime import datetime
from PyQt5.QtCore import QTimer

DATA_DIR = "data"            
BACKUP_FILE = "backUp.json" 

class GestoreSistema:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.backup_file = BACKUP_FILE

    def create_backup(self):
        backup_path = os.path.join(self.data_dir, self.backup_file)

        if os.path.exists(backup_path):
            try:
                with open(backup_path, "r", encoding="utf-8") as f:
                    all_backups = json.load(f)
                if not isinstance(all_backups, list):
                    all_backups = []
            except Exception:
                all_backups = []
        else:
            all_backups = []

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "files": {}
        }

        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json") and filename != self.backup_file:
                file_path = os.path.join(self.data_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        snapshot["files"][filename] = json.load(f)
                except Exception as e:
                    print(f"❌ Errore nel leggere {filename}: {e}")

        all_backups.append(snapshot)

        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(all_backups, f, indent=4, ensure_ascii=False)

        print(f"✅ Nuovo backup aggiunto in {backup_path}")

    def start_scheduled_backup(self, qt_app):
        """Avvia il backup giornaliero senza bloccare PyQt"""
        schedule.every().day.at("00:00").do(self.create_backup)
        print("⏳ Backup automatico pianificato ogni giorno alle 00:00")

        # Usa QTimer per eseguire schedule.run_pending ogni 30 secondi
        self.timer = QTimer()
        self.timer.timeout.connect(schedule.run_pending)
        self.timer.start(30000)  # 30 secondi
