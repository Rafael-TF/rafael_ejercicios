class Usuario:
    
    # Método constructor:
    def __init__(self, nombre, email, edad, altura, esudiante, birthday): # atributos de instancia
        self.nombre = nombre
        self.email = email
        self.edad = edad
        self.altura = altura
        self.estudiante = esudiante
        self.birthday = birthday
        print("Usuario creado correctamente")
        
    # Método para imprimir los usuarios
    def __str__(self):
        return (
            f"--- Información del Usuario ---\n"
            f"Nombre      : {self.nombre}\n"
            f"Email       : {self.email}\n"
            f"Edad        : {self.edad} años\n"
            f"Altura      : {self.altura} metros\n"
            f"Estudiante  : {self.estudiante}\n"
            f"Cumpleaños  : {self.birthday}\n"
            f"------------------------------"
        )