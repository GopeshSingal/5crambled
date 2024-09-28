import flet as ft
import flet.canvas as cv

from flet_contrib.color_picker import ColorPicker

canvas_size = 512
grid_size = 16
ratio = canvas_size / grid_size 
color = ft.colors.BLACK
color_picker = ColorPicker(color="#fff8e7")
background = cv.Fill(
                ft.Paint(
                    "#ffffff"
                )
            )


class State:
    x: float
    y: float


state = State()


class Color_palette:
    def __init__(self):
        palette = []

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
        
        # create button to select pick or save
        # pick: use the selected color
        # save: reset the button color to the current color
        self.select_group = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="pick", label="Pick"),
        ft.Radio(value="save", label="Save")]),
        value="pick")

        self.palette = ft.Column(
            [
                ft.Row(palette),
                self.select_group
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # Changes the paint color to the button color if "pick"
    # Otherwise resets the button color to the current color
    def select_color(self, e):
        if self.select_group.value == "pick":
            color_picker.color=e.control.icon_color
            color_picker.update()
        else:
            e.control.icon_color=color_picker.color
            e.control.update()


        
def main(page: ft.Page):
    page.title = "Flet Brush"
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
    color_palette = Color_palette()

    color_col = ft.Container(
        content=ft.Column(
            [color_picker, color_palette.palette],
            ft.MainAxisAlignment.CENTER
        ),
        bgcolor="#d8dae0",
        border_radius=5,
    )
    def upload():
        return

    
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
        expand=False,
    )
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
            color_col,
        ]
    )

    button_row = ft.Row(
        [
            ft.ElevatedButton(text="Reset", on_click=reset_canvas),
            ft.ElevatedButton(text="Fill", on_click= lambda x: reset_canvas(x, color=color_picker.color)),
            ft.ElevatedButton(text="Upload", on_click=upload)
        ]
    )

    page.add(
        row,
        button_row
    )
ft.app(main)