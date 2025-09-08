
"""
main.py - Sistema de Viajes (Prototipo Etapa 1)
Ejecuta el flujo general: login simple + menús usuario/admin.
"""
from modulo_grupo02 import (
    crear_usuarios_simulados, simular_viajes,
    menu_usuario, menu_admin
)

# ------------------------- Bootstrap de demo -------------------------
# Creamos 5 usuarios simulados además de 'admin'
usuarios, contras, viajes = crear_usuarios_simulados(5)

# Simulamos viajes para mostrar reportes sin cargar mucho por teclado
viajes = simular_viajes(viajes, prob_tener_viaje=0.8)

# ------------------------- Inicio de sesión -------------------------
while True:
    print("\nIngrese su usuario (o 'salir' para terminar):")
    u = input("> ").strip()
    if u.lower() == "salir":
        print("¡Hasta luego!")
        break
    print("Ingrese contraseña:")
    p = input("> ").strip()

    # Autenticación por listas paralelas (sin diccionarios)
    i = 0
    pos = -1
    while i < len(usuarios) and pos == -1:
        if usuarios[i] == u and contras[i] == p:
            pos = i
        i += 1

    if pos == -1:
        print("Credenciales inválidas.")
    else:
        if usuarios[pos] == "admin":
            menu_admin(usuarios, contras, viajes)
        else:
            menu_usuario(usuarios[pos], usuarios, contras, viajes, pos)
