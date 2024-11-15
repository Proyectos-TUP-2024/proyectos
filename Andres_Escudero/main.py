from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
import sys
import os

# Ruta del directorio raíz del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from database.db_nueva import Database  
from interface.login import VentanaLogin  

def main():
    
    db = Database()  
    app = QApplication(sys.argv)
    css_file = QFile(os.path.join(root_dir, "css", "styles.css"))
    if css_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(css_file)
        app.setStyleSheet(stream.readAll())
        css_file.close()
        
    ventana_login = VentanaLogin(db)  
    ventana_login.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
