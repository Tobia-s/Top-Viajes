import json
import os
import random

TEMP_DATA_FILE = "viajeros.temp"
DATA_FILE = "viajeros.txt"
USER_FILE = "usuarios.txt"
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



# ------------------------- Persistencia (JSON) -------------------------

def crear_usuarios(cantidad, cant_viajes = 8, tipo = 1):
    '''Crea usuarios con viajes, recibe cantidad de usuarios, cantidad de viajes maximo y tipo: 1 si es normal, 2 si es admin '''
    for i in range(cantidad):
        crear_usuario_y_contrasena(f"Usuario{i}", "1234", tipo)

        escribir_datos(f"Usuario{i}",simular_viajes(cant_viajes))
        escribir_log(f"Usuario{i} creado \n")


def crear_usuario_y_contrasena(usuario, contrasena, tipo=1):
        '''Crea usuarios sin viajes, recibe usuario, contraseña y tipo 1 si es normal, 2 si es admin'''
        if escribir_datos(usuario, contrasena, USER_FILE, TEMP_DATA_FILE, False, tipo) == -1:
            print("Error al crear usuarios de prueba")
            escribir_log("Error al crear usuarios de prueba")


def simular_viajes(cant_viajes_max = 8):
    '''Usando Randint genera viajes aleatorios, recibe la cantidad maxima de viajes que se desea'''
    lista_viajes = []
    cant_paradas = random.randint(2, cant_viajes_max)
    lista_viajes.append(DESTINOS[random.randint(0, len(DESTINOS)-1)])
    i=0
    while i < cant_paradas - 1:
        proximo_destino = DESTINOS[random.randint(0, len(DESTINOS)-1)]
        if proximo_destino != lista_viajes[-1]:
            lista_viajes.append(proximo_destino)
            i += 1
    return lista_viajes
    



# ------------Refactor line ------------------------------------------------------------------------------------------------------------------------------------

# ------------------------- Reportes (admin) -------------------------
def top5_destinos():
    '''Devuelve los 5 destinos mas concurridos del dataset'''
    usuario = ""
    i=0
    visitas = [0] * len(DESTINOS)
    usuario = get_usuario_por_numero(i)
    while usuario != "-1":          #itera usuarios
        i += 1
        usuario_viajes = leer_datos(usuario)[1]
        for viaje in usuario_viajes:   #itera por cada destino del usuario
            for indice_destinos in range(len(DESTINOS)):
                if viaje == DESTINOS[indice_destinos]: #itera por cada destino en DESTINOS
                    visitas[indice_destinos] += 1
        usuario = get_usuario_por_numero(i)
    #visitas tiene la cantidad de veces que se visitó el destino (el indice coincide con la lista DESTINOS)
    lista_top5_destinos = []
    for _ in range(5):
        maximo = 0
        for indice in range(len(visitas)): #itera por todos los destinos (visitas) y guarda el indice mas grande
            if visitas[indice] > maximo:
                maximo = visitas[indice]
                indice_maximo = indice
        lista_top5_destinos.append(DESTINOS[indice_maximo])
        visitas[indice_maximo] = -1 #anulo el indice para que no se repita
    return lista_top5_destinos


def get_id_destino(nombre): #Validado
    '''Devuelve el id del destino para usar la lista de DESTINOS'''
    nombre = nombre.lower()
    i = 0
    while i < len(DESTINOS) and DESTINOS[i].lower() != nombre:
        i += 1
    return i if i < len(DESTINOS) else -1


def provincia_de(destino): #Validado
    '''Devuelve la provincia asociada al destino Rosario -> Santa Fe'''
    i = get_id_destino(destino)
    if i == -1:
        raise DestinationError("Destino desconocido para obtener provincia.")
    return PROVINCIAS[i]


def kms_viaje(viajes_usuario): #Validado
    '''Devuelve la cantidad de KM del usuario'''
    cant_viajes = len(viajes_usuario)
    if cant_viajes == 0:
        print("No hay viaje cargado.")
        return
    total = 0
    i = 0
    if cant_viajes > 1:
        while i < cant_viajes - 1:
            total += km_entre(viajes_usuario[i], viajes_usuario[i+1])
            i += 1
    return total


def cant_escalas(usuario_viajes):
    '''Enumera la cantidad de escalas de un Usuario'''
    print(f"Cantidad de escalas/destinos: {len(usuario_viajes)-1}")
    return len(usuario_viajes)-1


def cant_provincias(usuario_viajes):
    '''Devuelve la cantidad de provincias diferentes visitadas usando set() para evitar que se repitan'''
    if usuario_viajes == []:
        print("No hay viaje cargado.")
        return 0
    provs = set()
    i = 1
    while i < len(usuario_viajes):
        provs.add(provincia_de(usuario_viajes[i]))
        i += 1
    print("Provincias visitadas:", sorted(list(provs)))
    return len(provs)


def total_km_todos():
    '''Devuelve la suma de todos los kilometros de los usuarios'''
    indice_usuarios = 0
    total_km = 0
    usuario = get_usuario_por_numero(indice_usuarios)
    while usuario != "-1":
        indice_usuarios += 1
        viajes_usuario = leer_datos(usuario)[1]
        cant_destinos = len(viajes_usuario)
        if cant_destinos > 1:
            i=0
            while i < cant_destinos - 1:
                try:
                    total_km += km_entre(viajes_usuario[i], viajes_usuario[i+1])
                except DestinationError:
                    print("Error calculo KM")
                i += 1
        usuario = get_usuario_por_numero(indice_usuarios)
    return total_km
    

def km_entre(origen, destino):
    '''Usa la matriz de _KM y devuelve los KM, recibe un origen y un destino, estos tienen que estar en la tabla'''
    i, j = get_id_destino(origen), get_id_destino(destino)
    if i == -1 or j == -1:
        raise DestinationError("Destino desconocido para calcular KM.")
    return _KM[i][j]


def usuario_max_km():
    '''Devuelve el usuario con mas KMs'''
    usuario_max_km = ""
    indice_usuarios = 0
    max_km = 0
    usuario = get_usuario_por_numero(indice_usuarios)
    while usuario != "-1":
        indice_usuarios += 1
        viajes_usuario = leer_datos(usuario)[1]
        cant_destinos = len(viajes_usuario)
        km_usuario = 0
        if cant_destinos > 1:
            i = 0
            while i < cant_destinos - 1:
                try:
                    km_usuario += km_entre(viajes_usuario[i], viajes_usuario[i+1])
                except DestinationError:
                    print("Error calculo KM")
                    km_usuario = 0
                if km_usuario > max_km:
                    max_km = km_usuario
                    usuario_max_km = usuario
                i += 1
        usuario = get_usuario_por_numero(indice_usuarios)
    return usuario_max_km, max_km
    

def usuario_max_destinos():
    '''Devuelve el usuario con mas destinos'''
    usuario_max_dest = ""
    i=0
    max = 0
    usuario = get_usuario_por_numero(i)
    while usuario != "-1":
        i += 1
        datos = leer_datos(usuario)[1]
        cant_destinos = len(datos)
        if cant_destinos > max:
            max = cant_destinos
            usuario_max_dest = usuario
        usuario = get_usuario_por_numero(i)
    return usuario_max_dest, max
    


# ------------------------- Autenticación (diccionario) -------------------------
def autenticar(usuario_ingresado, contrasena_ingresada):
    '''usuario;contrasena;tipo (tipo = 1 si es normal | tipo = 2 si es admin | -1 si no encuentra al usuario)'''
    with open("usuarios.txt", mode="r", encoding="utf-8") as archivo_usuarios:
        linea_leida = archivo_usuarios.readline()
        tipo_leido = 0
        while(linea_leida != ""):
            usuario_a_autenticar, contrasena_a_verificar, tipo = linea_leida.split(";")
            if (usuario_ingresado == usuario_a_autenticar and contrasena_ingresada == invertir_chars(contrasena_a_verificar)):
                tipo_leido = int(tipo)
                break
            linea_leida = archivo_usuarios.readline()
        else:
            tipo_leido = -1
        return tipo_leido



def registrar_viaje(viajes_usuario): 
    '''Registra las paradas del usurio y retorna lista, si ya está la lista agrega los nuevos items'''
    while True:
        consultar_viaje(viajes_usuario)
        print("\n")
        print("Ingrese nuevo destino (o 'fin' para cancelar):")
        nuevo_destino = normalizar(input("> ").lower())
        if nuevo_destino.lower() == "fin":
            break
        if get_id_destino(nuevo_destino) == -1:
            raise DestinationError("Origen no valido. Debe ser uno de los destinos conocidos.")
        else:
            if len(viajes_usuario) == 0:
                viajes_usuario.append(nuevo_destino)
            else:
                if nuevo_destino == viajes_usuario[-1]:
                    print("Destino igual al anterior, no se agrega.")
                else:
                    viajes_usuario.append(nuevo_destino)



def consultar_viaje(viajes_usuario, con_leyenda=True):
    '''Muesta los viajes en formato tuple con un avion ascii'''

    cant_viajes = len(viajes_usuario)
    if cant_viajes == 0:
        print("No hay viaje cargado.")
        return
    print("Itinerario:") if con_leyenda else None
    i = 0
    if cant_viajes == 1:
         print(f"  {viajes_usuario[0]}")
    while i < cant_viajes - 1:
        print(f"  ({viajes_usuario[i]} \u2708  {viajes_usuario[i+1]})", end=" ")
        i += 1



# ------------------------- Menus -------------------------
def menu_usuario(viajes_usuario, usuario):
    escribir_log(f"{usuario} inició sesion \n")
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
                    registrar_viaje(viajes_usuario)
                    escribir_datos(usuario, viajes_usuario)
                    escribir_log(f"{usuario} editó sus viajes \n")
                except DestinationError as mensaje_error:
                    print(mensaje_error)
            elif opcion == 2:
                consultar_viaje(viajes_usuario)
                escribir_log(f"{usuario} consultó sus viajes \n")
            elif opcion == 3:
                try:
                    print(kms_viaje(viajes_usuario))
                except (EmptyItineraryError, DestinationError) as e:
                    print(e)
                    escribir_log(f"{usuario} error al calcular kilometros \n")
            elif opcion == 4:
                cant_escalas(viajes_usuario)
                escribir_log(f"{usuario} consultó la cantidad de escalas \n")
            elif opcion == 5:
                try:
                    cant_provincias(viajes_usuario)
                    escribir_log(f"{usuario} consultó cuantras povincias va a visitar con su viaje \n")
                except DestinationError as mensaje_error:
                    print(mensaje_error)
                    escribir_log(f"{usuario} Error de destino \n")
            elif opcion == 6:
                viajes_usuario = []
                escribir_datos(usuario, viajes_usuario)
                print("Viaje borrado")
                escribir_log(f"{usuario} borró sus viajes \n")
            elif opcion == 7:
                print("Cerrando sesion...")
                escribir_log(f"{usuario} cerró sesion \n")
            else:
                raise MenuOptionError("Opcion invalida.")
        except MenuOptionError as mensaje_error:
            print(mensaje_error)
            escribir_log(f"{usuario} Error de menú \n")



def menu_admin(usuario):
    escribir_log(f"{usuario} inició sesion como admin\n")
    opcion = -1
    while opcion != 9:
        print("\n--- Menu Admin ---")
        print("1) Cantidad de usuarios")
        print("2) KM totales (todos los usuarios)")
        print("3) Destinos mas frecuentados (top 5)")
        print("4) Usuario con mas KM")
        print("5) Usuario con mas destinos")
        print("6) Menu de usuario (impersonar)")
        print("7) Cambiar contrasena o agregar usuario")
        print("8) Reporte consolidado (matriz de viajes)")
        print("9) Cerrar sesion")
        try:
            opcion = input_int("Opcion: ")
            if opcion == 1:
                print("Cantidad de usuarios:", cantidad_usuarios())
                escribir_log(f"{usuario} consultó la cantidad de usuarios\n")
            elif opcion == 2:
                print("KM totales:", total_km_todos())
                escribir_log(f"{usuario} consultó la cantidad de kilometros totales\n")
            elif opcion == 3:
                top = top5_destinos()
                if not top:
                    print("Sin datos suficientes.")
                else:
                    print("Top 5 destinos:", top)
                    escribir_log(f"{usuario} consultó los top 5 destinos\n")
            elif opcion == 4:
                u, km = usuario_max_km()
                print("Usuario con mas KM:", u, "-", km, "KM")
                escribir_log(f"{usuario} consultó cual es el usuario con mas kilometros \n")
            elif opcion == 5:
                u, cant = usuario_max_destinos()
                print("Usuario con mas destinos:", u, "-", cant, "destinos")
                escribir_log(f"{usuario} consultó cual es el usuario con mas kilometros \n")
            elif opcion == 6:
                print("Usuario a simular menu:")
                usuario_a_impersonar = input("> ")
                if (usuario_existe(usuario_a_impersonar)):
                    escribir_log(f"{usuario} impersonó a {usuario_a_impersonar} \n")
                    menu_usuario(leer_datos(usuario_a_impersonar)[1], usuario_a_impersonar)
                else:
                    print("Usuario no encontrado.")
            elif opcion == 7:
                try:
                    print("Ingrese el nuevo usuario")
                    cambiar_contrasena(normalizar(input("> ")))
                    escribir_log(f"{usuario} inició un cambio de contraseña \n")
                except AuthError as mensaje_error:
                    print(mensaje_error)
                    escribir_log(f"{usuario} error de cambio de contraseña \n")
            elif opcion == 8:
                reporte_consolidado()
                escribir_log(f"{usuario} consultó el reporte consolidado \n")
            elif opcion == 9:
                print("Cerrando sesion...")
            else:
                raise MenuOptionError("Opcion invalida.")
        except MenuOptionError as mensaje_error:
            print(mensaje_error)
            escribir_log(f"{usuario} Error de menú \n")


def escribir_log(cadena):
    '''Escribe la cadena'''
    with open("logs.txt", mode="a", encoding="utf-8") as archivo_log:
        archivo_log.write(cadena +"\n")



def usuario_existe(usuario_a_chequear):
    '''Devuelve True si existe de lo contrario False'''
    with open("usuarios.txt", mode="r", encoding="utf-8") as archivo_usuarios:

        linea_leida = archivo_usuarios.readline()
        usuario_encontrado = False

        while(linea_leida != ""):
            usuario_leido, contrasena, tipo = linea_leida.split(";")

            if (usuario_a_chequear == usuario_leido):
                usuario_encontrado = True
                break
            linea_leida = archivo_usuarios.readline()

        return usuario_encontrado




def leer_datos(usuario_a_leer, archivo=DATA_FILE):
    '''Busca al usuario y trae la info de viajes retorna -1 si hay un error, 0 si no lo encuentra y 1 si encuentra
    Estructura: Daniel;["CABA", "Rosario", "La Plata"] '''
    resultado = 1
    datos_final=[]
    try:
        with open(archivo, "r", encoding="utf-8") as archivo_viajes:
            usuario_leido = ""
            datos_leidos = ""
            linea_leida = archivo_viajes.readline()
            while linea_leida != "":
                try:
                    usuario_leido, datos_leidos = linea_leida.split(";")
                except ValueError:
                    print("error de Parseo")
                    resultado = -1
                    linea_leida= ""
                else:
                    if usuario_leido.lower() == usuario_a_leer.lower():
                        try:
                            datos_final = json.loads(datos_leidos)
                        except ValueError:
                            print("Error de parseo lista")
                            resultado = -1
                            datos_leidos = ""
                            break
                linea_leida = archivo_viajes.readline()
            else:
                datos_leidos = ""
                resultado = 0
    except OSError:
        resultado = -1
        datos_leidos = ""
        print("Error de archivo")
    return resultado, datos_final


def escribir_datos(usuario_a_escribir, datos_a_escribir, nombre_archivo_principal=DATA_FILE, nombre_archivo_temporal=TEMP_DATA_FILE, escribir_viajes = True, tipo=1): #Validado
    '''Escribe un archivo .txt temporal con los nuevos datos, si no encuentra al usuario lo agrega al final
    La estructura es usuario;[destino 1, destino2, destino3]   Retorna -1 si falla o 1 si escribe'''
    resultado = 1
    usuario_encontrado = False
    sin_datos = True if datos_a_escribir == [] else False
    try:
        with open (nombre_archivo_principal, mode="r", encoding="utf-8") as archivo_principal, open (nombre_archivo_temporal, mode="w", encoding="utf-8") as archivo_temporal:
            cant_lineas = sum(1 for _ in archivo_principal)
            archivo_principal.seek(0)
            i = 0
            linea_leida = archivo_principal.readline()
            if linea_leida == "":
                if not sin_datos:
                    archivo_temporal.write(usuario_a_escribir + ";" + json.dumps(datos_a_escribir)) if escribir_viajes else archivo_temporal.write(usuario_a_escribir + ";" + invertir_chars(str(datos_a_escribir)) + ";" + str(tipo))#Si el archivo está vacío
                usuario_encontrado = True
            while linea_leida != "":
                i+=1
                try:
                    usuario_leido = linea_leida.split(";")[0]
                except ValueError:
                    print("Error parseando archivo")
                    resultado = -1
                    linea_leida= ""
                else:
                    if usuario_leido != usuario_a_escribir:
                        archivo_temporal.write(linea_leida)
                    else: 
                        if not sin_datos:        
                            if cant_lineas != i:
                                archivo_temporal.write(usuario_a_escribir + ";" + json.dumps(datos_a_escribir) + "\n") if escribir_viajes else archivo_temporal.write(usuario_a_escribir + ";" + invertir_chars(str(datos_a_escribir)) + ";" + str(tipo) + "\n")
                            else:
                                archivo_temporal.write(usuario_a_escribir + ";" + json.dumps(datos_a_escribir)) if escribir_viajes else archivo_temporal.write(usuario_a_escribir + ";" + invertir_chars(str(datos_a_escribir)) + ";" + str(tipo))
                        usuario_encontrado = True
                linea_leida = archivo_principal.readline()
            if usuario_encontrado == False and resultado == 1 and not sin_datos:
                archivo_temporal.write("\n" + usuario_a_escribir + ";" + json.dumps(datos_a_escribir)) if escribir_viajes else archivo_temporal.write("\n" + usuario_a_escribir + ";" + invertir_chars(str(datos_a_escribir)) + ";" + str(tipo))
    except OSError:
        resultado = -1
        print("Error abriendo el archivo")
    if resultado == 1:
        os.replace(nombre_archivo_temporal, nombre_archivo_principal)
    return resultado


def cantidad_usuarios():
    '''Devuelve la cantidad de Usuarios'''
    cant_lineas = 0
    with open("usuarios.txt", mode="r", encoding="utf-8") as archivo_usuarios:
        linea_leida = archivo_usuarios.readline()
        while(linea_leida != ""):
            cant_lineas += 1
            linea_leida = archivo_usuarios.readline()
    return cant_lineas

def get_usuario_por_numero(numero):
    '''La primera linea es la numero 0 devuelve el usuario en esa posición'''
    if numero < 0:
        return "-1"
    with open("usuarios.txt", mode="r", encoding="utf-8") as archivo_usuarios:
        usuario = ""
        for _ in range(numero+1):
            linea_leida = archivo_usuarios.readline()
            if linea_leida == "":
                usuario = "-1"
                break
            try:
                usuario = linea_leida.split(";")[0]
            except ValueError:
                usuario = "-1"
                break
        return usuario



def reporte_consolidado():
    '''Imprime los viajes de todos los usuarios'''
    print("\n=== REPORTE CONSOLIDADO DE VIAJES (MATRIZ) ===")
    print("Usuario  |   [ Vuelos ]")
    usuario = ""
    i=0
    usuario = get_usuario_por_numero(i)
    while usuario != "-1":
            i += 1
            print(f"{usuario}  {leer_datos(usuario)[1]}")
            usuario = get_usuario_por_numero(i)


def cambiar_contrasena(usuario):
    '''Cambia la contraseña y el tipo, si no encuentra el usuario lo agrega'''

    print("Cambio de contrasena, si no existe el usuario se agrega")
    print("Contrasena:")
    nueva_contrasena = normalizar(input("> "))

    print("Tipo (1 si es usuario normal, 2 si es admin):")
    tipo = normalizar(input("> "))

    if escribir_datos(usuario, nueva_contrasena, USER_FILE, TEMP_DATA_FILE, False, tipo) == 1:
        print("Contrasena cambiada.")
    else:
        print("Error en el cambio de contraseña")


def invertir_chars(cadena):
    '''Invierte los chars A->Z a->Z 1->0'''
    mayusculas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    minusculas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numeros = ['1','2','3','4','5','6','7','8','9','0']
    nueva_cadena = ""
    for character in cadena:
        if character.isdigit():
            indice = numeros.index(character)
            nueva_cadena += numeros[(-1)*indice]
        elif character.isupper():
            indice = mayusculas.index(character)
            nueva_cadena += minusculas[(-1)*indice]
        elif character.islower():
            indice = minusculas.index(character)
            nueva_cadena += mayusculas[(-1)*indice]
    return nueva_cadena