"""
main.py - Voyago (diccionarios, tuplas, sets y archivos JSON)
"""
from modulo_grupo02 import (
    cargar_datos, guardar_datos, crear_viajeros_simulados, simular_viajes,
    autenticar, menu_usuario, menu_admin, AuthError
)

# ------------------------- Cargar o inicializar datos -------------------------
try:
    logs = open("logs.txt", "w")
except OSError:
    print("Error de archivo de log, cerrando")
else:

    viajeros = cargar_datos()
    if viajeros is None:
        # No hay archivo: creamos y simulamos
        viajeros = crear_viajeros_simulados(5)
        viajeros = simular_viajes(viajeros, prob_tener_viaje=0.8)
        guardar_datos(viajeros)

    # ------------------------- Inicio de sesion -------------------------
    while True:
        print("\nIngrese su usuario (o 'salir' para terminar):")
        u = input("> ").strip()
        if u.lower() == "salir":
            print("¡Hasta luego!")
            break
        print("Ingrese contraseña:")
        p = input("> ").strip()




        try:
            user = autenticar(viajeros, u, p)
            if user == "admin":
                logs.write("Usuario admin logueado")
                menu_admin(viajeros, logs)
            else:
                logs.write("Usuario logueado")
                logs.write(user)
                menu_usuario(viajeros, user, logs)
        except AuthError as e:
            print(e)
finally:
    logs.close