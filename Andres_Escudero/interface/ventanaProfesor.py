import sys
import os
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTreeWidget, QTreeWidgetItem, QTabWidget, QTextEdit, QMessageBox, QFrame, QInputDialog
)
from PyQt6.QtCore import Qt, QFile, QTextStream


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir) 

from database.db_nueva import Database
from database.db_nueva import Alumnos, Inscripciones, Profesores

class VentanaProfesor(QMainWindow):
    def __init__(self, ventana_login, db, id_profesor):
        super().__init__()
        self.ventana_login = ventana_login
        self.db = db
        self.id_profesor = id_profesor

        css_file = QFile(os.path.join(root_dir, "css", "ventanaProfesor_styles.css"))
        if css_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(css_file)
            self.setStyleSheet(stream.readAll())
            css_file.close()
      
        self.setWindowTitle("Gestión de Alumnos y Mensajes")
        self.setGeometry(100, 100, 920, 500)

     
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        button_layout = QHBoxLayout()

   
        self.btnAtras = QPushButton("Atras", self)
        self.btnAtras.clicked.connect(self.fAtras)
        button_layout.addWidget(self.btnAtras, alignment=Qt.AlignmentFlag.AlignLeft)

        self.btnAgregarCalificacion = QPushButton("Agregar Calificación", self)
        self.btnAgregarCalificacion.clicked.connect(self.fAgregarCalificacion)
        button_layout.addWidget(self.btnAgregarCalificacion, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(button_layout)

        self.tree_widget_alumnos = QTreeWidget()
        self.tree_widget_alumnos.setColumnCount(4)
        self.tree_widget_alumnos.setHeaderLabels(["ID", "Nombre", "Apellido", "Nota"])
        layout.addWidget(self.tree_widget_alumnos)


        self.cargar_alumnos()

        self.label = QLabel("Mensajes Recibidos de Alumnos", self)
        layout.addWidget(self.label)

        self.mensajes_recibidos = QTextEdit(self)
        self.mensajes_recibidos.setReadOnly(True)
        layout.addWidget(self.mensajes_recibidos)


        self.btn_actualizar = QPushButton("Actualizar Mensajes", self)
        self.btn_actualizar.clicked.connect(self.mostrar_mensajes)
        layout.addWidget(self.btn_actualizar)

        self.btn_responder = QPushButton("Responder Mensaje", self)
        self.btn_responder.clicked.connect(self.responder_mensaje)
        layout.addWidget(self.btn_responder)

        self.mostrar_mensajes()

    def cargar_alumnos(self):
        """Carga los alumnos inscritos en la materia del profesor"""
        inscripciones = Inscripciones(self.db)
        alumnos = inscripciones.consulta_alumnos_por_materia(self.id_profesor)
        self.tree_widget_alumnos.clear()
        
        for alumno in alumnos:
            if len(alumno) >= 4:
                QTreeWidgetItem(self.tree_widget_alumnos, [
                    str(alumno[0]),  
                    alumno[1],      
                    alumno[2],     
                    str(alumno[3]) if alumno[3] is not None else "N/A"  
                ])
            else:
                print("Advertencia: Fila incompleta para el alumno. Saltando entrada.")

    def fAgregarCalificacion(self):
        """Abre una ventana emergente para agregar una calificación al alumno seleccionado"""
        item = self.tree_widget_alumnos.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un alumno.")
            return
        alumno_id = int(item.text(0))
        nombre = item.text(1)
        apellido = item.text(2)
        calificacion, ok = QInputDialog.getDouble(
            self, "Agregar Calificación", f"Ingrese la calificación para {nombre} {apellido}:", 
            min=0, max=10, decimals=1
        )

        if ok:
            print(f"[DEBUG] Instanciando Alumnos con db: {self.db}")
            alumnos = Alumnos(self.db)
            if alumnos.modificar_nota(alumno_id, calificacion):
                item.setText(3, str(calificacion))
                QMessageBox.information(self, "Éxito", f"Calificación de {nombre} {apellido} actualizada a {calificacion}.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la calificación en la base de datos.")

    def mostrar_mensajes(self):
        """Muestra los mensajes recibidos de los alumnos"""
        profesores = Profesores(self.db)
        mensajes = profesores.leer_mensajes_alumnos(self.id_profesor)
        self.mensajes_recibidos.clear()

        for nombre, apellido, mensaje, fecha in mensajes:
            item_text = f"De {nombre} {apellido} el {fecha}:\n{mensaje}\n\n"
            self.mensajes_recibidos.append(item_text)

    def responder_mensaje(self):
        """Envía una respuesta al alumno seleccionado"""
        alumno_nombre, ok = QInputDialog.getText(self, "Responder a Alumno", "Ingresa el nombre del alumno:")
        if ok and alumno_nombre:
            mensaje, ok = QInputDialog.getText(self, "Enviar Respuesta", "Escribe tu respuesta:")
            if ok and mensaje:
                id_alumno = self.obtener_id_alumno_por_nombre(alumno_nombre)
                if id_alumno:
                    exito = self.enviar_respuesta_al_alumno(id_alumno, mensaje)
                    if exito:
                        QMessageBox.information(self, "Éxito", "Respuesta enviada correctamente.")
                    else:
                        QMessageBox.warning(self, "Error", "No se pudo enviar la respuesta.")
                else:
                    QMessageBox.warning(self, "Error", "Alumno no encontrado.")

    def obtener_id_alumno_por_nombre(self, nombre):
        """Obtiene el ID del alumno por su nombre"""
        consulta_alumnos = Alumnos(self.db)
        id_alumno = consulta_alumnos.obtener_id_alumno_por_nombre(nombre)
        print(f"[DEBUG] ID del alumno para nombre '{nombre}': {id_alumno}")
        return id_alumno

    def enviar_respuesta_al_alumno(self, id_alumno, mensaje):
        """Envía una respuesta al alumno y la guarda en la tabla notificaciones"""
        try:
            print(f"[DEBUG] Preparando para enviar respuesta al alumno ID {id_alumno}")
            print(f"[DEBUG] Contenido de la respuesta: {mensaje}")

            cur = self.db.cnn.cursor()
            query = """
                INSERT INTO notificaciones (id_profesor, id_alumnos, mensaje, fecha)
                VALUES (?, ?, ?, datetime('now'))
            """
            print(f"[DEBUG] Ejecutando consulta SQL para enviar respuesta al alumno: {query}")
            cur.execute(query, (self.id_profesor, id_alumno, mensaje))
            self.db.cnn.commit()
            cur.close()
            
            print(f"[DEBUG] Respuesta enviada correctamente al alumno ID {id_alumno}")
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Error al enviar respuesta al alumno: {e}")
            return False
    def fAtras(self):
        """Regresa a la ventana de inicio de sesión"""
        self.close()
        self.ventana_login.show()
