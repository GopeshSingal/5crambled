import flet as ft
import requests
from firebase_utils import firebase_auth_url_template

button_style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))

class LoginPage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.email_field = ft.TextField(label='Email', width=300)
        self.password_field = ft.TextField(label='Password', width=300, password=True, can_reveal_password=True)

    def firebase_post(self, endpoint: str, body: dict):
        url = firebase_auth_url_template.format(endpoint=endpoint)
        headers = {"Content-Type": "application/json"}
        return requests.post(url, json=body, headers=headers)

    def login(self, email, password):
        login_endpoint = 'accounts:signInWithPassword'
        request_body = {"email":email, "password": password, "returnSecureToken":True}
        response = self.firebase_post(login_endpoint, request_body)
        body = response.json()

        if response.ok:
            uid = body['localId']
            self.page.go('/home', uid=uid)
        elif response.status_code == 400:
            error_message = body['error']['message']
            if 'EMAIL' in error_message:
                self.email_field.error_text = body['error']['message']
                self.email_field.update()
            else:
                self.password_field.error_text = body['error']['message']
                self.password_field.update()


    def sign_up(self, email, password):
        signup_endpoint = 'accounts:signUp'
        request_body = {"email":email, "password": password, "returnSecureToken": True}
        response = self.firebase_post(signup_endpoint, request_body)
        body = response.json()

        if response.ok:
            uid = body['localId']
            self.page.go('/home', uid=uid)
        elif response.status_code == 400:
            error_message = body['error']['message']
            if 'EMAIL' in error_message:
                self.email_field.error_text = body['error']['message']
                self.email_field.update()
            else:
                self.password_field.error_text = body['error']['message']
                self.password_field.update()

    def build_page(self):
        login_button = ft.ElevatedButton(
            text='Login',
            on_click=lambda _: self.login(self.email_field.value, self.password_field.value),
            style=button_style)
        sign_up_button = ft.ElevatedButton(
            text='Sign up',
            on_click=lambda _: self.sign_up(self.email_field.value, self.password_field.value),
            style=button_style
        )

        input_row = ft.Row(
            [
                ft.Column(
                    [
                        self.email_field,
                        self.password_field,
                        ft.Row(
                            [
                                login_button,
                                sign_up_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
        login_button = ft.ElevatedButton(text='Login', on_click=self.login)
        
        buttons = [
            ft.ElevatedButton("Go to canvas", on_click=lambda _: self.page.go("/home", uid='anonymous'), style=button_style),
            ft.IconButton(
                icon=ft.icons.PHOTO_LIBRARY_ROUNDED, 
                icon_color=ft.colors.BLUE_GREY_700,
                icon_size=28,
                on_click=lambda _: self.page.go("/works", uid='anonymous')
            )
        ]
        
        return [
            ft.AppBar(
                title=ft.Text("Login"),
                center_title=True, 
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.Container(
                        content=ft.Row(buttons), 
                        padding=ft.padding.only(right=10)
                    ),
                ],
            ),
            input_row
        ]