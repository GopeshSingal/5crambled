import flet as ft
import firebase_admin
from firebase_admin import credentials, auth


def login_page(page: ft.Page):
    username = ft.TextField(label='Username', )
    password = ft.TextField(label='Password', )

    def login(username, password):
        pass

    input_row = ft.Row(
        [
            username,
            password,
        ]
    )
    login_button = ft.ElevatedButton(text='Login', on_click=login)
    
    buttons = [
        ft.ElevatedButton("Go to canvas", on_click=lambda _: page.go("/home")),
        ft.ElevatedButton("See Gallery", on_click=lambda _: page.go("/works"))
    ]
    
    return [
        ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT, actions=buttons),
        input_row,
        login_button
    ]