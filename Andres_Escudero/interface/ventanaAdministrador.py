import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QApplication, QLineEdit, QLabel
)

class VentanaAdmin(QMainWindow):
    def __init__(self, ventana_login=None):
        super().__init__()
        print("Inicialización de VentanaAdmin completa.")

        self.setWindowTitle("Administración de Alumnos y Profesores")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Layout para los botones de navegación en una sola fila
        button_layout = QHBoxLayout()

        # Botones para editar y eliminar
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_editar = QPushButton("Editar Datos")

        # Agregar botones al layout
        button_layout.addWidget(self.btn_editar)
        button_layout.addWidget(self.btn_eliminar)
        layout.addLayout(button_layout)
        
        # Tabla para mostrar datos
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # Configurar las columnas de la tabla
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "Apellido", "Rol", "Materia/Nota"])
        print("Preparando para cargar datos...")

        # Cargar datos de ejemplo al iniciar
        self.load_data()
        print("Datos cargados.")

        # Conectar los botones a sus funciones
        self.btn_editar.clicked.connect(self.edit_data)
        self.btn_eliminar.clicked.connect(self.delete_data)

    def load_data(self):
        print("Cargando datos de ejemplo...")

        # Datos de ejemplo en lugar de datos de la base de datos
        datos_ejemplo = [
            ("Juan", "Pérez", "Alumno", "Matemáticas"),
            ("Ana", "Gómez", "Profesor", "Ciencias"),
            ("Carlos", "López", "Alumno", "Historia"),
        ]

        # Llenar la tabla con los datos de ejemplo
        for nombre, apellido, rol, materia in datos_ejemplo:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(nombre))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(apellido))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(rol))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(materia))

    def edit_data(self):
        current_row = self.table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una fila para editar.")
            return
        
        # Obtén los datos de la fila seleccionada
        nombre = self.table_widget.item(current_row, 0).text()
        apellido = self.table_widget.item(current_row, 1).text()
        rol = self.table_widget.item(current_row, 2).text()
        materia = self.table_widget.item(current_row, 3).text()
        
        # Crear y mostrar la ventana de edición con los datos actuales
        self.ventana_editar = VentanaEditar(nombre, apellido, rol, materia)
        self.ventana_editar.show()

    def delete_data(self):
        current_row = self.table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una fila para eliminar.")
            return

        self.table_widget.removeRow(current_row)
        QMessageBox.information(self, "Éxito", "Datos eliminados exitosamente.")

class VentanaEditar(QWidget):
    def __init__(self, nombre, apellido, rol, materia):
        super().__init__()
        self.setWindowTitle("Editar Datos")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        # Campos de edición para cada atributo
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setText(nombre)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)

        self.apellido_input = QLineEdit(self)
        self.apellido_input.setText(apellido)
        layout.addWidget(QLabel("Apellido:"))
        layout.addWidget(self.apellido_input)

        self.rol_input = QLineEdit(self)
        self.rol_input.setText(rol)
        layout.addWidget(QLabel("Rol:"))
        layout.addWidget(self.rol_input)

        self.materia_input = QLineEdit(self)
        self.materia_input.setText(materia)
        layout.addWidget(QLabel("Materia/Nota:"))
        layout.addWidget(self.materia_input)

        # Botón para guardar los cambios
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_cambios(self):
        # Obtener valores actualizados
        nombre_actualizado = self.nombre_input.text()
        apellido_actualizado = self.apellido_input.text()
        rol_actualizado = self.rol_input.text()
        materia_actualizada = self.materia_input.text()

        # Aquí puedes añadir la lógica para actualizar los datos en la tabla principal o en la base de datos
        QMessageBox.information(self, "Guardado", "Cambios guardados exitosamente.")

        # Cierra la ventana de edición
        self.close()

if __name__ == "__main__":
    # Inicializa la aplicación
    app = QApplication(sys.argv)

    # Cargar el archivo CSS
    with open("css/ventanaAdmin_styles.css", "r") as file:
        app.setStyleSheet(file.read())

    ventana_admin = VentanaAdmin()
    ventana_admin.show()

    sys.exit(app.exec())
