import flet as ft
import flet.canvas as cv
from firebase_admin import firestore
from flet_contrib.color_picker import ColorPicker
from firebase_utils import cloud_firestore
from PIL import Image
from urllib.parse import urlencode
import math

import os
import shutil

directory = '../images'

def remove_local():
    path = os.path.abspath(directory)
    if os.path.exists(path):
        shutil.rmtree(path)

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

    def visualize_output_from_data(data, num, uid):
        hex_array = data
        size = math.sqrt(len(hex_array))
        size_inc = 4
        rgb_array = []
        
        for i in range(0, len(hex_array), int(size)):
            row = hex_array[i:i+int(size)]
            for _ in range(size_inc):
                for hex_color in row:
                    rgb_tuple = (int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16))
                    extend_list = [rgb_tuple for _ in range(size_inc)]
                    rgb_array.extend(extend_list)
        
        image = Image.new("RGB", ((int)(size*size_inc), (int)(size*size_inc)))
        image.putdata(rgb_array)
        image.save(f'{directory}/output_{uid}_{num}.png')
        query_param = urlencode([('data', i) for i in data])
        images.controls.append(
            ft.Container(
                content=ft.Image(
                    src=os.path.abspath(f'{directory}/output_{uid}_{num}.png'),
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),
                on_click=lambda _: page.go("/home", uid=uid, data=query_param)
            )
        )

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
        visualize_output_from_data(data, count, uid)


    home_button = [
        ft.IconButton(
            icon=ft.icons.HOUSE_ROUNDED, 
            icon_color=ft.colors.BLUE_GREY_700, 
            icon_size=28, 
            on_click=lambda _: page.go("/home", uid=uid)
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