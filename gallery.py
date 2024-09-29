import flet as ft
import flet.canvas as cv
from firebase_admin import firestore
from flet_contrib.color_picker import ColorPicker
from firebase_utils import cloud_firestore
from PIL import Image

import os

directory = '../images'
def get_images():
    print("getting images")
    doc_ref = cloud_firestore.collection("users").document("anonymous")
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
    image.save(f'../images/output{num}.png')

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
        if "output" in filename:
            print(filename)
            images.controls.append(
                ft.Image(
                    src=f'/Users/glbennett8876/Downloads/hackgt11/images/{filename}',
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