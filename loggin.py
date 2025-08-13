
# Sistema de login para reservas de restaurante
# Separado para administradores y usuarios
import getpass


# Archivo donde se guardan los usuarios
USUARIOS_FILE = "usuarios.txt"

def cargar_usuarios():
    usuarios = {}
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 5:
                    nombre, dni, username, password, rol = partes
                    usuarios[username] = {"nombre": nombre, "dni": dni, "password": password, "rol": rol}
                elif len(partes) == 3:
                    # Para compatibilidad con versiones anteriores
                    username, password, rol = partes
                    usuarios[username] = {"nombre": "", "dni": "", "password": password, "rol": rol}
    except FileNotFoundError:
        # Si no existe, crear algunos por defecto
        usuarios = {
            'admin': {'nombre': 'Administrador', 'dni': '00000000', 'password': 'admin123', 'rol': 'admin'},
            'usuario1': {'nombre': 'Usuario Uno', 'dni': '11111111', 'password': 'user123', 'rol': 'usuario'},
            'usuario2': {'nombre': 'Usuario Dos', 'dni': '22222222', 'password': 'user456', 'rol': 'usuario'}
        }
        guardar_usuarios(usuarios)
    return usuarios

def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        for username, data in usuarios.items():
            f.write(f"{data.get('nombre','')},{data.get('dni','')},{username},{data['password']},{data['rol']}\n")

USUARIOS = cargar_usuarios()


def login():
    print("=== Sistema de Login ===")
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    user = USUARIOS.get(username)
    if user and user['password'] == password:
        nombre = user.get('nombre', username)
        print(f"Bienvenido, {nombre}!")
        return user['rol']
    else:
        print("Usuario o contraseña incorrectos.")
        return None

def crear_usuario():
    print("=== Crear nuevo usuario ===")
    nombre = input("Nombre completo: ")
    dni = input("DNI: ")
    while True:
        username = input("Nombre de usuario: ")
        if username in USUARIOS:
            print("Ese usuario ya existe. Intente con otro nombre.")
        else:
            break
    password = getpass.getpass("Contraseña: ")
    while True:
        rol = input("Rol (admin/usuario): ").strip().lower()
        if rol in ["admin", "usuario"]:
            break
        else:
            print("Rol inválido. Debe ser 'admin' o 'usuario'.")
    USUARIOS[username] = {"nombre": nombre, "dni": dni, "password": password, "rol": rol}
    guardar_usuarios(USUARIOS)
    print(f"Usuario '{username}' creado exitosamente con rol '{rol}'.")


if __name__ == "__main__":
    while True:
        print("\n1. Iniciar sesión")
        print("2. Crear nuevo usuario")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            rol = None
            while not rol:
                rol = login()
            # Aquí puedes continuar con el menú según el rol, pero no mostrar el rol al usuario
        elif opcion == "2":
            crear_usuario()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")
