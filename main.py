"""
Aterrizar Main.py
"""

from modulo_grupo02 import (crear_usuarios, autenticar, menu_usuario, menu_admin, leer_datos)

# ------------------------- Cargar o inicializar datos -------------------------

#crear_usuarios(5) #Formato Usuario: Usuario{i} contraseña: 1234

# ------------------------- Inicio de sesion -------------------------
while True:
        print (" ")
        print("\nIngrese su usuario (o 'salir' para terminar):")
        usuario = input("> ").strip()
        if usuario.lower() == "salir":
            print("¡Hasta luego!")
            break
        print("Ingrese contraseña:")
        contrasena = input("> ").strip()

        user = autenticar(usuario, str(contrasena))
        if user == 1:
            viajes_usuario = leer_datos(usuario)[1]
            menu_usuario(viajes_usuario, usuario)
        elif user == 2:
            menu_admin(usuario)
        else:
            print("Usuario o contraseña incorrecta")