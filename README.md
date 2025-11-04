Aterrizar 

## Proyecto universitario utilizando Python 
## Objetivo: Simular un sistema de gestión de viajes que permita a los usuarios registrar y consultar itinerarios, y a los administradores obtener estadísticas globales.  
 Integrantes: - Tobias Larramendi 1143238       
              - Bichutte Mateo 1174425
              - Vazquez Daniel Andres 1220473
                

## Usuarios Validos 
  - Administrador
  - Usuario: `admin`
  - Contraseña: `admin`
  - Usuarios simulados
  - `user1` … `user5`
  - Contraseña: `1234`

## Funcionalidades

### Menú de Usuario
1. Registrar viaje 
2. Consultar viaje   
3. Consultar kilómetros del viaje 
4. Consultar cantidad de escalas 
5. Consultar provincias visitadas 
6. Eliminar viaje 
7. Cerrar sesión 

### Menú de Admin
1. Cantidad de usuarios  
2. Kilómetros totales (todos los usuarios) 
3. Top 5 destinos más visitados 
4. Usuario con más kilómetros recorridos 
5. Usuario con más destinos visitados 
6. Acceder al menú de un usuario 
7. Cambiar contraseña de usuario   
8. Cerrar sesión

##  Simulación de datos
- Se crean automáticamente 5 usuarios comunes más el administrador.  
- Los viajes se **simulan aleatoriamente** usando `random` para que los reportes muestren información sin necesidad de cargar manualmente.

### Destinos válidos
El sistema trabaja con un conjunto fijo de destinos, definidos en la lista `DESTINOS`:

- CABA  
- La Plata  
- Mar del Plata  
- Rosario  
- Córdoba  
- Mendoza  
- Salta  
- Bariloche  

Solo se aceptan estos destinos como **origen** o **destino**.  
Si se ingresa un valor diferente (ejemplo: `Paris`), el sistema mostrará un error `Destino no válido`.

### Pasos para registrar un viaje
1. Ingresar como usuario común (`user1` … `user5`, contraseña `1234`).  
2. Elegir la opción **1) Registrar viaje** en el menú.  
3. Ingresar un **origen** válido de la lista anterior.  
   - Para cancelar, escribir `fin`.  
4. Ingresar los **destinos** uno por uno.  
   - Finalizar escribiendo `fin`.  
   - Si se ingresa dos veces seguidas el mismo destino, se ignora el duplicado.  
5. El viaje queda registrado y puede consultarse en las demás opciones del menú.

---

