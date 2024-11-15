from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTreeWidget, QTreeWidgetItem, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
import sys
from database import Alumnos  # Asegúrate de importar correctamente la clase Alumnos desde su ubicación

class VentanaProfesor(QMainWindow):
    def __init__(self, ventana_login=None):
        super().__init__()
        self.ventana_login = ventana_login
        self.alumnos_db = Alumnos()  # Instancia de la base de datos Alumnos
        
        self.setWindowTitle("Gestión de Alumnos")
        self.setGeometry(100, 100, 920, 380)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout(self.central_widget)
        
        # Frame izquierdo para botones de acciones
        frame1 = QFrame(self)
        frame1.setFrameShape(QFrame.Shape.StyledPanel)
        layout.addWidget(frame1)
        frame1_layout = QVBoxLayout(frame1)

        self.btnNuevo = QPushButton("Nuevo", self)
        self.btnNuevo.clicked.connect(self.fNuevo)
        frame1_layout.addWidget(self.btnNuevo)

        self.btnModificar = QPushButton("Modificar", self)
        self.btnModificar.clicked.connect(self.fModificar)
        frame1_layout.addWidget(self.btnModificar)

        self.btnAtras = QPushButton("Atras", self)
        self.btnAtras.clicked.connect(self.fAtras)
        frame1_layout.addWidget(self.btnAtras)

        # Frame central para los campos de entrada
        frame2 = QFrame(self)
        frame2.setFrameShape(QFrame.Shape.StyledPanel)
        layout.addWidget(frame2)
        frame2_layout = QVBoxLayout(frame2)

        self.nombre = QLineEdit(self)
        self.apellido = QLineEdit(self)
        self.nota = QLineEdit(self)

        frame2_layout.addWidget(QLabel("Nombre:", self))
        frame2_layout.addWidget(self.nombre)
        frame2_layout.addWidget(QLabel("Apellido:", self))
        frame2_layout.addWidget(self.apellido)
        frame2_layout.addWidget(QLabel("Nota:", self))
        frame2_layout.addWidget(self.nota)

        # Layout para el campo de búsqueda
        buscar_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Buscar alumno...")

        search_button = QPushButton("Buscar", self)
        search_button.clicked.connect(self.fBuscar)
        buscar_layout.addWidget(self.search_input)
        buscar_layout.addWidget(search_button)

        frame2_layout.addLayout(buscar_layout)

        self.btnGuardar = QPushButton("Guardar", self)
        self.btnGuardar.clicked.connect(self.fGuardar)
        frame2_layout.addWidget(self.btnGuardar)

        self.btnCancelar = QPushButton("Cancelar", self)
        self.btnCancelar.clicked.connect(self.fCancelar)
        frame2_layout.addWidget(self.btnCancelar)

        # Frame derecho para la tabla de alumnos
        frame3 = QFrame(self)
        frame3.setFrameShape(QFrame.Shape.StyledPanel)
        layout.addWidget(frame3)
        frame3_layout = QVBoxLayout(frame3)

        self.grid = QTreeWidget(self)
        self.grid.setColumnCount(4)
        self.grid.setHeaderLabels(["ID", "Nombre", "Apellido", "Nota"])
        frame3_layout.addWidget(self.grid)

        self.cargar_alumnos()  # Cargar los alumnos al iniciar

    def fNuevo(self):
        """Limpia los campos para crear un nuevo alumno"""
        self.limpiarCajas()
        self.habilitarCajas(True)

    def fModificar(self):
        """Carga los datos seleccionados en los campos para su modificación"""
        item = self.grid.currentItem()
        if item:
            self.nombre.setText(item.text(1))
            self.apellido.setText(item.text(2))
            self.nota.setText(item.text(3))
            self.habilitarCajas(True)

    def fGuardar(self):
        """Guarda un nuevo alumno o modifica uno existente en la base de datos"""
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        nota_text = self.nota.text()

        if not nombre or not apellido or not nota_text:
            QMessageBox.warning(self, "Error", "Por favor completa todos los campos.")
            return

        try:
            nota = float(nota_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "La nota debe ser un número.")
            return

        if self.grid.currentItem():
            # Modificar alumno existente
            id_alumno = int(self.grid.currentItem().text(0))  # Obtener el ID del alumno seleccionado
            resultado = self.alumnos_db.modifica_alumno(id_alumno, nombre, apellido, nota)
            if resultado:
                QMessageBox.information(self, "Modificación", "Alumno modificado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo modificar el alumno.")
        else:
            # Insertar un nuevo alumno
            resultado = self.alumnos_db.inserta_alumno(nombre, apellido, nota)
            if resultado:
                QMessageBox.information(self, "Guardado", "Alumno guardado exitosamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar el alumno.")

        self.cargar_alumnos()  # Recargar la lista de alumnos
        self.limpiarCajas()

    def fBuscar(self): 
        """Busca un alumno en la base de datos y muestra los resultados"""
        texto_busqueda = self.search_input.text().strip()
        if not texto_busqueda:
            QMessageBox.warning(self, "Buscar", "Por favor, ingresa un nombre o apellido para buscar.")
            return

        resultados = self.alumnos_db.buscar_alumno(texto_busqueda)
        self.grid.clear()  # Limpiar resultados anteriores

        for id, nombre, apellido, nota in resultados:
            QTreeWidgetItem(self.grid, [str(id), nombre, apellido, str(nota)])

        if not resultados:
            QMessageBox.warning(self, "Buscar", "No se encontraron resultados para la búsqueda.")

    def fCancelar(self):
        """Cancela la acción actual y deshabilita los campos de entrada"""
        self.limpiarCajas()
        self.habilitarCajas(False)

    def fAtras(self):
        """Regresa a la ventana anterior"""
        self.close()
        if self.ventana_login:
            self.ventana_login.show()

    def cargar_alumnos(self):
        """Carga todos los alumnos en la tabla desde la base de datos"""
        self.grid.clear()
        alumnos = self.alumnos_db.consulta_alumno()

        for id, nombre, apellido, nota in alumnos:
            QTreeWidgetItem(self.grid, [str(id), nombre, apellido, str(nota)])

    def habilitarCajas(self, estado):
        """Habilita o deshabilita los campos de entrada"""
        self.nombre.setEnabled(estado)
        self.apellido.setEnabled(estado)
        self.nota.setEnabled(estado)

    def limpiarCajas(self):
        """Limpia los campos de entrada"""
        self.nombre.clear()
        self.apellido.clear()
        self.nota.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaProfesor()
    ventana.show()
    sys.exit(app.exec())
