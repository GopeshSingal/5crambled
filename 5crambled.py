import firebase_admin.firestore
import flet as ft
import flet.canvas as cv
import firebase_admin
from firebase_admin import credentials, firestore
from flet_contrib.color_picker import ColorPicker
import uuid

cred = credentials.Certificate("./secrets.json")
firebase_admin.initialize_app(cred)
cloud_firebase = firestore.client()

canvas_size = 512
grid_size = 32
ratio = canvas_size / grid_size 
color = ft.colors.BLACK


class State:
    x: float
    y: float


state = State()


def main(page: ft.Page):
    page.title = "Pixels"
    page.bgcolor = "#495da3"
    # page.window.width = canvas_size + 16
    # page.window.height = canvas_size + 32
    # page.window.resizable = False

    def init_canvas():
        shapes = []
        for i in range(grid_size):
            for j in range(grid_size):
                shapes.append(cv.Rect(j * ratio, i * ratio, ratio, ratio, paint=ft.Paint(color="#ffffff", stroke_width=2)))
        return shapes

    # color picker code
    color_picker = ColorPicker(color="#fff8e7")


    def change_color(e):
        color_picker.color = new_color.value
        color_picker.update()

    def upload_to_firebase(e):
        data_array = []
        for i in range(grid_size):
            for j in range(grid_size):
                data_array.append(cp.shapes[(int)(i + j * grid_size)].paint.color)
        cloud_firebase.collection("images").add({"hex_array": data_array,
                                                 "timestamp": firestore.SERVER_TIMESTAMP})

    
    def set_pixel(x, y):
        if x > -1 and x < 512 and y > -1 and y < 512:
            x = x // ratio
            y = y // ratio
            cp.shapes[(int)(x + y * grid_size)].paint.color = color_picker.color


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
                cp.shapes[(int)(i + j * grid_size)].paint.color = color
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
    page.add(
        row,
        button_row
    )
ft.app(main)