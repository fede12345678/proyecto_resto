
import flet as ft
import os

USUARIOS_FILE = "usuarios.txt"


# Ahora los usuarios se guardan como: nombre,dni,usuario,contrasena,rol
def verificar_usuario(usuario, contrasena):
    if not os.path.exists(USUARIOS_FILE):
        return False
    with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
        for linea in f:
            datos = linea.strip().split(",")
            if len(datos) == 5 and datos[2] == usuario and datos[3] == contrasena:
                return True
    return False

def crear_usuario(nombre, dni, usuario, contrasena):
    rol = "usuario"
    if not os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "w", encoding="utf-8"):
            pass
    with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
        for linea in f:
            datos = linea.strip().split(",")
            if len(datos) == 5 and datos[2] == usuario:
                return False  # Usuario ya existe
    with open(USUARIOS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{nombre},{dni},{usuario},{contrasena},{rol}\n")
    return True


def main(page: ft.Page):
    page.title = "Login y Registro"
    page.window_width = 400
    page.window_height = 400

    # --- Login widgets ---
    login_usuario = ft.TextField(label="Usuario", width=300)
    login_contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    login_mensaje = ft.Text(value="", color="red")

    # --- Registro widgets ---
    reg_nombre = ft.TextField(label="Nombre completo", width=300)
    reg_dni = ft.TextField(label="DNI", width=300)
    reg_usuario = ft.TextField(label="Usuario", width=300)
    reg_contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    reg_mensaje = ft.Text(value="", color="red")

    def mostrar_login():
        page.controls.clear()
        bordo = "#800000"
        def hover_anim(e):
            e.control.scale = 1.08 if e.data == "true" else 1
            e.control.update()
        page.add(
            ft.Row([
                ft.Column([
                    ft.Image(src="kansasgrill.jpg", width=180, height=120, fit=ft.ImageFit.CONTAIN),
                    login_usuario,
                    login_contrasena,
                    ft.Row([
                        ft.ElevatedButton(
                            "Iniciar sesión",
                            on_click=login_click,
                            style=ft.ButtonStyle(
                                bgcolor= bordo,
                                color="white",
                                animation_duration=200
                            ),
                            on_hover=hover_anim
                        ),
                        ft.ElevatedButton(
                            "Crear usuario",
                            on_click=lambda _: mostrar_registro(),
                            style=ft.ButtonStyle(
                                bgcolor= bordo,
                                color="white",
                                animation_duration=200
                            ),
                            on_hover=hover_anim
                        ),
                    ], alignment="center"),
                    login_mensaje
                ], alignment="center", horizontal_alignment="center", spacing=20)
            ], alignment="center", vertical_alignment="center", expand=True)
        )
        login_usuario.value = ""
        login_contrasena.value = ""
        login_mensaje.value = ""
        page.update()

    def mostrar_registro():
        page.controls.clear()
        bordo = "#800000"
        def hover_anim(e):
            e.control.scale = 1.08 if e.data == "true" else 1
            e.control.update()
        page.add(
            ft.Row([
                ft.Column([
                    ft.Image(src="kansasgrill.jpg", width=180, height=120, fit=ft.ImageFit.CONTAIN),
                    reg_nombre,
                    reg_dni,
                    reg_usuario,
                    reg_contrasena,
                    ft.Row([
                        ft.ElevatedButton(
                            "Registrar",
                            on_click=registrar_usuario,
                            style=ft.ButtonStyle(
                                bgcolor= bordo,
                                color="white",
                                animation_duration=200
                            ),
                            on_hover=hover_anim
                        ),
                        ft.ElevatedButton(
                            "Volver",
                            on_click=lambda _: mostrar_login(),
                            style=ft.ButtonStyle(
                                bgcolor= bordo,
                                color="white",
                                animation_duration=200
                            ),
                            on_hover=hover_anim
                        ),
                    ], alignment="center"),
                    reg_mensaje
                ], alignment="center", horizontal_alignment="center", spacing=20)
            ], alignment="center", vertical_alignment="center", expand=True)
        )
        reg_nombre.value = ""
        reg_dni.value = ""
        reg_usuario.value = ""
        reg_contrasena.value = ""
        reg_mensaje.value = ""
        page.update()

    def login_click(_):
        if verificar_usuario(login_usuario.value, login_contrasena.value):
            login_mensaje.value = "¡Login exitoso!"
            login_mensaje.color = "green"
        else:
            login_mensaje.value = "Usuario o contraseña incorrectos."
            login_mensaje.color = "red"
        page.update()

    def registrar_usuario(_):
        if not (reg_nombre.value and reg_dni.value and reg_usuario.value and reg_contrasena.value):
            reg_mensaje.value = "Completa todos los campos."
            reg_mensaje.color = "red"
        elif crear_usuario(reg_nombre.value, reg_dni.value, reg_usuario.value, reg_contrasena.value):
            reg_mensaje.value = "Usuario creado exitosamente."
            reg_mensaje.color = "green"
        else:
            reg_mensaje.value = "El usuario ya existe."
            reg_mensaje.color = "red"
        page.update()

    mostrar_login()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
