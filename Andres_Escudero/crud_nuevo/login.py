from PyQt6.QtWidgets import (
    QApplication,QComboBox, QWidget,QDateEdit, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from database.db import Database
from database.consulta_usuario import Usuarios
from interface.ventanaAdministrador import VentanaAdmin
from interface.ventanaProfesor import VentanaProfesor
from interface.ventanaAlumno import VentanaAlumno

class VentanaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale = 70
        self.setGeometry(40, 100, 400, 300)
        self.setWindowTitle("Login")

        # Crear el widget central
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet("background-color: rgb(105, 105, 105);")
        
        # Layouts
        self.layout_general = QHBoxLayout()
        self.form_layout = QVBoxLayout() 
        self.form_input_layout = QVBoxLayout()
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        
        # Imagen
        self.img = QLabel()
        self.pixmap = QPixmap("./layout/fondo_logo.jpg").scaled(600, 600)
        self.img.setPixmap(self.pixmap)

        # Componentes del formulario
        self.title = QLabel("Login")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: black; font-size: 36px; font-weight:bold;")
        self.title.setMaximumHeight(50)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("Usuario")
        self.email.setTextMargins(20, 0, 0, 0)
        self.email.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px;") 
        self.email.setMinimumSize(int(self.width() * 0.5), 50)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setTextMargins(20, 0, 0, 0)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px;")
        self.password.setMinimumSize(int(self.width() * 0.5), 50)

        self.btnLogin = QPushButton("Iniciar Sesion")
        self.btnLogin.setStyleSheet("background-color: #6339A7; font-size: 15px; font-weight: bold; border-radius: 15px; padding: 10px;")
        self.btnLogin.setMinimumSize(int(self.width() * 0.6), 50)
        self.btnLogin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btnLogin.clicked.connect(self.iniciar_sesion)

        self.btnregistrar = QPushButton("Registrarse")
        self.btnregistrar.setStyleSheet("background-color: #6339A7; font-size: 15px; font-weight: bold; border-radius: 15px; padding: 10px;")
        self.btnregistrar.setMinimumSize(int(self.width() * 0.6), 50)
        self.btnregistrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btnregistrar.clicked.connect(self.mostrar_registro)

        # Añadir widgets al layout del formulario
        self.form_input_layout.addWidget(self.email)
        self.form_input_layout.addWidget(self.password)
        self.form_input_layout.addWidget(self.btnLogin)
        self.form_input_layout.addWidget(self.btnregistrar)
        self.form_input_layout.setSpacing(10)
        
        # Añadir el título y el layout del formulario al layout principal
        self.form_layout.addWidget(self.title)
        self.form_layout.addLayout(self.form_input_layout)
        self.form_layout.setSpacing(0)

        # Agregar imagen y layout del formulario al layout general
        self.layout_general.addWidget(self.img)
        self.layout_general.addWidget(self.form_widget)
        self.layout_general.addLayout(self.form_layout)

        # Establecer el layout general en el widget central
        self.centralWidget.setLayout(self.layout_general)
        
        # Tamaño de la ventana
        self.setMinimumSize(14 * self.scale, 7 * self.scale)
        self.setMaximumSize(14 * self.scale, 7 * self.scale)

    def mostrar_registro(self):
        self.ventana_registro = VentanaRegistro()
        self.ventana_registro.show()

    def iniciar_sesion(self):
        usuario = self.email.text()
        contraseña = self.password.text()

    # Crear una instancia de Alumnos para verificar las credenciales
        db = Usuarios()

    # Verificar las credenciales
        if db.verificar_usuario(usuario, contraseña):
        # Obtener el rol del usuario
            rol = db.obtener_rol_usuario(usuario)  # Aquí solo necesitas el usuario

            if rol == "Profesor":
                self.ventana_profesor = VentanaProfesor()
                self.ventana_profesor.show()
            elif rol == "Alumno":
                self.ventana_alumno = VentanaAlumno()
                self.ventana_alumno.show()
            elif rol == "Admin":
                self.ventana_admin = VentanaAdmin()  # Suponiendo que tienes una clase VentanaAdmin
                self.ventana_admin.show()    
            else:
                QMessageBox.warning(self, "Error", "Rol de usuario no reconocido.")
        
            self.close()  # Cerrar la ventana de login
        else:
                QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

        self.hide()
                
    def obtener_rol_usuario(self, usuario):
        db = Usuarios()  # Asegúrate de que tu clase Alumnos tenga este método
        # Lógica para obtener el rol del usuario
        rol = db.obtener_rol_usuario(usuario)  # Debes implementar este método en tu clase Alumnos
        return rol
    
    def show_login(self):
        print("Mostrando ventana de login")
        self.show()
    
class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(150, 150, 400, 250)
        
        # Layout y widgets del formulario de registro
        layout = QVBoxLayout()
        
        self.rol = QComboBox()
        self.rol.addItems(["Seleccionar Rol", "Alumno", "Profesor"])  # Opciones de rol
        layout.addWidget(self.rol)
        
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre")
        layout.addWidget(self.nombre)
        
        self.apellido = QLineEdit()
        self.apellido.setPlaceholderText("Apellido")
        layout.addWidget(self.apellido)
        
        self.edad = QLineEdit()
        self.edad.setPlaceholderText("Edad")
        layout.addWidget(self.edad)
        
        h_layout_fecha = QHBoxLayout()

        # Etiqueta para Fecha de Nacimiento
        self.label_fecha_nacimiento = QLabel("Fecha de Nacimiento:")
        h_layout_fecha.addWidget(self.label_fecha_nacimiento)

        # Campo de entrada para la fecha de nacimiento
        self.fecha_nacimiento = QDateEdit()
        self.fecha_nacimiento.setDisplayFormat("dd/MM/yyyy")  # Formato de la fecha
        self.fecha_nacimiento.setCalendarPopup(True)  # Desplegar un calendario al hacer clic
        h_layout_fecha.addWidget(self.fecha_nacimiento)

        # Añadir el layout horizontal al layout principal
        layout.addLayout(h_layout_fecha)
                
        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)
        
        self.btnRegistrar = QPushButton("Registrar")
        self.btnRegistrar.clicked.connect(self.registrar_usuario)
        layout.addWidget(self.btnRegistrar)
        
        self.setLayout(layout)

    def registrar_usuario(self):
        nombre = self.nombre.text()  # Cambiado de username a nombre
        apellido = self.apellido.text()  # Cambiado de username a apellido
        edad = self.edad.text()  # Obtiene el valor de la edad
        contraseña = self.password.text()
        rol_seleccionado = self.rol.currentText()

        if rol_seleccionado == "Seleccionar Rol":
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un rol.")
            return
        
        # Aquí puedes llamar al método registrar_usuario de la clase Alumnos
        db = Database()
        resultado = db.registrar_usuario(nombre, apellido, edad, contraseña, rol_seleccionado)  # Debes definir el método en tu clase

        if resultado:
            QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente.")
            self.close()  # Cerrar ventana de registro
        else:
            QMessageBox.critical(self, "Error", "Error al registrar el usuario.")