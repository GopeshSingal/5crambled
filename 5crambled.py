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
    fill: bool

state = State()
history = []
rhistory = []


def main(page: ft.Page):
    page.title = "Pixels"
    page.bgcolor = "#495da3"

    def init_canvas():
        shapes = []
        state.fill = False
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
        save_state()
        if state.fill:
            fill_canvas(e.local_x, e.local_y)
        else:
            set_pixel(e.local_x, e.local_y)
        cp.update()
        
    def reset_canvas(e):
        save_state()
        for i in range(grid_size):
            for j in range(grid_size):
                cp.shapes[(int)(i + j * grid_size)].paint.color = "#ffffff"
        page.update()

    def save_state(do=True):
        if do:
            current_state = [shape.paint.color for shape in cp.shapes]
            history.append(current_state)
        else:
            current_state = [shape.paint.color for shape in cp.shapes]
            rhistory.append(current_state)

    def revert_state(e):
        save_state(False)
        if history:
            old_state = history.pop()
            for i, shape in enumerate(cp.shapes):
                shape.paint.color = old_state[i]
            cp.update()
    
    def unrevert_state(e):
        save_state()
        if rhistory:
            old_state = rhistory.pop()
            for i, shape in enumerate(cp.shapes):
                shape.paint.color = old_state[i]
            cp.update()

    def fill_checkbox_changed(e):
        if state.fill:
            state.fill = False
        else:
            state.fill = True
    
    def is_valid(x, y):
        return 0 <= x < grid_size and 0 <= y < grid_size

    def fill_canvas(x, y):
        x = x // ratio
        y = y // ratio
        frontier = [(x, y)]
        visited = []
        old_color = cp.shapes[(int)(x + y * grid_size)].paint.color
        new_color = color_picker.color
        if new_color == old_color:
            return
        while frontier:
            cx, cy = frontier.pop()
            if (cx, cy) in visited:
                continue
            visited.append((cx, cy))
            if is_valid(cx, cy) and cp.shapes[(int)(cx + cy * grid_size)].paint.color == old_color:
                set_pixel(cx * ratio, cy * ratio)
                frontier.append((cx + 1, cy))
                frontier.append((cx - 1, cy))
                frontier.append((cx, cy + 1))
                frontier.append((cx, cy - 1))

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
            ft.ElevatedButton(text="Upload", on_click=upload_to_firebase),
            ft.ElevatedButton(text="Undo", on_click=revert_state),
            ft.ElevatedButton(text="Redo", on_click=unrevert_state),
            ft.Checkbox(label="Fill Mode", on_change=fill_checkbox_changed)
        ]
    )
    page.add(
        row,
        button_row
    )
ft.app(main)