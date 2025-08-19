import flet as ft

# Datos del restaurante
DESCRIPCION = (
    "Kansas es un restaurante de Contemporary American Cuisine, inaugurado en junio de 1999 en San Isidro. "
    "Nuestra visión es ofrecer alimentos de calidad en un ambiente placentero con un servicio excelente. "
    "Creemos que la base de un buen plato está en la calidad de los ingredientes, por lo que usamos los mejores productos frescos. "
    "Además, consideramos la música, la arquitectura y la decoración esenciales para la experiencia gastronómica. "
    "Cada local tiene su propio carácter, con especial atención a los materiales y diseño. "
    "Nos esforzamos por satisfacer la confianza de nuestros clientes, brindando un servicio rápido y eficiente que supere todas las expectativas."
)
DIRECCION = "Ruta Panamericana Km. 43,5, y las Amapolas, Pilar, Provincia de Buenos Aires"
HORARIOS = "11:45am hasta 23:00pm"
FOTOS_LOCAL = ["fotos_a_utilizar/local_pilar.jpg", "fotos_a_utilizar/local_adentro.jpg", "fotos_a_utilizar/plato.jpg"]
FOTOS_MENU = ["fotos_a_utilizar/qr.jpg"]

# Reseñas iniciales
reseñas = [
    {"nombre": "Juan", "estrellas": 5, "texto": "Excelente comida y atención."},
    {"nombre": "Ana", "estrellas": 4, "texto": "Muy buen ambiente, volveré pronto."},
]

def main(page: ft.Page):
    page.title = "Detalles del Restaurante"
    page.window_width = 700
    page.window_height = 900

    reseña_nombre = ft.TextField(label="Tu nombre", width=200)
    reseña_estrellas_valor = 5
    reseña_estrellas_row = ft.Row([])
    reseña_texto = ft.TextField(label="Tu reseña", multiline=True, width=400)
    reseña_mensaje = ft.Text(value="", color="red")
    reseñas_column = ft.Column([])

    def actualizar_estrellas(valor):
        nonlocal reseña_estrellas_valor
        reseña_estrellas_valor = valor
        reseña_estrellas_row.controls.clear()
        for i in range(1, 6):
            reseña_estrellas_row.controls.append(
                ft.IconButton(
                    icon=ft.Icons.STAR if i <= valor else ft.Icons.STAR_BORDER,
                    icon_color="#800000",
                    on_click=lambda e, v=i: actualizar_estrellas(v),
                    style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=0)})
                )
            )
        page.update()

    def mostrar_reseñas():
        reseñas_column.controls.clear()
        bordo = "#800000"
        for r in reseñas:
            reseñas_column.controls.append(
                ft.Container(
                    ft.Column([
                        ft.Row([
                            ft.Text(r["nombre"], weight="bold"),
                            ft.Row([
                                *[ft.Icon(ft.Icons.STAR, color=bordo) for _ in range(r["estrellas"])],
                                *[ft.Icon(ft.Icons.STAR_BORDER, color=bordo) for _ in range(5 - r["estrellas"])],
                            ]),
                        ], alignment="spaceBetween"),
                        ft.Text(r["texto"])
                    ]),
                    bgcolor="#f8f8f8", border_radius=8, padding=10, margin=5
                )
            )
        page.update()

    def agregar_reseña(e):
        nombre = reseña_nombre.value.strip() or "Anónimo"
        estrellas = reseña_estrellas_valor
        texto = reseña_texto.value.strip()
        if not texto:
            reseña_mensaje.value = "Por favor, escribe una reseña."
            page.update()
            return
        reseñas.append({"nombre": nombre, "estrellas": estrellas, "texto": texto})
        reseña_nombre.value = ""
        actualizar_estrellas(5)
        reseña_texto.value = ""
        reseña_mensaje.value = "¡Gracias por tu reseña!"
        mostrar_reseñas()
        page.update()

    actualizar_estrellas(5)
    mostrar_reseñas()

    bordo = "#800000"
    page.add(
        ft.Column([
            ft.Text("Kansas Grill - Pilar", size=32, weight="bold", color=bordo),
            ft.Text(DESCRIPCION, size=16, selectable=True),
            ft.Divider(),
            ft.Text(f"Dirección: {DIRECCION}", size=14, weight="bold", color=bordo),
            ft.Text(f"Horarios: {HORARIOS}", size=14, weight="bold", color=bordo),
            ft.Divider(),
            ft.Text("Fotos del lugar", size=18, weight="bold", color=bordo),
            ft.Row([
                ft.Image(src=f, width=450, height=310, fit=ft.ImageFit.FILL) for f in FOTOS_LOCAL
            ], scroll="auto"),
            ft.Divider(),
            ft.Text("Menú", size=18, weight="bold", color=bordo),
            ft.Row([
                ft.Image(src=FOTOS_MENU[0], width=180, height=180, fit=ft.ImageFit.FILL),
                ft.Container(
                    ft.Text(
                        "Escaneando el código QR con su celular tendrá acceso a nuestro menú",
                        size=15,
                        color=bordo,
                        width=220,
                        selectable=True
                    ),
                    alignment=ft.alignment.center,
                    padding=10
                )
            ], alignment="center", spacing=20),
            ft.Divider(),
            ft.Text("Reseñas", size=18, weight="bold", color=bordo),
            reseñas_column,
            ft.Text("Deja tu reseña", size=19, weight="bold", color=bordo),
            ft.Row([
                reseña_nombre,
                reseña_estrellas_row
            ]),
            reseña_texto,
            ft.Row([
                ft.ElevatedButton("Enviar reseña", on_click=agregar_reseña, style=ft.ButtonStyle(bgcolor=bordo, color="white")),
                reseña_mensaje
            ]),
        ], scroll="auto", expand=True, horizontal_alignment="center", alignment="start", spacing=18)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
