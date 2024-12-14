import usuario_crud as crud

# Llamar a esta función antes de guardar o cargar el archivo CSV
crud.asegurarse_carpeta_existe()

# Cargamos los usuarios desde el archivo CSV al inicio
crud.cargar_usuarios_csv()

menu = """Te damos la bienvenida a la app de usuarios, estas son las opciones:
          1 - Ver todos los usuarios
          2 - Ver todos los usuarios ordenados por edad
          3 - Buscar un usuario por nombre
          4 - Crear nuevo usuario
          5 - Actualizar usuario existente
          6 - Borrar un usuario por email
          7 - Borrar todos los usuarios
          8 - Salir
          """
          
while True:
    option = int(input(menu))
    match option:
        case 1:
            crud.print_user()
        case 2:
            crud.print_user_sorted_by_edad()
        case 3:
            crud.print_user_by_email()
        case 4:
            crud.create_usuario()
        case 5:
            crud.update_usuario()
        case 6:
            crud.delete_user()
        case 7:
            crud.delete_users()
        case 8:
            print("Hasta pronto.")
            break
        case _:
            print("Opción incorrecta")