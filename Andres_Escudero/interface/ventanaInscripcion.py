from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QDateEdit, QPushButton, QMessageBox
from database.db_nueva import Alumnos, Inscripciones  
from PyQt6.QtCore import QFile,QTextStream
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

class VentanaInscripcion(QDialog):
    def __init__(self, materias, alumnos_id, db):
        super().__init__()
        self.alumno_id = alumnos_id
        self.materias = materias
        self.db = db
        self.setObjectName("ventanaInscripcion") 
        self.init_ui()
        self.resize(400, 200)
        css_file = QFile(os.path.join(root_dir, "css", "ventanaInscripcion_styles.css"))
        if css_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(css_file)
            self.setStyleSheet(stream.readAll())
            css_file.close()

    def init_ui(self):
        self.setWindowTitle("Inscripción a Materias")
        layout = QVBoxLayout(self)

       
        self.combo_materias = QComboBox()
        self.combo_materias.setObjectName("comboMaterias")  
        for materia in self.materias:
            self.combo_materias.addItem(materia[1], materia[0])  

        layout.addWidget(self.combo_materias)

       
        self.fecha_inscripcion = QDateEdit()
        self.fecha_inscripcion.setObjectName("fechaInscripcion")  
        self.fecha_inscripcion.setDisplayFormat("yyyy-MM-dd")
        self.fecha_inscripcion.setCalendarPopup(True)
        layout.addWidget(self.fecha_inscripcion)

   
        btn_inscribir = QPushButton("Inscribirse")
        btn_inscribir.setObjectName("btnInscribir")  
        btn_inscribir.clicked.connect(self.inscribirse)
        layout.addWidget(btn_inscribir)

    def inscribirse(self):
        id_materia = self.combo_materias.currentData()
        fecha = self.fecha_inscripcion.date().toString("yyyy-MM-dd")
        inscripciones = Inscripciones(self.db)  
        resultado = inscripciones.inscribir_alumno(self.alumno_id, id_materia, fecha)
        if resultado:
            QMessageBox.information(self, "Inscripción Exitosa", "Te has inscrito en la materia correctamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Error en la inscripción.")
    