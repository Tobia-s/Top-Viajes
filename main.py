"""
Aterrizar Main.py
"""
import os
from modulo_grupo02 import (
    crear_viajeros_simulados, simular_viajes,
    autenticar, menu_usuario, menu_admin, AuthError, escribir_log, leer_datos, escribir_datos, get_usuario_por_numero, reporte_consolidado, cambiar_contrasena
)

# ------------------------- Cargar o inicializar datos -------------------------
'''
viajes_usuario = cargar_datos()
if viajes_usuario is None:
    # No hay archivo: creamos y simulamos
    viajes_usuario = crear_viajeros_simulados(5)
    viajes_usuario = simular_viajes(viajes_usuario, prob_tener_viaje=0.8)
    guardar_datos(viajes_usuario)'''

# ------------------------- Inicio de sesion -------------------------
a = True
if a: 
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
else:
    cambiar_contrasena("Jorge")