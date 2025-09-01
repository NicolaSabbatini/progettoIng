import sys
from PyQt5.QtWidgets import QApplication
from controllers.GestoreUtenti import GestoreUtenti
from views.login_view import LoginView

def main():
    app = QApplication(sys.argv)
    
    # Inizializza il controller e la view
    controller = GestoreUtenti()
    login_view = LoginView(controller)
    controller.login_view = login_view
    
    
    # Mostra la finestra di login
    login_view.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
