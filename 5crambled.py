import flet as ft
import flet.canvas as cv

from flet_contrib.color_picker import ColorPicker

canvas_size = 512
grid_size = 16
ratio = canvas_size / grid_size 
color = ft.colors.BLACK

background = cv.Fill(
                ft.Paint(
                    gradient=ft.PaintLinearGradient(
                        (0, 0), (600, 600), colors=[ft.colors.CYAN_50, ft.colors.GREY]
                    )
                )
            )


class State:
    x: float
    y: float


state = State()


def main(page: ft.Page):
    page.title = "Flet Brush"
    # page.window.width = canvas_size + 16
    # page.window.height = canvas_size + 32
    # page.window.resizable = False

    def set_pixel():
        cp.shapes.remove()

    # color picker code
    color_picker = ColorPicker(color="#fff8e7")

    def change_color(e):
        color_picker.color = new_color.value
        color_picker.update()

    
    def pan_start(e: ft.DragStartEvent):
        state.x = (e.local_x // ratio)
        state.y = (e.local_y // ratio)

    def pan_update(e: ft.DragUpdateEvent):
        cp.shapes.append(
            cv.Rect(
                state.x * ratio, state.y * ratio, ratio, ratio, paint=ft.Paint(color=color_picker.color, stroke_width=2),
            )
        )
        
        cp.update()
        state.x = (e.local_x // ratio)
        state.y = (e.local_y // ratio)
    def on_tap(e: ft.TapEvent):
        state.x = (e.local_x // ratio)
        state.y = (e.local_y // ratio)
        cp.shapes.append(
            cv.Rect(
                state.x * ratio, state.y * ratio, ratio, ratio, paint=ft.Paint(color=color_picker.color, stroke_width=2),
            )
        )
        cp.update()
    def reset_canvas(e):
        cp.shapes = [background]
        page.update()

    cp = cv.Canvas(
        [
            background,
        ],
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
            on_tap_down = on_tap,
        expand=False,
    )
    )

    col = ft.Column(
        [
            color_picker,
        ]
    )

    row = ft.Row(
        [
            ft.Container(
                cp,
                border_radius=5,
                width=canvas_size,
                height=canvas_size,
                expand=False,
            ),
            col
        ]
    )
    page.add(
        row,
        ft.ElevatedButton(text="Reset", on_click=reset_canvas)
    )


ft.app(main)