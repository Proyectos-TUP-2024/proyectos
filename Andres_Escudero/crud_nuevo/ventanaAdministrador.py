from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QMenu
)
import sqlite3
import sys

class VentanaAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administración de Alumnos y Profesores")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Layout para los botones de navegación en una sola fila
        button_layout = QHBoxLayout()

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_editar = QPushButton("Editar Datos")

        # Crear menú para agregar
        agregar_menu = QMenu(self)
        agregar_menu.addAction("Profesor", self.show_add_profesor_dialog)
        agregar_menu.addAction("Alumnos", self.show_add_alumno_dialog)
        agregar_menu.addAction("Materia", self.show_add_materia_dialog)

        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.setMenu(agregar_menu)

        button_layout.addWidget(self.btn_agregar)
        button_layout.addWidget(self.btn_editar)
        button_layout.addWidget(self.btn_eliminar)
        
        layout.addLayout(button_layout)

        # Tabla para mostrar datos
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        self.table_widget.setColumnCount(4)  # Ajusta esto según tus columnas
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "Apellido","rol","Materia"])

        self.load_data()  # Cargar datos al iniciar

        self.btn_editar.clicked.connect(self.edit_data)
        self.btn_eliminar.clicked.connect(self.delete_data)

    def load_data(self):
        self.table_widget.setRowCount(0)  # Limpiar tabla

        # Conexión a la base de datos
        conn = sqlite3.connect("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")
        cursor = conn.cursor()

        try:
            # Consulta para obtener alumnos con su rol
            cursor.execute("""
                SELECT u.nombre, u.apellido, u.rol 
                FROM alumnos a 
                JOIN usuarios u ON a.id = u.id
            """)
            alumnos = cursor.fetchall()

            # Consulta para obtener profesores con su materia
            cursor.execute("""
                SELECT p.nombre, p.apellido, m.nombre_materia 
                FROM profesor p 
                JOIN materia m ON p.id = m.id_profesor
                JOIN usuarios u ON p.id = u.id
            """)
            profesores = cursor.fetchall()

            # Inserta los alumnos en la tabla
            for nombre, apellido, rol in alumnos:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(nombre))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(apellido))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(rol))  # Añadir rol

            # Inserta los profesores en la tabla
            for nombre, apellido, materia in profesores:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(nombre))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(apellido))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(materia))  # Añadir materia
            
        except sqlite3.Error as e:
            print(f"Error al cargar datos: {e}")
            QMessageBox.warning(self, "Error", "Error al cargar los datos desde la base de datos.")

        finally:
            conn.close()
    def get_usuario_id(self, nombre, apellido):
        conn = sqlite3.connect("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM usuarios WHERE nombre = ? AND apellido = ?", (nombre, apellido))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error al obtener el ID del usuario: {e}")
            return None
        finally:
            conn.close()

    def show_add_profesor_dialog(self):
        self.add_dialog = AddProfesorDialog(self)
        self.add_dialog.show()

    def show_add_alumno_dialog(self):
        self.add_dialog = AddAlumnoDialog(self)
        self.add_dialog.show()

    def show_add_materia_dialog(self):
        self.add_dialog = AddMateriaDialog(self)
        self.add_dialog.show()

    def edit_data(self):
        current_row = self.table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una fila para editar.")
            return
        
        nombre = self.table_widget.item(current_row, 0).text()
        apellido = self.table_widget.item(current_row, 1).text()
        self.add_dialog = AddAlumnoDialog(self, nombre, apellido)
        self.add_dialog.show()

    def delete_data(self):
        current_row = self.table_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una fila para eliminar.")
            return

    # Obtener el nombre y apellido del usuario seleccionado
        nombre = self.table_widget.item(current_row, 0).text()
        apellido = self.table_widget.item(current_row, 1).text()

    # Aquí debes obtener el ID correspondiente desde la base de datos
    # Asumiendo que tienes un método que obtiene el ID por nombre y apellido
        usuario_id = self.get_usuario_id(nombre, apellido)  # Debes implementar este método

        if usuario_id is not None:
        # Conexión a la base de datos
            conn = sqlite3.connect("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")
            try:
                with conn:
                    # Ejecutar la consulta para eliminar el registro de la base de datos
                    conn.execute("DELETE FROM alumnos WHERE id = ?", (usuario_id,))
                    conn.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
                # Eliminar la fila de la tabla
                self.table_widget.removeRow(current_row)
                QMessageBox.information(self, "Éxito", "Datos eliminados exitosamente.")
            except sqlite3.Error as e:
                print(f"Error al eliminar datos: {e}")
                QMessageBox.warning(self, "Error", "No se pudo eliminar el dato de la base de datos.")
            finally:
                conn.close()
        else:
            QMessageBox.warning(self, "Advertencia", "No se encontró el usuario para eliminar.")

class AddAlumnoDialog(QWidget):
    def __init__(self, parent, nombre='', apellido=''):
        super().__init__(parent)
        self.setWindowTitle("Agregar Alumno")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nombre")
        self.name_input.setText(nombre)
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit(self)
        self.surname_input.setPlaceholderText("Apellido")
        self.surname_input.setText(apellido)
        layout.addWidget(self.surname_input)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_data(self):
        nombre = self.name_input.text()
        apellido = self.surname_input.text()
        if not nombre or not apellido:
            QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")
            return
        
        # Guardar en la base de datos
        conn = sqlite3.connect("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")
        cursor = conn.cursor()
        try:
            # Aquí deberías obtener el rol o establecerlo de manera adecuada
            rol = "alumno"  # Asumiendo un rol por defecto
            cursor.execute("INSERT INTO usuarios (nombre, apellido, rol) VALUES (?, ?, ?)", (nombre, apellido, rol))
            usuario_id = cursor.lastrowid  # Obtener el ID del usuario recién insertado
            cursor.execute("INSERT INTO alumnos (id, nombre, apellido) VALUES (?, ?, ?)", (usuario_id, nombre, apellido))
            QMessageBox.information(self, "Éxito", "Alumno guardado exitosamente.")
            self.parent().load_data()  # Recargar datos en la tabla
            self.close()
        except sqlite3.Error as e:
            print(f"Error al guardar el alumno: {e}")
            QMessageBox.warning(self, "Error", "No se pudo guardar el alumno.")
        finally:
            conn.close()
    def save_data(self):
        nombre = self.name_input.text()
        apellido = self.surname_input.text()
        if not nombre or not apellido:
            QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")
            return
        # Aquí deberías agregar la lógica para guardar en la base de datos
        QMessageBox.information(self, "Éxito", "Alumno guardado exitosamente.")
        self.close()
        self.parent().load_data()  # Recargar datos en la tabla

class AddProfesorDialog(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Agregar Profesor")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nombre")
        layout.addWidget(self.name_input)

        self.surname_input = QLineEdit(self)
        self.surname_input.setPlaceholderText("Apellido")
        layout.addWidget(self.surname_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Para ocultar la contraseña
        layout.addWidget(self.password_input)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_data(self):
        nombre = self.name_input.text()
        apellido = self.surname_input.text()
        password = self.password_input.text()  # Obtener la contraseña
        rol = "Profesor"  # Asignar el rol como 'Profesor'
        
        if not nombre or not apellido or not password:
            QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")
            return
        
        # Guardar en la base de datos
        conn = sqlite3.connect("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, apellido, rol, password) VALUES (?, ?, ?, ?)", (nombre, apellido, rol, password))
            usuario_id = cursor.lastrowid  # Obtener el ID del usuario recién insertado
            cursor.execute("INSERT INTO profesor (id, nombre, apellido) VALUES (?, ?, ?)", (usuario_id, nombre, apellido))
            QMessageBox.information(self, "Éxito", "Profesor guardado exitosamente.")
            self.parent().load_data()  # Recargar datos en la tabla
            self.close()
        except sqlite3.Error as e:
            print(f"Error al guardar el profesor: {e}")
            QMessageBox.warning(self, "Error", "No se pudo guardar el profesor.")
        finally:
            conn.close()
class AddMateriaDialog(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Agregar Materia")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        self.materia_input = QLineEdit(self)
        self.materia_input.setPlaceholderText("Nombre de la Materia")
        layout.addWidget(self.materia_input)

        self.profesor_input = QLineEdit(self)
        self.profesor_input.setPlaceholderText("Nombre del Profesor")
        layout.addWidget(self.profesor_input)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_data(self):
        materia = self.materia_input.text()
        profesor = self.profesor_input.text()
        if not materia or not profesor:
            QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")
            return
        
        # Guardar en la base de datos
        conn = sqlite3.connect("c:/Users/Emula/Desktop/Python-CRUD-QT/mi_base_de_datos.db")
        cursor = conn.cursor()
        try:
            # Primero, debes obtener el ID del profesor
            cursor.execute("SELECT id FROM usuarios WHERE nombre = ? AND apellido = ?", (profesor.split()[0], profesor.split()[1]))  # Suponiendo nombre completo
            result = cursor.fetchone()
            if result:
                profesor_id = result[0]
                cursor.execute("INSERT INTO materia (nombre_materia, id_profesor) VALUES (?, ?)", (materia, profesor_id))
                QMessageBox.information(self, "Éxito", "Materia guardada exitosamente.")
                self.parent().load_data()  # Recargar datos en la tabla
                self.close()
            else:
                QMessageBox.warning(self, "Error", "El profesor no se encuentra en la base de datos.")
        except sqlite3.Error as e:
            print(f"Error al guardar la materia: {e}")
            QMessageBox.warning(self, "Error", "No se pudo guardar la materia.")
        finally:
            conn.close()


