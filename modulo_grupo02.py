
"""
Módulo del equipo GRUPO 02 - Sistema de Viajes (Etapa 1 con Excepciones)
- Estructuras: listas, listas de listas (matrices), cadenas, funciones
- Ahora incorpora: manejo de excepciones (try/except, raise) según Clase 06
- No usa archivos, ni POO, ni diccionarios/tuplas/conjuntos
"""
import random

# ------------------------- Excepciones propias -------------------------
class AuthError(Exception):
    pass

class MenuOptionError(Exception):
    pass

class DestinationError(Exception):
    pass

class EmptyItineraryError(Exception):
    pass

# ------------------------- Datos simulados base -------------------------
DESTINOS = ["CABA", "La Plata", "Mar del Plata", "Rosario", "Córdoba", "Mendoza", "Salta", "Bariloche"]
PROVINCIAS = ["CABA", "Buenos Aires", "Buenos Aires", "Santa Fe", "Córdoba", "Mendoza", "Salta", "Río Negro"]

_KM = [
    [0,   56,  415, 300, 700, 1050, 1540, 1620],
    [56,   0,  355, 330, 690, 1100, 1590, 1700],
    [415,355,    0, 620, 950, 1350, 1850, 1600],
    [300,330,  620,   0, 400, 1050, 1320, 1500],
    [700,690,  950, 400,   0,  620,  980, 1450],
    [1050,1100,1350,1050,620,   0,  1200, 800],
    [1540,1590,1850,1320,980, 1200,   0, 2100],
    [1620,1700,1600,1500,1450, 800, 2100,   0],
]

# ------------------------- Utilidades -------------------------
def idx_destino(nombre):
    i = 0
    while i < len(DESTINOS) and DESTINOS[i].lower() != nombre.lower():
        i += 1
    return i if i < len(DESTINOS) else -1

def km_entre(origen, destino):
    i, j = idx_destino(origen), idx_destino(destino)
    if i == -1 or j == -1:
        raise DestinationError("Destino desconocido para calcular KM.")
    return _KM[i][j]

def provincia_de(destino):
    i = idx_destino(destino)
    if i == -1:
        raise DestinationError("Destino desconocido para obtener provincia.")
    return PROVINCIAS[i]

def input_int(prompt):
    """Lee un entero por teclado con validación y manejo de ValueError."""
    while True:
        try:
            s = input(prompt).strip()
            return int(s)
        except ValueError:
            print("❌ Debe ingresar un número entero. Intente nuevamente.")

# ------------------------- Autenticación -------------------------
def crear_usuarios_simulados(n):
    usuarios = ["admin"] + [f"user{i+1}" for i in range(n)]
    contras = ["admin"] + ["1234" for _ in range(n)]
    viajes = [[] for _ in usuarios]
    return usuarios, contras, viajes

def autenticar(usuarios, contras, user, pwd):
    i = 0
    while i < len(usuarios):
        if usuarios[i] == user and contras[i] == pwd:
            return i
        i += 1
    raise AuthError("Credenciales inválidas.")

# ------------------------- Registro y consulta de viajes (usuario) -------------------------
def registrar_viaje(viajes, pos_usuario):
    print("Ingrese ORIGEN (o 'fin' para cancelar):")
    origen = input("> ").strip()
    if origen.lower() == "fin":
        return
    if idx_destino(origen) == -1:
        raise DestinationError("Origen no válido. Debe ser uno de los destinos conocidos.")
    trayecto = [origen]
    print("Ingrese destinos uno por uno. Escriba 'fin' para terminar.")
    while True:
        dest = input("Destino: ").strip()
        if dest.lower() == "fin":
            break
        if dest == "":
            print("Destino vacío: intente nuevamente.")
        else:
            if idx_destino(dest) == -1:
                raise DestinationError(f"Destino no válido: '{dest}'.")
            if dest == trayecto[-1]:
                print("Destino igual al anterior, no se agrega.")
            else:
                trayecto.append(dest)
    viajes[pos_usuario] = trayecto

def consultar_viaje(viajes, pos_usuario):
    viaje = viajes[pos_usuario]
    if len(viaje) == 0:
        print("No hay viaje cargado.")
        return
    print("Itinerario:")
    for i in range(len(viaje)):
        print(f"  {i}. {viaje[i]}")

def kms_viaje(viajes, pos_usuario):
    viaje = viajes[pos_usuario]
    if len(viaje) < 2:
        raise EmptyItineraryError("Aún no hay tramos suficientes para calcular KMs.")
    total = 0
    i = 0
    while i < len(viaje) - 1:
        total += km_entre(viaje[i], viaje[i+1])
        i += 1
    print(f"KM del viaje: {total}")
    return total

def cant_escalas(viajes, pos_usuario):
    viaje = viajes[pos_usuario]
    cantidad = len(viaje) - 1 if len(viaje) > 0 else 0
    print(f"Cantidad de escalas/destinos: {cantidad}")
    return cantidad

def cant_provincias(viajes, pos_usuario):
    viaje = viajes[pos_usuario]
    if len(viaje) == 0:
        print("No hay viaje cargado.")
        return 0
    provincias_vistas = []
    i = 1
    while i < len(viaje):
        try:
            prov = provincia_de(viaje[i])
            j, esta = 0, False
            while j < len(provincias_vistas) and not esta:
                esta = provincias_vistas[j] == prov
                j += 1
            if not esta:
                provincias_vistas.append(prov)
        except DestinationError as e:
            print("Aviso:", e)
        i += 1
    print("Provincias visitadas:", provincias_vistas)
    return len(provincias_vistas)

def eliminar_viaje(viajes, pos_usuario):
    viajes[pos_usuario] = []
    print("Viaje eliminado.")

# ------------------------- Estadísticas (admin) -------------------------
def cantidad_usuarios(usuarios):
    return len(usuarios)

def total_km_todos(viajes):
    total = 0
    i = 0
    while i < len(viajes):
        j = 0
        while j < len(viajes[i]) - 1:
            try:
                total += km_entre(viajes[i][j], viajes[i][j+1])
            except DestinationError:
                pass
            j += 1
        i += 1
    return total

def top5_destinos(viajes):
    visitas = [0] * len(DESTINOS)
    i = 0
    while i < len(viajes):
        j = 1
        while j < len(viajes[i]):
            idx = idx_destino(viajes[i][j])
            if idx != -1:
                visitas[idx] += 1
            j += 1
        i += 1
    indices = list(range(len(DESTINOS)))
    a = 0
    while a < len(indices) - 1:
        pos_max = a
        b = a + 1
        while b < len(indices):
            if visitas[indices[b]] > visitas[indices[pos_max]]:
                pos_max = b
            b += 1
        aux = indices[a]
        indices[a] = indices[pos_max]
        indices[pos_max] = aux
        a += 1
    resultado = []
    k = 0
    while k < 5 and k < len(indices):
        if visitas[indices[k]] > 0:
            resultado.append([DESTINOS[indices[k]], visitas[indices[k]]])
        k += 1
    return resultado

def usuario_max_km(usuarios, viajes):
    mejor = -1
    mejor_km = -1
    i = 0
    while i < len(usuarios):
        km_u = 0
        j = 0
        while j < len(viajes[i]) - 1:
            try:
                km_u += km_entre(viajes[i][j], viajes[i][j+1])
            except DestinationError:
                pass
            j += 1
        if km_u > mejor_km:
            mejor_km = km_u
            mejor = i
        i += 1
    return (usuarios[mejor] if mejor != -1 else "", mejor_km)

def usuario_max_destinos(usuarios, viajes):
    mejor = -1
    mejor_cant = -1
    i = 0
    while i < len(usuarios):
        cant = len(viajes[i]) - 1 if len(viajes[i]) > 0 else 0
        if cant > mejor_cant:
            mejor_cant = cant
            mejor = i
        i += 1
    return (usuarios[mejor] if mejor != -1 else "", mejor_cant)

def cambiar_contrasena(usuarios, contrasenas):
    print("Usuario a modificar:")
    u = input("> ").strip()
    i = 0
    while i < len(usuarios) and usuarios[i] != u:
        i += 1
    if i < len(usuarios):
        print("Nueva contraseña:")
        contrasenas[i] = input("> ").strip()
        print("Contraseña cambiada.")
    else:
        raise AuthError("Usuario no encontrado.")

# ------------------------- Simulador de datos -------------------------
def simular_viajes(viajes, prob_tener_viaje=0.8):
    i = 0
    while i < len(viajes):
        if random.random() < prob_tener_viaje:
            total_paradas = random.randint(2, 5)
            origen = DESTINOS[random.randint(0, len(DESTINOS)-1)]
            trayecto = [origen]
            j = 1
            while j < total_paradas:
                d = DESTINOS[random.randint(0, len(DESTINOS)-1)]
                if d != trayecto[-1]:
                    trayecto.append(d)
                    j += 1
            viajes[i] = trayecto
        i += 1
    return viajes

# ------------------------- Menús -------------------------
def menu_usuario(nombre, usuarios, contras, viajes, pos_usuario):
    opcion = -1
    while opcion != 7:
        print("\n--- Menú Usuario ---")
        print("1) Registrar viaje")
        print("2) Consultar viaje")
        print("3) Consultar KMs del viaje")
        print("4) Consultar cantidad de escalas")
        print("5) Consultar cantidad de provincias visitadas")
        print("6) Eliminar viaje")
        print("7) Cerrar sesión")
        try:
            opcion = input_int("Opción: ")
            if opcion == 1:
                try:
                    registrar_viaje(viajes, pos_usuario)
                except DestinationError as e:
                    print("❌", e)
            elif opcion == 2:
                consultar_viaje(viajes, pos_usuario)
            elif opcion == 3:
                try:
                    kms_viaje(viajes, pos_usuario)
                except (EmptyItineraryError, DestinationError) as e:
                    print("❌", e)
            elif opcion == 4:
                cant_escalas(viajes, pos_usuario)
            elif opcion == 5:
                cant_provincias(viajes, pos_usuario)
            elif opcion == 6:
                eliminar_viaje(viajes, pos_usuario)
            elif opcion == 7:
                print("Cerrando sesión...")
            else:
                raise MenuOptionError("Opción inválida.")
        except MenuOptionError as e:
            print("❌", e)

def menu_admin(usuarios, contras, viajes):
    opcion = -1
    while opcion != 8:
        print("\n--- Menú Admin ---")
        print("1) Cantidad de usuarios")
        print("2) KM totales (todos los usuarios)")
        print("3) Destinos más frecuentados (top 5)")
        print("4) Usuario con más KM")
        print("5) Usuario con más destinos")
        print("6) Menú de usuario (impersonar)")
        print("7) Cambiar contraseña de usuario")
        print("8) Cerrar sesión")
        try:
            opcion = input_int("Opción: ")
            if opcion == 1:
                print("Cantidad de usuarios:", cantidad_usuarios(usuarios))
            elif opcion == 2:
                print("KM totales:", total_km_todos(viajes))
            elif opcion == 3:
                top = top5_destinos(viajes)
                if len(top) == 0:
                    print("Sin datos suficientes.")
                else:
                    i = 0
                    print("Top 5 destinos:")
                    while i < len(top):
                        print(f" {i+1}. {top[i][0]} - {top[i][1]} visitas")
                        i += 1
            elif opcion == 4:
                u, km = usuario_max_km(usuarios, viajes)
                print("Usuario con más KM:", u, "-", km, "KM")
            elif opcion == 5:
                u, cant = usuario_max_destinos(usuarios, viajes)
                print("Usuario con más destinos:", u, "-", cant, "destinos")
            elif opcion == 6:
                print("Usuario a simular menú:")
                u = input("> ").strip()
                i = 0
                while i < len(usuarios) and usuarios[i] != u:
                    i += 1
                if i < len(usuarios):
                    menu_usuario(usuarios[i], usuarios, contras, viajes, i)
                else:
                    print("❌ Usuario no encontrado.")
            elif opcion == 7:
                try:
                    cambiar_contrasena(usuarios, contras)
                except AuthError as e:
                    print("❌", e)
            elif opcion == 8:
                print("Cerrando sesión...")
            else:
                raise MenuOptionError("Opción inválida.")
        except MenuOptionError as e:
            print("❌", e)
