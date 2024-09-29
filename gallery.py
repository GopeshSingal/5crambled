import flet as ft
import flet.canvas as cv
from firebase_admin import firestore
from flet_contrib.color_picker import ColorPicker
import os

directory = 'assets'

def gallery_page(page: ft.Page):
    images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            images.controls.append(
                ft.Image(
                    src=filename,
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )

    buttons = [
        ft.ElevatedButton("Go to canvas", on_click=lambda _: page.go("/home")),
        ft.ElevatedButton("See Gallery", on_click=lambda _: page.go("/works"))
    ]
    
    return [
        ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT, actions=buttons),
        images
    ]