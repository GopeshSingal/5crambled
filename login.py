import flet as ft
import requests
from firebase import firebase
from firebase_admin import auth
from firebase_utils import firebase_auth_url_template


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
        print(body)
        if response.ok:
            page.go('/home')

    def sign_up(email, password):
        signup_endpoint = 'accounts:signUp'
        request_body = {"email":email, "password": password, "returnSecureToken":True}
        response = firebase_post(signup_endpoint, request_body)
        body = response.json()
        print(body)
        if response.ok:
            page.go('/home')

    login_button = ft.ElevatedButton(text='Login', on_click=lambda _: login(email_field.value, password_field.value))
    sign_up_button = ft.ElevatedButton(text='Sign up', on_click=lambda _: sign_up(email_field.value, password_field.value))
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