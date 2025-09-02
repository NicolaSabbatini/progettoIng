import os
import json
import schedule
import time
from datetime import datetime

DATA_DIR = "data"            
BACKUP_FILE = "backUp.json" 

class GestoreSistema:
     
    def __init__(self):
        # Qui potresti salvare variabili di configurazione se servono
        self.data_dir = DATA_DIR
        self.backup_file = BACKUP_FILE

    def create_backup(self):
        backup_path = os.path.join(self.data_dir, self.backup_file)

        # Se il file esiste già, carichiamo i backup precedenti
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

        # Creiamo un nuovo snapshot
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

        # Aggiungiamo lo snapshot alla lista dei backup
        all_backups.append(snapshot)

        # Riscriviamo il file con tutti i backup
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(all_backups, f, indent=4, ensure_ascii=False)

        print(f"✅ Nuovo backup aggiunto in {backup_path}")

    def doBackUp(self):
        schedule.every().day.at("00:00").do(self.create_backup)
        print("⏳ Backup automatico pianificato ogni giorno alle 00:00")
        while True:
            schedule.run_pending()
            time.sleep(30)
