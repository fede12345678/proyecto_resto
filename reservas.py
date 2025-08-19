#gestion de reservas
import flet as ft
import datetime
import calendar
import pytz

def main(page: ft.Page, nombre_usuario="Usuario"):
    meses_es = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    bordo = "#800000"
    fuente = "Arial"
    # Dialogo de confirmación de reserva
    def cerrar_dialogo_ok(e):
        dialogo_ok.open = False
        page.update()
    dialogo_ok = ft.AlertDialog(
        modal=True,
        title=ft.Text("Reserva confirmada", weight="bold", color=bordo, font_family=fuente),
        content=ft.Text("¡Reserva realizada correctamente! Lo esperamos en Kansas Grill.", font_family=fuente),
        actions=[ft.ElevatedButton("OK", on_click=cerrar_dialogo_ok, style=ft.ButtonStyle(bgcolor=bordo, color="white"))],
        actions_alignment="center",
        icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=bordo, size=40),
    )
    page.bgcolor = "white"
    # Campo para ingresar el nombre de la persona que reserva
    nombre_reserva = ft.TextField(label="Nombre de quien reserva", value=nombre_usuario, width=220, color=bordo)
    page.title = "Calendario de Reservas"

    # Obtener fecha actual en horario de Argentina
    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    hoy = datetime.datetime.now(tz).date()
    year = hoy.year
    month = hoy.month

    # mensaje eliminado, solo se usará el dialogo_ok
    # Dialogo de advertencia
    def cerrar_dialogo(e):
        dialogo_warning.open = False
        page.update()
    dialogo_warning = ft.AlertDialog(
        modal=True,
        title=ft.Text("Error de reserva", weight="bold", color=bordo, font_family=fuente),
        content=ft.Text("Faltan completar campos para terminar la reserva.", font_family=fuente),
        actions=[ft.ElevatedButton("OK", on_click=cerrar_dialogo, style=ft.ButtonStyle(bgcolor=bordo, color="white"))],
        actions_alignment="center",
        icon=ft.Icon(ft.Icons.ERROR, color=bordo, size=40),
    )
    grid = ft.Column()
    seleccionado = {"dia": None}
    intento_reserva = {"valor": False}

    cantidad_personas = ft.Dropdown(
        label="Cantidad de personas",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 11)],
        width=180,
        color=bordo,
        border_color=bordo
    )

    horario_reserva = ft.Dropdown(
        label="Horario",
        options=[ft.dropdown.Option(h) for h in ["19:00", "20:00", "21:00", "22:00"]],
        width=180,
        color=bordo,
        border_color=bordo
    )

    def actualizar_calendario():
        _, last_day = calendar.monthrange(year, month)
        first_weekday = calendar.monthrange(year, month)[0]  # 0=Monday

        dias = []
        fila = []
        for _ in range(first_weekday):
            fila.append(ft.Container(width=80, height=60))
        for dia in range(1, last_day + 1):
            def crear_on_click(d):
                return lambda e: seleccionar_dia(d)
            def hover_anim(e):
                e.control.scale = 1.10 if e.data == "true" else 1
                e.control.update()
            style = ft.ButtonStyle(
                text_style=ft.TextStyle(size=24),
                bgcolor=bordo,
                color="white",
                animation_duration=150
            )
            if intento_reserva["valor"] and seleccionado["dia"] is None:
                style.shape = ft.RoundedRectangleBorder(radius=6)
            if seleccionado["dia"] == dia:
                style.bgcolor = "#4B0010"  # Un bordo más oscuro para el seleccionado
                style.color = "white"
            btn = ft.ElevatedButton(
                str(dia),
                width=80,
                height=60,
                style=style,
                on_click=crear_on_click(dia),
                on_hover=hover_anim
            )
            fila.append(btn)
            if len(fila) == 7:
                dias.append(ft.Row(fila, spacing=10))
                fila = []
        if fila:
            dias.append(ft.Row(fila, spacing=10))
        encabezado = ft.Row(
            [ft.Text(d, width=80, weight="bold", size=20, text_align="center", color=bordo, font_family=fuente) for d in ["LU", "MA", "MI", "JU", "VI", "SA", "DO"]],
            spacing=10
        )
        grid.controls = [
            ft.Text(f"{meses_es[month]} {year}", size=32, weight="bold", width=600, text_align="center", color=bordo, font_family=fuente),
            encabezado
        ] + dias
        page.update()

    def reservar(e):
        intento_reserva["valor"] = True
        campos_ok = True

        cantidad_personas.border_color = None
        horario_reserva.border_color = None

        if seleccionado["dia"] is None:
            campos_ok = False
        if not cantidad_personas.value:
            cantidad_personas.border_color = "red"
            campos_ok = False
        if not horario_reserva.value:
            horario_reserva.border_color = "red"
            campos_ok = False

        if campos_ok:
            nombre_final = nombre_reserva.value.strip() or nombre_usuario
            with open("reservas.txt", "a", encoding="utf-8") as f:
                f.write(f"{nombre_final},{seleccionado['dia']}/{month}/{year},{cantidad_personas.value} personas, {horario_reserva.value}\n")
            # Mostrar dialogo de confirmación
            page.dialog = dialogo_ok
            dialogo_ok.open = True
            page.update()
            return
        else:
            campos_faltantes = []
            if seleccionado["dia"] is None:
                campos_faltantes.append("día")
            if not cantidad_personas.value:
                campos_faltantes.append("cantidad de personas")
            if not horario_reserva.value:
                campos_faltantes.append("horario")
            dialogo_warning.content.value = f"Faltan completar los siguientes campos: {', '.join(campos_faltantes)}."
            page.dialog = dialogo_warning
            dialogo_warning.open = True
            page.update()
            return
        actualizar_calendario()
        page.update()

    def personas_o_horario_change(e):
        if cantidad_personas.value:
            cantidad_personas.border_color = None
        if horario_reserva.value:
            horario_reserva.border_color = None
        page.update()

    cantidad_personas.on_change = personas_o_horario_change
    horario_reserva.on_change = personas_o_horario_change

    def seleccionar_dia(dia):
        seleccionado["dia"] = dia
        actualizar_calendario()

    reservar_btn = ft.ElevatedButton(
        "Reservar",
        on_click=reservar,
        width=180,
        style=ft.ButtonStyle(bgcolor=bordo, color="white")
    )

    # Calendario a la izquierda, listas y botón a la derecha
    page.add(
        ft.Column([
            ft.Image(src="fotos_a_utilizar/kansasgrill.jpg", width=340, height=110, fit=ft.ImageFit.CONTAIN),
            ft.Container(
                ft.Row(
                    [
                        grid,
                        ft.VerticalDivider(width=30),
                        ft.Column(
                            [nombre_reserva, cantidad_personas, horario_reserva, reservar_btn],
                            alignment="start",
                            horizontal_alignment="center",
                            spacing=18
                        ),
                    ],
                    alignment="center",
                    vertical_alignment="start",
                    spacing=30
                ),
                padding=ft.padding.only(top=30)
            ),
            # mensaje eliminado, solo se usará el dialogo_ok
            dialogo_warning,
            dialogo_ok,
        ], horizontal_alignment="center", spacing=10)
    )
    actualizar_calendario()


ft.app(main)