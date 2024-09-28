import flet as ft
import flet.canvas as cv
from firebase_admin import firestore
from flet_contrib.color_picker import ColorPicker
from firebase_utils import cloud_firestore

canvas_size = 512
grid_size = 32
ratio = canvas_size / grid_size
color = ft.colors.BLACK

class State:
    x: float
    y: float


state = State()

def home_page(page: ft.Page):
    def init_canvas():
        shapes = []
        for i in range(grid_size):
            for j in range(grid_size):
                shapes.append(cv.Rect(j * ratio, i * ratio, ratio, ratio, paint=ft.Paint(color="#ffffff", stroke_width=2)))
        return shapes

        # color picker code
    color_picker = ColorPicker(color="#fff8e7")

    def upload_to_firebase(e):
        data_array = []
        for i in range(grid_size):
            for j in range(grid_size):
                data_array.append(cp.shapes[int(i + j * grid_size)].paint.color)
        cloud_firestore.collection("images").add({"hex_array": data_array,
                                                 "timestamp": firestore.SERVER_TIMESTAMP})


    def set_pixel(x, y):
        if -1 < x < 512 and -1 < y < 512:
            x = x // ratio
            y = y // ratio
            cp.shapes[int(x + y * grid_size)].paint.color = color_picker.color


    def pan_start(e: ft.DragStartEvent):
        set_pixel(e.local_x, e.local_y)

    def pan_update(e: ft.DragUpdateEvent):
        set_pixel(e.local_x, e.local_y)
        cp.update()
        state.x = (e.local_x // ratio)
        state.y = (e.local_y // ratio)
    def on_tap(e: ft.TapEvent):
        set_pixel(e.local_x, e.local_y)
        cp.update()

    def reset_canvas(e, color="#ffffff"):
        for i in range(grid_size):
            for j in range(grid_size):
                cp.shapes[int(i + j * grid_size)].paint.color = color
        page.update()

    cp = cv.Canvas(init_canvas(),
                   content=ft.GestureDetector(
                       on_pan_start=pan_start,
                       on_pan_update=pan_update,
                       drag_interval=10,
                       on_tap_down = on_tap,
                       expand=False,)
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
            color_picker,
        ]
    )
    button_row = ft.Row(
        [
            ft.ElevatedButton(text="Reset", on_click=reset_canvas),
            ft.ElevatedButton(text="Fill", on_click= lambda x: reset_canvas(x, color=color_picker.color)),
            ft.ElevatedButton(text="Upload", on_click=upload_to_firebase)
        ]
    )

    return [
            ft.AppBar(title=ft.Text("Home"), bgcolor=ft.colors.SURFACE_VARIANT, actions=[ft.ElevatedButton("Log out", on_click=lambda _: page.go("/"))],),
            row,
            button_row
        ]