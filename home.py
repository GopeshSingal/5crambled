import flet as ft
import flet.canvas as cv
from firebase_admin import firestore
from flet_contrib.color_picker import ColorPicker
from firebase_utils import cloud_firestore

canvas_size = 512
grid_size = 32
ratio = canvas_size / grid_size

button_style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))

class State:
    x: float
    y: float
    fill: bool
    dropper: bool

class Color_palette:
    def __init__(self, page):
        palette = []
        self.prev_button = None
        self.page = page
        # base colors: white, black, red, orange, green, blue, purple
        self.base_colors = ["#ffffff", "#000000", "#ff0000", "#ffa500", "#008000", "#0000ff", "#7D0DC3"]

        for i in range(7):
            palette.append(
                ft.IconButton(
                    icon=ft.icons.SQUARE_ROUNDED,
                    icon_color=self.base_colors[i],
                    icon_size=20,
                    on_click=self.select_color
                    # tooltip="Pause record",
                )
            )

        self.palette = ft.Column(
            [ft.Row(palette)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # Changes the paint color to the button color if "pick"
    # Otherwise resets the button color to the current color
    def select_color(self, e):
        if self.prev_button != e.control: # picking new button
            if self.prev_button:
                self.prev_button.selected=False
            self.prev_button=e.control
            e.control.selected=True
            e.control.focus()
            e.control.update()
            color_picker.color=e.control.icon_color
            color_picker.update()
        else:
            button = e.control
            def save_color(e):
                if e.control.text == "Yes":
                    button.icon_color=color_picker.color
                    button.update()
                dlg_modal.open=False
                self.page.update()
            
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Save color?"),
                actions=[
                    ft.TextButton("Yes", on_click=save_color),
                    ft.TextButton("No", on_click=save_color),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.views[-1].controls.append(dlg_modal)
            dlg_modal.open=True
            self.page.update()


state = State()
state.fill = False
state.dropper = False
history = []
rhistory = []
color_picker = ColorPicker(color="#fff8e7")

def home_page(page: ft.Page):
    def init_canvas():
        shapes = []
        for i in range(grid_size):
            for j in range(grid_size):
                shapes.append(cv.Rect(j * ratio, i * ratio, ratio, ratio, paint=ft.Paint(color="#ffffff", stroke_width=2)))
        return shapes

    def upload_to_firebase(e):
        data_array = []
        for i in range(grid_size):
            for j in range(grid_size):
                data_array.append(cp.shapes[(int)(i + j * grid_size)].paint.color)
        
        cloud_firestore.collection("images").add({"hex_array": data_array,
                                             "timestamp": firestore.SERVER_TIMESTAMP})
        
    def set_pixel(x, y):
        if -1 < x < 512 and -1 < y < 512:
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
        if state.dropper:
            i = e.local_x // ratio
            j = e.local_y // ratio
            color_picker.color = cp.shapes[(int)(i + j * grid_size)].paint.color
            color_picker.update()
            return
        save_state()
        reset_history()
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

    def reset_history():
        rhistory.clear()

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
    
    def dropper_checkbox_changed(e):
        if state.dropper:
            state.dropper = False
        else:
            state.dropper = True

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

    color_palette = Color_palette(page)

    cp = cv.Canvas(init_canvas(),
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
            on_tap_down = on_tap,
        expand=False,
        )
    )

    color_col = ft.Container(
        content=ft.Column(
            [color_picker, color_palette.palette],
            ft.MainAxisAlignment.CENTER
        ),
        bgcolor="#d8dae0",
        border_radius=5, 
        height = canvas_size
    )

    button_row = ft.Row(
        [
            ft.ElevatedButton(
                text="Reset", 
                on_click=reset_canvas, 
                style=button_style
            ),
            ft.ElevatedButton(
                text="Upload", 
                on_click=upload_to_firebase, 
                style=button_style
            ),
            ft.ElevatedButton(
                text="Undo", 
                on_click=revert_state, 
                style=button_style
            ),
            ft.ElevatedButton(
                text="Redo", 
                on_click=unrevert_state, 
                style=button_style
            ),
            ft.Checkbox(label="Fill Mode", on_change=fill_checkbox_changed),
            ft.Checkbox(label="Dropper", on_change=dropper_checkbox_changed)
        ]
    )

    column = ft.Column(
        [
            ft.Container(
                cp,
                border_radius=5,
                width=canvas_size,
                height=canvas_size,
                expand=False,
            ),
            button_row,
        ], 
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment = ft.CrossAxisAlignment.CENTER
    )

    container = ft.Container(
        content=ft.Row(
            [column, color_col],
            alignment=ft.MainAxisAlignment.CENTER, 
            vertical_alignment = ft.CrossAxisAlignment.START, 
            expand = True
        ),
    )

    main_col = ft.Column(
        [container], 
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment = ft.CrossAxisAlignment.CENTER, 
        expand = True
    )

    return [
            ft.AppBar(title=ft.Text("Home"), bgcolor=ft.colors.SURFACE_VARIANT, actions=[ft.ElevatedButton("Log out", on_click=lambda _: page.go("/"))],),
            main_col
        ]
