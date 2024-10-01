import flet as ft

class ColorPalette:
    def __init__(self, page, color_picker):
        palette = []
        self.prev_button = None
        self.page = page
        self.color_picker = color_picker
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
            self.color_picker.color=e.control.icon_color
            self.color_picker.update()
        else:
            button = e.control
            def save_color(e):
                if e.control.text == "Yes":
                    button.icon_color=self.color_picker.color
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