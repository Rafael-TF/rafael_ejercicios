import os
import csv
from usuario import Usuario
from datetime import datetime

# Ruta del archivo CSV
CSV_FILE = "archivos_csv/usuarios.csv"

# Verificar si la carpeta existe y, si no, crearla
def asegurarse_carpeta_existe():
    if not os.path.exists('archivos_csv'):
        os.makedirs('archivos_csv')
        print("Carpeta 'archivos_csv' creada.")


# Lista de usuarios predefinidos
usuarios = [
    Usuario("Ana López", "ana.lopez@email.com", 25, 1.68, True, "10/04/1998"),
    Usuario("Carlos Gómez", "carlos.gomez@email.com", 34, 1.82, False, "22/01/1989"),
    Usuario("María Pérez", "maria.perez@email.com", 29, 1.60, True, "15/07/1994"),
    Usuario("Luis Rodríguez", "luis.rodriguez@email.com", 40, 1.75, False, "05/12/1983")
]

#-------------------------------------------------------------------------------------------------------
#-------------------------------------- Cargar Usuarios del CSV -----------------------------------------
#-------------------------------------------------------------------------------------------------------

# Cargar usuarios desde un archivo CSV al inicio del programa
def cargar_usuarios_csv():
    try:
        """He usado csv.DictReader ya que según he leido se emplea para leer archivos CSV y convertir cada fila en un diccionario,
           donde las claves del diccionario corresponden a los nombres de las columnas definidos en la primera fila del archivo (cabecera). 
           newline="": Asegura que las líneas del archivo se escriban correctamente en todos los sistemas operativos.
           Fuente --> https://docs.python.org/3/library/csv.html#csv.DictReader
        """
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo) 
            for fila in lector:
                # Creamos los objetos Usuario desde las filas del CSV
                usuario = Usuario(
                    nombre=fila["nombre"],
                    email=fila["email"],
                    edad=int(fila["edad"]),
                    altura=float(fila["altura"]),
                    estudiante=fila["estudiante"].lower() == "true",
                    birthday=fila["birthday"]
                )
                
                # Introducimos los usuarios
                usuarios.append(usuario)
                
    except FileNotFoundError:
         # Si el archivo no existe, lo creamos automáticamente
        print(f"El archivo {CSV_FILE} no existe. Se creará uno nuevo al guardar.")
        # Aquí se crear el archivo vacío inicialmente si es necesario.
        guardar_usuarios_csv()
    except Exception as e:
        print(f"Error al cargar usuarios desde el CSV: {e}")
        
#-------------------------------------------------------------------------------------------------------
#-------------------------------------- Guardar Usuarios en el CSV --------------------------------------
#-------------------------------------------------------------------------------------------------------

# Guardar usuarios en un archivo CSV tras cada cambio en la lista
def guardar_usuarios_csv():
    try:
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as archivo:
            campos = ["nombre", "email", "edad", "altura", "estudiante", "birthday"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            # Se escribe la primera línea del archivo CSV, que contiene los nombres de las columnas (nombre, email, edad, altura, estudiante, birthday).
            escritor.writeheader()

            # Escribir usuarios como filas
            for usuario in usuarios:
                escritor.writerow({
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "edad": usuario.edad,
                    "altura": usuario.altura,
                    "estudiante": str(usuario.estudiante).lower(),
                    "birthday": usuario.birthday
                })
    except Exception as e:
        print(f"Error al guardar usuarios en el CSV: {e}")

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------OPCION 1----------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# Imprimir todos los usuarios de la lista
def print_user():
    try:
        if not usuarios:
            print("No hay usuarios en la base de datos.")
            return
        
        for usuario in usuarios:
            print(usuario)
            
    except ValueError as e:
        print(f"Error: {e}") # Con este capturamos los errores esperados como que no haya usuarios.
    except Exception as e:  # Este lo he implementado para capturar cualquier otra excepción inesperada.
        print(f"Ocurrió un error inesperado: {e}")
 
 #-------------------------------------------------------------------------------------------------------       
 #-------------------------------------------OPCION 2----------------------------------------------------
 #-------------------------------------------------------------------------------------------------------
 
 #Imprimir todos los usuarios ordenados por edad descendente. Opcional: pedir por input si quiere ascendente o descendente       
def print_user_sorted_by_edad():
    
    if not usuarios:  # Verificamos si la lista está vacía
        print("No hay usuarios en la base de datos.")
        return

    """Aquí he usado un while True ya que como he decidido introducir las opciones para que el usuario decida el orden,
       con esto lo que hacemos es asegurarnos de que el programa siga solicitando la entrada del usuario hasta que este 
       ingrese una opción válida, es decir, 1 o 2."""
       
    while True:
        try:
            # Solicitamos al usuario su preferencia de orden
            orden = input("¿Cómo deseas ordenar los usuarios por edad?\n"
                          "1 - Ascendente (de menor a mayor)\n"
                          "2 - Descendente (de mayor a menor)\n"
                          "Introduce el número de tu elección: ").strip()

            if orden not in ['1', '2']:
                print("Opción inválida. Por favor, elige 1 o 2.")

            # Ordenar en orden ascendente
            if orden == '1':
                print("\nUsuarios ordenados por edad (ascendente):")
                usuarios_ordenados = sorted(usuarios, key=lambda u: u.edad)
                for usuario in usuarios_ordenados:
                    print(usuario)

            # Ordenar en orden descendente
            elif orden == '2':
                print("\nUsuarios ordenados por edad (descendente):")
                usuarios_ordenados = sorted(usuarios, key=lambda u: u.edad, reverse=True)
                for usuario in usuarios_ordenados:
                    print(usuario)

            break  # Salir del bucle si todo salió bien

        except ValueError as e:
            print(f"Error: {e}. Inténtalo de nuevo.\n")

        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}. Inténtalo de nuevo.\n")
            
#-------------------------------------------------------------------------------------------------------       
#-------------------------------------------OPCION 3----------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# Imprimir un usuario por su email            
def print_user_by_email():
    
    if not usuarios:
        print("No hay usuarios en la base de datos.")
        return

    try:
        email = input("Introduce el email del usuario que quieres ver: ").strip() # El .strip() lo he puesto para evitar espacios en blanco
        
        if not email: 
            raise ValueError("El email no puede estar vacío.")
        
        for usuario in usuarios:
            if usuario.email.lower() == email.lower():
                print("\nUsuario encontrado:")
                print(usuario)
                return

        print(f"No se encontró ningún usuario con el email: {email}.")
    
    except ValueError as e:
        print(f"Error: {e}") 
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
        
#-------------------------------------------------------------------------------------------------------       
#-------------------------------------------OPCION 4----------------------------------------------------
#-------------------------------------------------------------------------------------------------------


# Crear un nuevo usuario
def create_usuario():
    try:
        nombre = input("Introduce el nombre: ").strip()
        email = input("Introduce el email: ").strip()
        edad = int(input("Introduce la edad: "))
        altura = float(input("Introduce la altura (en metros): "))
        estudiante = input("¿Es estudiante? (s/n): ").strip().lower() == 's'

        """Para introducir la fecha a través de los tres input he vuelto a usar el while True al igual que lo hice
           para la opción 2 a la hora de solicitarle al usuario que introduzca si prefiere en ascendente o descendente.
           En este caso como se le tiene que solicitar 3 datos relativos a la fecha de nacimiento lo he puesto así ya que
           considero que está mejor controlado y hace que la función quede mucho más robusta"""
           
        while True:
            try:
                dia = int(input("Introduce el día de nacimiento (1-31): "))
                mes = int(input("Introduce el mes de nacimiento (1-12): "))
                año = int(input("Introduce el año de nacimiento (YYYY): "))

                # Creamos la fecha con datetime para validarla
                fecha_nacimiento = datetime(year=año, month=mes, day=dia)
                # Estuve mirando cómo se puede formatear la fecha a DD-MM-YYYY. Fuente --> https://www.progress.com/es/blogs/formato-de-fecha-en-python
                birthday = fecha_nacimiento.strftime("%d/%m/%Y")
                break
            except ValueError:
                print("Fecha inválida. Asegúrate de introducir valores correctos para día, mes y año.")

        # Primero creamos el objeto Usuario
        nuevo_usuario = Usuario(nombre, email, edad, altura, estudiante, birthday)
        # Posteriormente lo que hacemos es agregar ese ususario nuevo a la lista
        usuarios.append(nuevo_usuario)
        
        # Se guardan los cambios en el CSV una vez se se haya creado y agregado el usuario en la lista
        guardar_usuarios_csv()
        print("Usuario creado y guardado correctamente.")
        
    except ValueError:
        print("Error: Verifica los datos ingresados. Edad debe ser un número entero y altura un decimal.")
    except Exception as e:
        print(f"Error inesperado al crear el usuario: {e}")
        
#-------------------------------------------------------------------------------------------------------       
#-------------------------------------------OPCION 5----------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# Actualizar un usuario
def update_usuario():
    try:
        if not usuarios:
            print("No hay usuarios en la base de datos.")
            return
        
        email = input("Introduce el email del usuario que deseas actualizar: ").strip()
        
        # Se busca el usuario en la lista
        usuario_encontrado = None
        for usuario in usuarios:
            if usuario.email.lower() == email.lower():
                usuario_encontrado = usuario
                break
        
        if not usuario_encontrado:
            print("Usuario no encontrado.")
            return
        
        print(f"Usuario encontrado: {usuario_encontrado}")
        
        """Con esto lo que pretendo hacer es que el usuario modifique aquellos datos que quiera.
           A través del while True controlamos todas las opciones"""
           
        while True:
            print("\n¿Qué deseas actualizar?")
            print("1. Nombre")
            print("2. Edad")
            print("3. Altura")
            print("4. ¿Es estudiante?")
            print("5. Cumpleaños")
            print("6. Finalizar cambios")
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == "1":
                nuevo_nombre = input("Introduce el nuevo nombre: ").strip()
                usuario_encontrado.nombre = nuevo_nombre
                print("Nombre actualizado.")
            elif opcion == "2":
                try:
                    nueva_edad = int(input("Introduce la nueva edad: "))
                    usuario_encontrado.edad = nueva_edad
                    print("Edad actualizada.")
                except ValueError:
                    print("Edad inválida. Debe ser un número entero.")
            elif opcion == "3":
                try:
                    nueva_altura = float(input("Introduce la nueva altura (en metros): "))
                    usuario_encontrado.altura = nueva_altura
                    print("Altura actualizada.")
                except ValueError:
                    print("Altura inválida. Debe ser un número decimal.")
            elif opcion == "4":
                es_estudiante = input("¿Es estudiante? (s/n): ").strip().lower()
                if es_estudiante in ['s', 'n']:
                    usuario_encontrado.estudiante = es_estudiante == 's'
                    print("Estado de estudiante actualizado.")
                else:
                    print("Opción inválida. Introduce 's' o 'n'.")
            elif opcion == "5":
                # Validar y actualizar la fecha de cumpleaños
                while True:
                    try:
                        dia = int(input("Introduce el día de nacimiento (1-31): "))
                        mes = int(input("Introduce el mes de nacimiento (1-12): "))
                        año = int(input("Introduce el año de nacimiento (YYYY): "))
                        fecha_nacimiento = datetime(year=año, month=mes, day=dia)
                        usuario_encontrado.birthday = fecha_nacimiento.strftime("%d-%m-%Y")
                        print("Fecha de nacimiento actualizada.")
                        break
                    except ValueError:
                        print("Fecha inválida. Asegúrate de introducir valores correctos para día, mes y año.")
            elif opcion == "6":
                print("Finalizando cambios...")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
        
        # Guardamos los cambios en el CSV
        guardar_usuarios_csv()
        print("Usuario actualizado correctamente.")
        print(usuario_encontrado)
        
    except ValueError:
        print("Error: Introduce datos válidos.")
    except Exception as e:
        print(f"Error inesperado al actualizar el usuario: {e}")
        
#-------------------------------------------------------------------------------------------------------       
#-------------------------------------------OPCION 6----------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# Boerrar un usuario de la lista
def delete_user():
    try:
        if not usuarios:
            print("No hay usuarios en la base de datos.")
            return
        
        email = input("Introduce el email del usuario que deseas borrar: ").strip()
        
       
        for index, usuario in enumerate(usuarios):
            if usuario.email.lower() == email.lower():
                del usuarios[index]
                # Guardamos cambios en el CSV una vez se ha eliminado el usuario
                guardar_usuarios_csv()
                print(f"Usuario con email '{email}' eliminado correctamente.")
            else:
                print("Usuario no encontrado")
        
    except Exception as e:
        print(f"Error inesperado al intentar borrar el usuario: {e}")
            
#-------------------------------------------------------------------------------------------------------       
#-------------------------------------------OPCION 7----------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# Borrar todos los usuarios
def delete_users():
    try:
        if not usuarios:
            print("No hay usuarios en la base de datos.")
            return

        """Aqui al ser una opción en la que se borran todos los usuarios he querido controlar la acción
           pidiendo al usuario que confirme el borrado de los datos"""
           
        confirmation = input("¿Estás seguro de que deseas borrar todos los usuarios? (s/n): ").strip().lower()
        
        if confirmation == 's':
            print("Borrando lista de usuarios...")
            usuarios.clear()
            guardar_usuarios_csv()  # Guardamos después de limpiar la lista
            print("Todos los usuarios han sido eliminados con éxito.")
        else:
            print("Operación cancelada.")
            
    except Exception as e:
        print(f"Error inesperado al intentar borrar los usuarios: {e}")