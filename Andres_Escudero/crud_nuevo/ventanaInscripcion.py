from PyQt6.QtWidgets import (
    QMainWindow, QWidget,QComboBox, QDateEdit, QVBoxLayout, QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget
)
from PyQt6.QtCore import Qt

class VentanaInscripcion(QDialog):
    def __init__(self, materias, alumno_id):
        super().__init__()
        self.alumno_id = alumno_id
        self.materias = materias
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Inscripción a Materias")
        layout = QVBoxLayout(self)

        self.combo_materias = QComboBox()
        for materia in self.materias:
            self.combo_materias.addItem(materia[1], materia[0])  # Agrega ID como dato de fondo

        layout.addWidget(self.combo_materias)

        self.fecha_inscripcion = QDateEdit()
        layout.addWidget(self.fecha_inscripcion)

        btn_inscribir = QPushButton("Inscribirse")
        btn_inscribir.clicked.connect(self.inscribirse)
        layout.addWidget(btn_inscribir)

    def inscribirse(self):
        id_materia = self.combo_materias.currentData()
        fecha = self.fecha_inscripcion.date().toString("yyyy-MM-dd")
        resultado = Alumnos().inscribir_alumno(self.alumno_id, id_materia, fecha)
        if resultado:
            print("Inscripción exitosa")
        else:
            print("Error en la inscripción")


    def inscribirse(self):
        selected_items = self.lista_materias.selectedItems()
        if selected_items:
            materia = selected_items[0].text()
            # Aquí agregar la lógica para inscribir al alumno en la materia
            # Esto puede incluir una consulta a la base de datos
            QMessageBox.information(self, "Inscripción Exitosa", f"Te has inscrito en {materia}.")
            self.close()  # Cierra la ventana de inscripción
        else:
            QMessageBox.warning(self, "Error", "Por favor, selecciona una materia para inscribirte.")
