#gestion de reservas
import flet as ft
import datetime
import calendar
import pytz

def main(page: ft.Page):
    page.title = "Calendario de Reservas"

    # Obtener fecha actual en horario de Argentina
    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    hoy = datetime.datetime.now(tz).date()
    year = hoy.year
    month = hoy.month

    mensaje = ft.Text("")
    grid = ft.Column()
    seleccionado = {"dia": None}
    intento_reserva = {"valor": False}

    cantidad_personas = ft.Dropdown(
        label="Cantidad de personas",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 11)],
        width=180
    )

    horario_reserva = ft.Dropdown(
        label="Horario",
        options=[ft.dropdown.Option(h) for h in ["19:00", "20:00", "21:00", "22:00"]],
        width=180
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
            style = ft.ButtonStyle(
                text_style=ft.TextStyle(size=24)
            )
            if intento_reserva["valor"] and seleccionado["dia"] is None:
                style.shape = ft.RoundedRectangleBorder(radius=6, border_side=ft.BorderSide(2, "red"))
            if seleccionado["dia"] == dia:
                style.bgcolor = "blue"
                style.color = "white"
            btn = ft.ElevatedButton(
                str(dia),
                width=80,
                height=60,
                style=style,
                on_click=crear_on_click(dia)
            )
            fila.append(btn)
            if len(fila) == 7:
                dias.append(ft.Row(fila, spacing=10))
                fila = []
        if fila:
            dias.append(ft.Row(fila, spacing=10))
        encabezado = ft.Row(
            [ft.Text(d, width=80, weight="bold", size=20, text_align="center") for d in ["L", "M", "X", "J", "V", "S", "D"]],
            spacing=10
        )
        grid.controls = [
            ft.Text(f"{calendar.month_name[month]} {year}", size=32, weight="bold", width=600, text_align="center"),
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
            mensaje.value = (
               f"Reserva realizada para el {seleccionado['dia']}/{month}/{year} - "
                f"{cantidad_personas.value} personas a las {horario_reserva.value}"
            )
            with open("reservas.txt", "a", encoding="utf-8") as f:
                f.write(f"{seleccionado['dia']}/{month}/{year},{cantidad_personas.value} personas, {horario_reserva.value}\n")
        else:
            mensaje.value = ""
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

    reservar_btn = ft.ElevatedButton("Reservar", on_click=reservar, width=180)

    # Calendario a la izquierda, listas y botón a la derecha
    page.add(
        ft.Row(
            [
                grid,
                ft.VerticalDivider(width=30),
                ft.Column(
                    [cantidad_personas, horario_reserva, reservar_btn],
                    alignment="start",
                    horizontal_alignment="center",
                    spacing=18
                ),
            ],
            alignment="center",
            vertical_alignment="start",
            spacing=30
        ),
        mensaje
    )
    actualizar_calendario()

ft.app(main)