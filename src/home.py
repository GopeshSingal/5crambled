import flet as ft
import flet.canvas as cv
from flet_contrib.color_picker import ColorPicker
from color_palette import ColorPalette
from state import State
from utils.button_handlers import handle_key, fill_button_clicked, dropper_button_clicked, reset_canvas
from utils.upload_utils import Upload

canvas_size = 512
grid_size = 32
ratio = canvas_size / grid_size

button_style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))

class HomePage:
    def __init__(self, page: ft.Page, uid: str, data: str | None):
        self.page = page
        self.uid = uid
        self.data = data
        self.color_picker = ColorPicker(color="#000000")
        self.cp = cv.Canvas(self.init_canvas(),
            content=ft.GestureDetector(
                on_pan_start=self.pan_start,
                on_pan_update=self.pan_update,
                drag_interval=10,
                on_tap_down = self.on_tap,
            expand=False,
            )
        )
        self.state = State(self.cp)
        self.state.fill = False
        self.state.dropper = False

    def init_canvas(self):
        shapes = []
        for i in range(grid_size):
            for j in range(grid_size):
                if self.data:
                    shapes.append(cv.Rect(j * ratio, i * ratio, ratio, ratio, paint=ft.Paint(color=self.data[i * grid_size + j], stroke_width=2))) 
                    # shapes.append(cv.Rect(j * ratio, i * ratio, ratio, ratio, paint=ft.Paint(color="#ffffff", stroke_width=2)))
                else:
                    shapes.append(cv.Rect(j * ratio, i * ratio, ratio, ratio, paint=ft.Paint(color="#ffffff", stroke_width=2)))
        return shapes

    def pan_start(self, e: ft.DragStartEvent):
        self.set_pixel(e.local_x, e.local_y)

    def set_pixel(self, x, y):
        if 0 <= x < 512 and 0 <= y < 512:
            x = x // ratio
            y = y // ratio
            self.cp.shapes[(int)(x + y * grid_size)].paint.color = self.color_picker.color

    def pan_update(self, e: ft.DragUpdateEvent):
        self.set_pixel(e.local_x, e.local_y)
        self.cp.update()
        self.state.x = (e.local_x // ratio)
        self.state.y = (e.local_y // ratio)

    def on_tap(self, e: ft.TapEvent):
        if self.state.dropper:
            i = e.local_x // ratio
            j = e.local_y // ratio
            self.color_picker.color = self.cp.shapes[(int)(i + j * grid_size)].paint.color
            self.color_picker.update()
            self.button_row.controls[5].selected = False
            self.button_row.update()
            self.state.dropper = False
            return
        self.state.save_state()
        self.state.reset_history()
        if self.state.fill:
            self.fill_canvas(e.local_x, e.local_y)
        else:
            self.set_pixel(e.local_x, e.local_y)
        self.cp.update()

    def is_valid(self, x, y):
        return 0 <= x < grid_size and 0 <= y < grid_size

    def fill_canvas(self, x, y):
        x = x // ratio
        y = y // ratio
        frontier = [(x, y)]
        visited = []
        old_color = self.cp.shapes[(int)(x + y * grid_size)].paint.color
        new_color = self.color_picker.color
        if new_color == old_color:
            return
        while frontier:
            cx, cy = frontier.pop()
            if (cx, cy) in visited:
                continue
            visited.append((cx, cy))
            if self.is_valid(cx, cy) and self.cp.shapes[(int)(cx + cy * grid_size)].paint.color == old_color:
                self.set_pixel(cx * ratio, cy * ratio)
                frontier.append((cx + 1, cy))
                frontier.append((cx - 1, cy))
                frontier.append((cx, cy + 1))
                frontier.append((cx, cy - 1))
        self.button_row.controls[4].selected = False
        self.button_row.update()
        self.state.fill = False

    def build_page(self):
        self.color_palette = ColorPalette(self.page, self.color_picker)
        upload_obj = Upload(self.page, grid_size, self.cp, self.uid)

        color_col = ft.Container(
            content=ft.Column(
                [self.color_picker, self.color_palette.palette],
                ft.MainAxisAlignment.CENTER
            ),
            bgcolor="#d8dae0",
            border_radius=5, 
            height = canvas_size
        )

        self.button_row = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.FORMAT_COLOR_RESET_ROUNDED,
                    icon_color=ft.colors.BLUE_GREY_700,
                    icon_size=20, 
                    on_click=lambda e: reset_canvas(e, grid_size, self.state, self.cp, self.page), 
                    tooltip="Reset",
                ),
                ft.IconButton(
                    icon=ft.icons.CLOUD_UPLOAD_ROUNDED,
                    icon_color=ft.colors.BLUE_GREY_700,
                    icon_size=20, 
                    on_click=upload_obj.upload_to_firebase, 
                    tooltip="Upload",
                ),
                ft.IconButton(
                    icon=ft.icons.UNDO_ROUNDED,
                    icon_color=ft.colors.BLUE_GREY_700,
                    icon_size=20, 
                    on_click=self.state.revert_state, 
                    tooltip="Undo",
                ),
                ft.IconButton(
                    icon=ft.icons.REDO_ROUNDED,
                    icon_color=ft.colors.BLUE_GREY_700,
                    icon_size=20, 
                    on_click=self.state.unrevert_state, 
                    tooltip="Redo",
                ),
                ft.IconButton(
                    icon=ft.icons.FORMAT_COLOR_FILL_ROUNDED, 
                    selected_icon=ft.icons.FORMAT_COLOR_FILL_ROUNDED, 
                    icon_size=20, 
                    on_click=lambda e: fill_button_clicked(e, self.state, self.button_row), 
                    selected=False,
                    style=ft.ButtonStyle(color={"selected": ft.colors.BLUE_300, "": ft.colors.BLUE_GREY_700}),
                    tooltip="Toggle Fill",
                ),
                ft.IconButton(
                    icon=ft.icons.COLORIZE_ROUNDED, 
                    selected_icon=ft.icons.COLORIZE_ROUNDED,  
                    icon_size=20, 
                    on_click=lambda e: dropper_button_clicked(e, self.state, self.button_row), 
                    selected=False,
                    style=ft.ButtonStyle(color={"selected": ft.colors.BLUE_300, "": ft.colors.BLUE_GREY_700}),
                    tooltip="Toggle Dropper",
                )
            ]
        )

        column = ft.Column(
            [
                ft.Container(
                    self.cp,
                    border_radius=5,
                    width=canvas_size,
                    height=canvas_size,
                    expand=False,
                ),
                self.button_row,
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
                on_click=lambda _: self.page.go("/works", uid=self.uid)
            ), 
            ft.IconButton(
                icon=ft.icons.LOGOUT_ROUNDED, 
                icon_color=ft.colors.BLUE_GREY_700, 
                icon_size=28, 
                on_click=lambda _: self.page.go("/"))
        ]

        self.page.on_keyboard_event = lambda e: handle_key(e, self.button_row, self.color_picker, self.color_palette, self.state, self.page, grid_size, self.cp)


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
