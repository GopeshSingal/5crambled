import flet as ft
import flet.canvas as cv
from firebase_admin import firestore
from flet_contrib.color_picker import ColorPicker
from firebase_utils import cloud_firestore
from PIL import Image

import os
import shutil

directory = '../images'
def get_images(uid):
    path = os.path.abspath(directory)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    doc_ref = cloud_firestore.collection("users").document(uid)
    image_ref = doc_ref.collection("images").stream()
    count = 0
    for doc in image_ref:
        count += 1
        image = doc.to_dict()
        data = image["hex_array"]
        visualize_output_from_data(data, count)

def visualize_output_from_data(data, num):
    hex_array = data
    rgb_array = [(int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)) for hex_color in hex_array]
    image = Image.new("RGB", (32, 32))
    image.putdata(rgb_array)
    image.save(f'{directory}/output{num}.png')

button_style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))

def gallery_page(page: ft.Page, uid: str):
    images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    for filename in os.listdir(directory):
        if "output" in filename:
            images.controls.append(
                ft.Image(
                    src=os.path.abspath(f'{directory}/{filename}'),
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )
        page.update()

    home_button = [
        ft.IconButton(
            icon=ft.icons.HOUSE_ROUNDED, 
            icon_color=ft.colors.BLUE_GREY_700, 
            icon_size=28, 
            on_click=lambda _: page.go("/home")
        )
    ]

    logout_button = [
        ft.IconButton(
            icon=ft.icons.LOGOUT_ROUNDED, 
            icon_color=ft.colors.BLUE_GREY_700, 
            icon_size=28, 
            on_click=lambda _: page.go("/"))
    ]
    
    return [
            ft.AppBar(
                leading=ft.Container(
                    content=ft.Row(home_button), 
                    padding=ft.padding.only(left=10)), 
                title=ft.Text("Gallery"), 
                center_title=True, 
                bgcolor=ft.colors.SURFACE_VARIANT, 
                actions=[
                    ft.Container(
                        content=ft.Row(logout_button),
                        padding=ft.padding.only(right=10)
                    )
                ],
            ),
            images
        ]