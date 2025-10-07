import json
import os
import random

DATA_FILE = "viajeros.json"
# ------------------------- Excepciones propias -------------------------
class AuthError(Exception):
    pass

class MenuOptionError(Exception):
    pass

class DestinationError(Exception):
    pass

class EmptyItineraryError(Exception):
    pass

# ------------------------- Utilidades simples -------------------------
normalizar = lambda s: s.strip()  
def input_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Debe ingresar un numero entero. Intente nuevamente.")

# ------------------------- Datos base (destinos, provincias, matriz km) -------------------------
DESTINOS = ["CABA", "La Plata", "Mar del Plata", "Rosario", "Cordoba", "Mendoza", "Salta", "Bariloche"]
PROVINCIAS = ["CABA", "Buenos Aires", "Buenos Aires", "Santa Fe", "Cordoba", "Mendoza", "Salta", "Rio Negro"]

# Matriz de distancias (km) - simetrica, 0 en diagonal
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

def idx_destino(nombre):
    nombre = nombre.lower()
    i = 0
    while i < len(DESTINOS) and DESTINOS[i].lower() != nombre:
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

# ------------------------- Persistencia (JSON) -------------------------
def _encode_for_json(viajeros):
    """Convierte tramos tuple->list para que sean serializables en JSON."""
    salida = {}
    for u, data in viajeros.items():
        tramos = [[a, b] for (a, b) in data.get("viaje", [])]
        salida[u] = {"password": data.get("password", ""), "viaje": tramos}
    return salida

def _decode_from_json(data):
    """Convierte tramos list->tuple al cargar JSON."""
    viajeros = {}
    for u, d in data.items():
        tramos = [(a, b) for [a, b] in d.get("viaje", [])]
        viajeros[u] = {"password": d.get("password", ""), "viaje": tramos}
    return viajeros

def guardar_datos(viajeros, archivo=DATA_FILE):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(_encode_for_json(viajeros), f, ensure_ascii=False, indent=2)

def cargar_datos(archivo=DATA_FILE):
    if not os.path.exists(archivo):
        return None
    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)
    return _decode_from_json(data)


def crear_viajeros_simulados(n):
    viajeros = {"admin": {"password": "admin", "viaje": []}}
    i = 1
    while i <= n:
        viajeros[f"user{i}"] = {"password": "1234", "viaje": []}
        i += 1
    return viajeros

def simular_viajes(viajeros, prob_tener_viaje=0.8):
    for u in viajeros.keys():
        if random.random() < prob_tener_viaje:
            total_paradas = random.randint(2, 5)
            origen = DESTINOS[random.randint(0, len(DESTINOS)-1)]
            paradas = [origen]
            j = 1
            while j < total_paradas:
                d = DESTINOS[random.randint(0, len(DESTINOS)-1)]
                if d != paradas[-1]:
                    paradas.append(d)
                    j += 1
            # convertir paradas en tramos (tuplas)
            tramos = []
            k = 0
            while k < len(paradas) - 1:
                tramos.append((paradas[k], paradas[k+1]))
                k += 1
            viajeros[u]["viaje"] = tramos
    return viajeros

# ------------------------- Autenticación (diccionario) -------------------------
def autenticar(viajeros, user, pwd):
    data = viajeros.get(user)
    if not data or data["password"] != pwd:
        raise AuthError("Credenciales invalidas.")
    return user  

# ------------------------- Utilidades de viaje (con tuplas de tramos) -------------------------
def reconstruir_paradas(tramos):
    """De [(A,B),(B,C),(C,D)] devuelve [A,B,C,D]. Si no hay tramos -> []."""
    if not tramos:
        return []
    paradas = [tramos[0][0]]
    i = 0
    while i < len(tramos):
        paradas.append(tramos[i][1])
        i += 1
    return paradas

def registrar_viaje(viajeros, user):
    print("Ingrese ORIGEN (o 'fin' para cancelar):")
    origen = normalizar(input("> "))
    if origen.lower() == "fin":
        return
    if idx_destino(origen) == -1:
        raise DestinationError("Origen no valido. Debe ser uno de los destinos conocidos.")

    print("Ingrese destinos uno por uno. Escriba 'fin' para terminar.")
    paradas = [origen]
    while True:
        dest = normalizar(input("Destino: "))
        if dest.lower() == "fin":
            break
        if dest == "":
            print("Destino vacio: intente nuevamente.")
            continue
        if idx_destino(dest) == -1:
            raise DestinationError(f"Destino no valido: '{dest}'.")
        if dest == paradas[-1]:
            print("Destino igual al anterior, no se agrega.")
            continue
        paradas.append(dest)

    
    tramos = []
    i = 0
    while i < len(paradas) - 1:
        tramos.append((paradas[i], paradas[i+1]))
        i += 1
    viajeros[user]["viaje"] = tramos

def consultar_viaje(viajeros, user):
    tramos = viajeros[user]["viaje"]
    paradas = reconstruir_paradas(tramos)
    if not paradas:
        print("No hay viaje cargado.")
        return
    print("Itinerario:")
    i = 0
    while i < len(paradas):
        print(f"  {i}. {paradas[i]}")
        i += 1

def kms_viaje(viajeros, user):
    tramos = viajeros[user]["viaje"]
    if len(tramos) == 0:
        raise EmptyItineraryError("Aun no hay tramos suficientes para calcular KMs.")
    total = 0
    i = 0
    while i < len(tramos):
        a, b = tramos[i]
        total += km_entre(a, b)
        i += 1
    print(f"KM del viaje: {total}")
    return total

def cant_escalas(viajeros, user):
    tramos = viajeros[user]["viaje"]
    print(f"Cantidad de escalas/destinos: {len(tramos)}")
    return len(tramos)

def cant_provincias(viajeros, user):
    tramos = viajeros[user]["viaje"]
    paradas = reconstruir_paradas(tramos)
    if not paradas:
        print("No hay viaje cargado.")
        return 0
    provs = set()
    i = 1
    while i < len(paradas):
        provs.add(provincia_de(paradas[i]))
        i += 1
    print("Provincias visitadas:", sorted(list(provs)))
    return len(provs)

def eliminar_viaje(viajeros, user):
    viajeros[user]["viaje"] = []
    print("Viaje eliminado.")

# ------------------------- Reportes (admin) -------------------------
def cantidad_usuarios(viajeros):
    return len(viajeros)

def total_km_todos(viajeros):
    total = 0
    for u, data in viajeros.items():
        i = 0
        while i < len(data["viaje"]):
            a, b = data["viaje"][i]
            try:
                total += km_entre(a, b)
            except DestinationError:
                pass
            i += 1
    return total

def top5_destinos(viajeros):
    # contamos apariciones de cada destino como destino final de tramo
    visitas = [0] * len(DESTINOS)
    for _, data in viajeros.items():
        i = 0
        while i < len(data["viaje"]):
            _, dest = data["viaje"][i]
            idx = idx_destino(dest)
            if idx != -1:
                visitas[idx] += 1
            i += 1
    # ordenamiento por seleccion sobre indices
    indices = list(range(len(DESTINOS)))
    a = 0
    while a < len(indices) - 1:
        pos_max = a
        b = a + 1
        while b < len(indices):
            if visitas[indices[b]] > visitas[indices[pos_max]]:
                pos_max = b
            b += 1
        indices[a], indices[pos_max] = indices[pos_max], indices[a]
        a += 1
    # top 5 con visitas > 0
    res = []
    k = 0
    while k < 5 and k < len(indices):
        if visitas[indices[k]] > 0:
            res.append([DESTINOS[indices[k]], visitas[indices[k]]])
        k += 1
    return res

def usuario_max_km(viajeros):
    mejor_user = ""
    mejor_km = -1
    for u, data in viajeros.items():
        km_u = 0
        i = 0
        while i < len(data["viaje"]):
            a, b = data["viaje"][i]
            try:
                km_u += km_entre(a, b)
            except DestinationError:
                pass
            i += 1
        if km_u > mejor_km:
            mejor_km = km_u
            mejor_user = u
    return mejor_user, mejor_km

def usuario_max_destinos(viajeros):
    mejor_user = ""
    mejor_cant = -1
    for u, data in viajeros.items():
        cant = len(data["viaje"])
        if cant > mejor_cant:
            mejor_cant = cant
            mejor_user = u
    return mejor_user, mejor_cant

def cambiar_contrasena(viajeros):
    print("Usuario a modificar:")
    u = normalizar(input("> "))
    if u not in viajeros:
        raise AuthError("Usuario no encontrado.")
    print("Nueva contrasena:")
    viajeros[u]["password"] = normalizar(input("> "))
    print("Contrasena cambiada.")

def reporte_consolidado(viajeros):
    max_paradas = 0
    for _, data in viajeros.items():
        paradas = reconstruir_paradas(data["viaje"])
        if len(paradas) > max_paradas:
            max_paradas = len(paradas)

    print("\n=== REPORTE CONSOLIDADO DE VIAJES (MATRIZ) ===")
    encabezado = ["Usuario"]
    j = 0
    while j < max_paradas:
        encabezado.append("Origen" if j == 0 else f"Destino {j}")
        j += 1
    print(" | ".join(encabezado))

    for u, data in viajeros.items():
        paradas = reconstruir_paradas(data["viaje"])
        fila = [u]
        j = 0
        while j < max_paradas:
            fila.append(paradas[j] if j < len(paradas) else "-")
            j += 1
        print(" | ".join(fila))

# ------------------------- Menus -------------------------
def menu_usuario(viajeros, user, logs):
    opcion = -1
    while opcion != 7:
        print("\n--- Menu Usuario ---")
        print("1) Registrar viaje")
        print("2) Consultar viaje")
        print("3) Consultar KMs del viaje")
        print("4) Consultar cantidad de escalas")
        print("5) Consultar cantidad de provincias visitadas")
        print("6) Eliminar viaje")
        print("7) Cerrar sesion")
        try:
            opcion = input_int("Opcion: ")
            if opcion == 1:
                try:
                    registrar_viaje(viajeros, user)
                    logs.write("un viaje se ha registrado por")
                    logs.write(user)
                    guardar_datos(viajeros)
                except DestinationError as e:
                    print(e)
            elif opcion == 2:
                consultar_viaje(viajeros, user)
            elif opcion == 3:
                try:
                    kms_viaje(viajeros, user)
                except (EmptyItineraryError, DestinationError) as e:
                    print(e)
            elif opcion == 4:
                cant_escalas(viajeros, user)
            elif opcion == 5:
                try:
                    cant_provincias(viajeros, user)
                except DestinationError as e:
                    print(e)
            elif opcion == 6:
                eliminar_viaje(viajeros, user)
                guardar_datos(viajeros)
            elif opcion == 7:
                print("Cerrando sesion...")
            else:
                raise MenuOptionError("Opcion invalida.")
        except MenuOptionError as e:
            print(e)

def menu_admin(viajeros, logs):
    opcion = -1
    while opcion != 9:
        print("\n--- Menu Admin ---")
        print("1) Cantidad de usuarios")
        print("2) KM totales (todos los usuarios)")
        print("3) Destinos mas frecuentados (top 5)")
        print("4) Usuario con mas KM")
        print("5) Usuario con mas destinos")
        print("6) Menu de usuario (impersonar)")
        print("7) Cambiar contrasena de usuario")
        print("8) Reporte consolidado (matriz de viajes)")
        print("9) Cerrar sesion")
        try:
            opcion = input_int("Opcion: ")
            if opcion == 1:
                print("Cantidad de usuarios:", cantidad_usuarios(viajeros))
            elif opcion == 2:
                print("KM totales:", total_km_todos(viajeros))
            elif opcion == 3:
                top = top5_destinos(viajeros)
                if not top:
                    print("Sin datos suficientes.")
                else:
                    print("Top 5 destinos:")
                    i = 0
                    while i < len(top):
                        print(f" {i+1}. {top[i][0]} - {top[i][1]} visitas")
                        i += 1
            elif opcion == 4:
                u, km = usuario_max_km(viajeros)
                print("Usuario con mas KM:", u, "-", km, "KM")
            elif opcion == 5:
                u, cant = usuario_max_destinos(viajeros)
                print("Usuario con mas destinos:", u, "-", cant, "destinos")
            elif opcion == 6:
                print("Usuario a simular menu:")
                u = normalizar(input("> "))
                if u in viajeros:
                    menu_usuario(viajeros, u)
                else:
                    print("Usuario no encontrado.")
            elif opcion == 7:
                try:
                    cambiar_contrasena(viajeros)
                    guardar_datos(viajeros)
                except AuthError as e:
                    print(e)
            elif opcion == 8:
                reporte_consolidado(viajeros)
            elif opcion == 9:
                logs.write("admin saliendo")
                print("Cerrando sesion...")
            else:
                raise MenuOptionError("Opcion invalida.")
        except MenuOptionError as e:
            print(e)
