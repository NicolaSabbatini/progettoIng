import sys
from PyQt5.QtWidgets import QApplication

from controllers.GestoreUtenti import GestoreUtenti
from controllers.GestoreSistema import GestoreSistema

from views.LoginView import LoginView

def main():
    app = QApplication(sys.argv)
    
    # Inizializza controller e view
    controller = GestoreUtenti()
    login_view = LoginView(controller)
    controller.login_view = login_view
    
    # Mostra la finestra di login
    login_view.show()
    
    # Avvia backup automatico
    gestore = GestoreSistema()
    gestore.start_scheduled_backup(app)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
