import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QApplication, QLineEdit
)
from PyQt6.QtCore import Qt

class VentanaCalificaciones(QWidget):
    def __init__(self, alumnos):
        super().__init__()
        self.alumnos = alumnos
        self.setWindowTitle("Ingresar Calificaciones")
        self.setGeometry(200, 200, 600, 400)
        
        # Layout principal
        layout = QVBoxLayout()

        # Tabla para mostrar los alumnos y sus calificaciones
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "Apellido", "Calificación"])
        layout.addWidget(self.table_widget)

        # Cargar datos de alumnos
        self.load_alumnos()

        # Botón para guardar calificaciones
        self.btn_guardar = QPushButton("Guardar Calificaciones")
        self.btn_guardar.clicked.connect(self.guardar_calificaciones)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def load_alumnos(self):
        # Limpiar la tabla
        self.table_widget.setRowCount(0)
        
        # Agregar cada alumno y su calificación en la tabla
        for alumno in self.alumnos:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            
            # Agregar nombre y apellido
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(alumno['nombre']))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(alumno['apellido']))
            
            # Agregar campo de calificación editable
            nota_item = QTableWidgetItem(str(alumno['nota']) if alumno['nota'] is not None else "")
            nota_item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(row_position, 2, nota_item)

    def guardar_calificaciones(self):
        # Recorrer la tabla para obtener los datos actualizados
        for row in range(self.table_widget.rowCount()):
            nombre = self.table_widget.item(row, 0).text()
            apellido = self.table_widget.item(row, 1).text()
            calificacion_texto = self.table_widget.item(row, 2).text()
            try:
                calificacion = float(calificacion_texto) if calificacion_texto else None
            except ValueError:
                QMessageBox.warning(self, "Error", f"Calificación inválida para {nombre} {apellido}.")
                return

            # Aquí puedes actualizar la base de datos con el método correspondiente
            self.actualizar_calificacion(nombre, apellido, calificacion)
        
        QMessageBox.information(self, "Éxito", "Calificaciones guardadas exitosamente.")
        self.close()

    def actualizar_calificacion(self, nombre, apellido, calificacion):
        # Implementa la lógica para actualizar la calificación en la base de datos
        print(f"Guardando calificación para {nombre} {apellido}: {calificacion}")
        # Ejemplo:
        # alumno_id = self.alumnos.obtener_id_alumno(nombre)
        # self.alumnos.modifica_alumno(alumno_id, nombre, apellido, calificacion)
        

if __name__ == "__main__":
    # Inicializa la aplicación
    app = QApplication(sys.argv)

    # Datos de ejemplo de alumnos
    alumnos = [
        {"nombre": "Juan", "apellido": "Pérez", "nota": 8.5},
        {"nombre": "Ana", "apellido": "Gómez", "nota": 9.0},
        {"nombre": "Carlos", "apellido": "López", "nota": None},
    ]

    # Crear e iniciar la ventana de calificaciones
    ventana_calificaciones = VentanaCalificaciones(alumnos)
    ventana_calificaciones.show()

    sys.exit(app.exec())