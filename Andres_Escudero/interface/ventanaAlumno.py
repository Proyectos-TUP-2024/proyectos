from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTreeWidget, QTreeWidgetItem, QCalendarWidget, QTextEdit, QTabWidget,QInputDialog
)
from PyQt6.QtCore import Qt,QFile,QTextStream
from database.db_nueva import Alumnos, Inscripciones, Profesores
from interface.ventanaInscripcion import VentanaInscripcion
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)


class VentanaAlumno(QMainWindow):
    def __init__(self, ventana_login, db, id_alumnos, id_profesor):
        super().__init__()
        self.ventana_login = ventana_login
        self.db = db
        self.id_alumnos = id_alumnos
        self.id_profesor = id_profesor
        self.consulta_inscripciones = Inscripciones(self.db)
        self.setWindowTitle("Ventana del Alumno")
        self.setGeometry(100, 100, 1000, 600)
        css_file = QFile(os.path.join(root_dir, "css", "ventanaAlumno_styles.css"))
        if css_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(css_file)
            self.setStyleSheet(stream.readAll())
            css_file.close()


        self.tab_widget = QTabWidget()  
        self.setCentralWidget(self.tab_widget)

   
        self.tab_materias = QWidget()
        self.init_tab_materias()
        self.tab_widget.addTab(self.tab_materias, "Materias y Calificaciones")
        self.init_tab_calendario()
        self.init_tab_mensajeria()
        self.init_tab_recursos()
        self.init_tab_perfil()

      
        self.btn_inscripcion = QPushButton("Inscribirse en Materias")
        self.btn_inscripcion.clicked.connect(self.mostrar_inscripcion)
        self.tab_widget.setCornerWidget(self.btn_inscripcion, Qt.Corner.TopRightCorner)

   
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.fAtras)
        self.tab_widget.setCornerWidget(self.btn_regresar, Qt.Corner.TopLeftCorner)



        self.tab_widget.tabBar().setStyleSheet("alignment: center;") 
        self.tab_widget.tabBar().setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    def init_tab_materias(self):
        layout = QVBoxLayout()
        label = QLabel("Resumen de Materias y Calificaciones")
        layout.addWidget(label)

       
        self.tree_widget_materias = QTreeWidget()
        self.tree_widget_materias.setColumnCount(3)
        self.tree_widget_materias.setHeaderLabels(["Materia", "Profesor", "Calificación"])
        layout.addWidget(self.tree_widget_materias)

      
        consulta_materia = Inscripciones(self.db)
        materias = consulta_materia.consulta_materias_por_alumno(self.id_alumnos)

        for materia, profesor, nota in materias:
            QTreeWidgetItem(self.tree_widget_materias, [materia, profesor, str(nota) if nota else "N/A"])
    
        self.tab_materias.setLayout(layout)

    def actualizar_materias_inscritas(self):
        self.tree_widget_materias.clear()
        consulta_materia = Inscripciones(self.db)
        materias = consulta_materia.consulta_materias_por_alumno(self.id_alumnos)

        for materia, profesor, nota in materias:
            QTreeWidgetItem(self.tree_widget_materias, [materia, profesor, str(nota) if nota else "N/A"])

    def init_tab_calendario(self):
        layout = QVBoxLayout()
        calendar_label = QLabel("Calendario Académico")
        calendar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(calendar_label)

        calendar = QCalendarWidget()
        layout.addWidget(calendar)

        container_widget = QWidget()
        container_widget.setLayout(layout)
        self.tab_widget.addTab(container_widget, "Calendario Académico")

    def init_tab_mensajeria(self):
        layout = QVBoxLayout()
        mensajeria_label = QLabel("Foro o Mensajería con Profesores")
        mensajeria_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mensajeria_label)

        self.mensajes = QTextEdit()
        self.mensajes.setPlaceholderText("Mensajes de profesores...")
        self.mensajes.setReadOnly(True)
        layout.addWidget(self.mensajes)

        self.cargar_mensajes_recibidos()

        self.nuevo_mensaje = QTextEdit()
        self.nuevo_mensaje.setPlaceholderText("Escribe tu mensaje aquí...")
        layout.addWidget(self.nuevo_mensaje)

        enviar_btn = QPushButton("Enviar Mensaje")
        enviar_btn.clicked.connect(self.enviar_mensaje)
        layout.addWidget(enviar_btn)

        container_widget = QWidget()
        container_widget.setLayout(layout)
        self.tab_widget.addTab(container_widget, "Mensajería")

    def init_tab_recursos(self):
        layout = QVBoxLayout()
        recursos_label = QLabel("Recursos de Estudio")
        recursos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(recursos_label)

        tree_widget = QTreeWidget()
        tree_widget.setColumnCount(2)
        tree_widget.setHeaderLabels(["Recurso", "Descripción"])
        layout.addWidget(tree_widget)

        recursos = [
            ("Presentación Matemáticas", "Temas de cálculo y álgebra."),
            ("PDF Historia", "Guía de estudio de la Edad Media."),
            ("Video Química", "Reacciones químicas en la vida diaria.")
        ]
        for recurso, descripcion in recursos:
            QTreeWidgetItem(tree_widget, [recurso, descripcion])

        container_widget = QWidget()
        container_widget.setLayout(layout)
        self.tab_widget.addTab(container_widget, "Recursos de Estudio")

    def init_tab_perfil(self):
        layout = QVBoxLayout()
        perfil_label = QLabel("Perfil del Alumno")
        perfil_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(perfil_label)

        alumnos = Alumnos(self.db)
        alumno = alumnos.consulta_alumno(self.id_alumnos)
        if alumno:
            nombre = alumno[2]
            apellido = alumno[3]
            promedio = alumno[4] if alumno[4] is not None else "Sin promedio"
            info_text = f"Nombre: {nombre} {apellido}\nPromedio: {promedio}"
            info = QLabel(info_text)
            layout.addWidget(info)
        else:
            layout.addWidget(QLabel("No se encontraron datos del alumno."))

        container_widget = QWidget()
        container_widget.setLayout(layout)
        self.tab_widget.addTab(container_widget, "Perfil")

    def mostrar_inscripcion(self):
        inscripciones = Inscripciones(self.db)
        materias = inscripciones.consulta_materias()
        self.ventana_inscripcion = VentanaInscripcion(materias, alumnos_id=self.id_alumnos, db=self.db)
        self.ventana_inscripcion.show()

    def cargar_mensajes_recibidos(self):
        """Carga los mensajes recibidos del profesor en la interfaz del alumno"""
        print(f"[DEBUG] Cargando mensajes recibidos para alumno ID: {self.id_alumnos}")
        
        mensajes = self.consulta_inscripciones.obtener_mensajes_para_alumno(self.id_alumnos)
        self.mensajes.clear()
        for mensaje, fecha in mensajes:
            mensaje_texto = f"Profesor:\n{mensaje}\nFecha: {fecha}\n{'-'*40}\n"
            self.mensajes.append(mensaje_texto)
        
        print(f"[DEBUG] Mensajes cargados en la interfaz: {mensajes}")

    def enviar_mensaje(self):
        """Método para enviar mensaje al profesor del alumno usando el área de texto 'self.nuevo_mensaje'"""
        print(f"[DEBUG] Enviando mensaje desde alumno ID: {self.id_alumnos}")

        try:
            id_profesor = self.consulta_inscripciones.obtener_id_profesor_por_alumno(self.id_alumnos)
            print(f"[DEBUG] ID del profesor obtenido: {id_profesor}")
            if id_profesor is None:
                print("[ERROR] No se encontró un profesor para este alumno.")
                QMessageBox.warning(self, "Error", "No se encontró un profesor asignado a este alumno.")
                return
            mensaje = self.nuevo_mensaje.toPlainText().strip()
            if mensaje:
                print(f"[DEBUG] Mensaje ingresado por el usuario: {mensaje}")
                exito = self.consulta_inscripciones.enviar_mensaje_al_profesor(self.id_alumnos, id_profesor, mensaje)
                if exito:
                    QMessageBox.information(self, "Éxito", "Mensaje enviado correctamente.")
                    self.nuevo_mensaje.clear()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo enviar el mensaje.")
            else:
                QMessageBox.warning(self, "Error", "El mensaje no puede estar vacío.")
        except AttributeError as e:
            print(f"[ERROR] Atributo no encontrado: {e}")
            QMessageBox.warning(self, "Error", f"Error: {e}")

    def fAtras(self):
        self.close()
        self.ventana_login.show()
