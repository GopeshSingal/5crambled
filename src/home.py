import flet as ft
import flet.canvas as cv
from firebase_admin import firestore
from flet_contrib.color_picker import ColorPicker
from firebase_utils import cloud_firestore
from datetime import datetime

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
color_picker = ColorPicker(color="#000000")

def home_page(page: ft.Page, uid: str):
    def init_canvas():
        shapes = []
        for i in range(grid_size):
            for j in range(grid_size):
                shapes.append(cv.Rect(j * ratio, i * ratio, ratio, ratio, paint=ft.Paint(color="#ffffff", stroke_width=2)))
        return shapes
    page.on_keyboard_event = lambda x: handle_key(e=x)
    def handle_key(e: ft.KeyboardEvent):
        match e.key:
            case "Z" if e.ctrl or e.meta:
                if e.shift:
                    unrevert_state(e)
                else:
                    revert_state(e)
            case "A" if e.ctrl or e.meta:
                button_row.controls[4].selected = not button_row.controls[4].selected
                button_row.update()
                fill_button_clicked(e)
            case "D" if e.ctrl or e.meta:
                button_row.controls[5].selected = not button_row.controls[5].selected
                button_row.update()
                dropper_button_clicked(e)
            case "1":
                color_picker.color = color_palette.palette.controls[0].controls[0].icon_color
                color_palette.palette.controls[0].controls[0].selected = True
                color_palette.palette.controls[0].controls[0].focus()
                color_palette.palette.controls[0].controls[0].update()
                page.update()
            case "2":
                color_picker.color = color_palette.palette.controls[0].controls[1].icon_color
                color_palette.palette.controls[0].controls[1].selected = True
                color_palette.palette.controls[0].controls[1].focus()
                color_palette.palette.controls[0].controls[1].update()
                page.update()
            case "3":
                color_picker.color = color_palette.palette.controls[0].controls[2].icon_color
                color_palette.palette.controls[0].controls[2].selected = True
                color_palette.palette.controls[0].controls[2].focus()
                color_palette.palette.controls[0].controls[2].update()
                page.update()
            case "4":
                color_picker.color = color_palette.palette.controls[0].controls[3].icon_color
                color_palette.palette.controls[0].controls[3].selected = True
                color_palette.palette.controls[0].controls[3].focus()
                color_palette.palette.controls[0].controls[3].update()
                page.update()
            case "5":
                color_picker.color = color_palette.palette.controls[0].controls[4].icon_color
                color_palette.palette.controls[0].controls[4].selected = True
                color_palette.palette.controls[0].controls[4].focus()
                color_palette.palette.controls[0].controls[4].update()
                page.update()
            case "6":
                color_picker.color = color_palette.palette.controls[0].controls[5].icon_color
                color_palette.palette.controls[0].controls[5].selected = True
                color_palette.palette.controls[0].controls[5].focus()
                color_palette.palette.controls[0].controls[5].update()
                page.update()
            case "7":
                color_picker.color = color_palette.palette.controls[0].controls[6].icon_color
                color_palette.palette.controls[0].controls[6].selected = True
                color_palette.palette.controls[0].controls[6].focus()
                color_palette.palette.controls[0].controls[6].update()
                page.update()
    def upload_anon(e):
        data_array = []
        for i in range(grid_size):
            for j in range(grid_size):
                data_array.append(cp.shapes[(int)(j + i * grid_size)].paint.color)
        cloud_firestore.collection("users").document('anonymous').collection('images').document(datetime.now().isoformat()).set({"hex_array": data_array,
                                         "timestamp": firestore.SERVER_TIMESTAMP})
        if uid != 'anonymous':
            cloud_firestore.collection("users").document(uid).collection('images').document(datetime.now().isoformat()).set({"hex_array": data_array,
                                            "timestamp": firestore.SERVER_TIMESTAMP})
        diag_box.open = False
        page.update()

    def upload_private(e):
        data_array = []
        for i in range(grid_size):
            for j in range(grid_size):
                data_array.append(cp.shapes[(int)(j + i * grid_size)].paint.color)
        cloud_firestore.collection("users").document(uid).collection('images').document(datetime.now().isoformat()).set({"hex_array": data_array,
                                         "timestamp": firestore.SERVER_TIMESTAMP})
        diag_box.open = False
        page.update()

    def upload_cancel(e):
        diag_box.open = False
        page.update()

    def upload_to_firebase(e):
        page.views[-1].controls.append(diag_box)
        diag_box.open=True
        page.update()

    def pan_start(e: ft.DragStartEvent):
        set_pixel(e.local_x, e.local_y)

    def set_pixel(x, y):
        if 0 <= x < 512 and 0 <= y < 512:
            x = x // ratio
            y = y // ratio
            cp.shapes[(int)(x + y * grid_size)].paint.color = color_picker.color

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
            button_row.controls[5].selected = False
            button_row.update()
            state.dropper = False
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
        if history:
            save_state(False)
            old_state = history.pop()
            for i, shape in enumerate(cp.shapes):
                shape.paint.color = old_state[i]
            cp.update()
    
    def unrevert_state(e):
        if rhistory:
            save_state()
            old_state = rhistory.pop()
            for i, shape in enumerate(cp.shapes):
                shape.paint.color = old_state[i]
            cp.update()

    def fill_button_clicked(e):
        if state.fill:
            state.fill = False
            e.control.selected = not e.control.selected
            e.control.update()
        else:
            state.fill = True
            button_row.controls[5].selected = False
            button_row.update()
            state.dropper = False
            e.control.selected = not e.control.selected
            e.control.update()
    
    def dropper_button_clicked(e):
        if state.dropper:
            state.dropper = False
            e.control.selected = not e.control.selected
            e.control.update()
        else:
            state.dropper = True
            button_row.controls[4].selected = False
            button_row.update()
            state.fill = False
            e.control.selected = not e.control.selected
            e.control.update()

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
        button_row.controls[4].selected = False
        button_row.update()
        state.fill = False


    color_palette = Color_palette(page)

    diag_box = ft.AlertDialog(
            modal=True,
            title=ft.Text("Upload globally or privately?"),
            actions=[
                    ft.TextButton("Global", on_click=upload_anon),
                    ft.TextButton("Private", on_click=upload_private),
                    ft.TextButton("Cancel", on_click=upload_cancel)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            )

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
            ft.IconButton(
                icon=ft.icons.FORMAT_COLOR_RESET_ROUNDED,
                icon_color=ft.colors.BLUE_GREY_700,
                icon_size=20, 
                on_click=reset_canvas, 
                tooltip="Reset",
            ),
            ft.IconButton(
                icon=ft.icons.CLOUD_UPLOAD_ROUNDED,
                icon_color=ft.colors.BLUE_GREY_700,
                icon_size=20, 
                on_click=upload_to_firebase, 
                tooltip="Upload",
            ),
            ft.IconButton(
                icon=ft.icons.UNDO_ROUNDED,
                icon_color=ft.colors.BLUE_GREY_700,
                icon_size=20, 
                on_click=revert_state, 
                tooltip="Undo",
            ),
            ft.IconButton(
                icon=ft.icons.REDO_ROUNDED,
                icon_color=ft.colors.BLUE_GREY_700,
                icon_size=20, 
                on_click=unrevert_state, 
                tooltip="Redo",
            ),
            ft.IconButton(
                icon=ft.icons.FORMAT_COLOR_FILL_ROUNDED, 
                selected_icon=ft.icons.FORMAT_COLOR_FILL_ROUNDED, 
                icon_size=20, 
                on_click=fill_button_clicked, 
                selected=False,
                style=ft.ButtonStyle(color={"selected": ft.colors.BLUE_300, "": ft.colors.BLUE_GREY_700}),
                tooltip="Toggle Fill",
            ),
            ft.IconButton(
                icon=ft.icons.COLORIZE_ROUNDED, 
                selected_icon=ft.icons.COLORIZE_ROUNDED,  
                icon_size=20, 
                on_click=dropper_button_clicked, 
                selected=False,
                style=ft.ButtonStyle(color={"selected": ft.colors.BLUE_300, "": ft.colors.BLUE_GREY_700}),
                tooltip="Toggle Dropper",
            )
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

    buttons = [
        ft.IconButton(
            icon=ft.icons.PHOTO_LIBRARY_ROUNDED, 
            icon_color=ft.colors.BLUE_GREY_700,
            icon_size=28,
            on_click=lambda _: page.go("/works", uid=uid)
        ), 
        ft.IconButton(
            icon=ft.icons.LOGOUT_ROUNDED, 
            icon_color=ft.colors.BLUE_GREY_700, 
            icon_size=28, 
            on_click=lambda _: page.go("/"))
    ]

    return [
            ft.AppBar(
                leading=ft.Container(), 
                title=ft.Text("Prompt: Favorite Food"), 
                center_title=True, 
                bgcolor=ft.colors.SURFACE_VARIANT, 
                actions=[
                    ft.Container(
                        content=ft.Row(buttons),
                        padding=ft.padding.only(right=10)
                    )
                ],
            ),
            main_col
        ]
