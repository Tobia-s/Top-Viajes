from modulo_grupo02 import (
    crear_usuarios_simulados, simular_viajes,
    menu_usuario, menu_admin, autenticar, AuthError
)

usuarios, contras, viajes = crear_usuarios_simulados(5)
viajes = simular_viajes(viajes, prob_tener_viaje=0.8)

#  Inicio de sesión 
while True:
    print("\nIngrese su usuario (o 'salir' para terminar):")
    u = input("> ").strip()
    if u.lower() == "salir":
        print("¡Hasta luego!")
        break
    print("Ingrese contraseña:")
    p = input("> ").strip()

    try:
        pos = autenticar(usuarios, contras, u, p)
        if usuarios[pos] == "admin":
            menu_admin(usuarios, contras, viajes)
        else:
            menu_usuario(usuarios[pos], usuarios, contras, viajes, pos)
    except AuthError as e:
        print("Error", e)
