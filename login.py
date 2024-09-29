import flet as ft
import requests
from firebase_utils import firebase_auth_url_template

button_style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))

def login_page(page: ft.Page):
    email_field = ft.TextField(label='Email', width=300)
    password_field = ft.TextField(label='Password', width=300, password=True, can_reveal_password=True)

    def firebase_post(endpoint: str, body: dict):
        url = firebase_auth_url_template.format(endpoint=endpoint)
        headers = {"Content-Type": "application/json"}
        return requests.post(url, json=body, headers=headers)

    def login(email, password):
        login_endpoint = 'accounts:signInWithPassword'
        request_body = {"email":email, "password": password, "returnSecureToken":True}
        response = firebase_post(login_endpoint, request_body)
        body = response.json()

        if response.ok:
            page.go('/home')
        elif response.status_code == 400:
            error_message = body['error']['message']
            if 'EMAIL' in error_message:
                email_field.error_text = body['error']['message']
                email_field.update()
            else:
                password_field.error_text = body['error']['message']
                password_field.update()


    def sign_up(email, password):
        signup_endpoint = 'accounts:signUp'
        request_body = {"email":email, "password": password, "returnSecureToken":True}
        response = firebase_post(signup_endpoint, request_body)
        body = response.json()

        if response.ok:
            page.go('/home')
        elif response.status_code == 400:
            error_message = body['error']['message']
            if 'EMAIL' in error_message:
                email_field.error_text = body['error']['message']
                email_field.update()
            else:
                password_field.error_text = body['error']['message']
                password_field.update()

    login_button = ft.ElevatedButton(
        text='Login',
        on_click=lambda _: login(email_field.value, password_field.value),
        style=button_style)
    sign_up_button = ft.ElevatedButton(
        text='Sign up',
        on_click=lambda _: sign_up(email_field.value, password_field.value),
        style=button_style
    )

    input_row = ft.Row(
        [
            ft.Column(
                [
                    email_field,
                    password_field,
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

    return [
        ft.AppBar(
            title=ft.Text("Login"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.ElevatedButton("Go to canvas", on_click=lambda _: page.go("/home"))
            ]
        ),
        input_row
    ]