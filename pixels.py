import flet as ft
import firebase_admin
from firebase_admin import firestore, credentials
import flet.canvas as cv

credentials_path = 'secrets.json'
cred = credentials.Certificate(credentials_path)

app = firebase_admin.initialize_app(cred)
db = firestore.client()

def main(page: ft.Page):
    page.title = 'Pixels'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    doc_name = ft.TextField(label='Document Name')
    field = ft.TextField(label='A field')

    def add_to_images(name: str, doc: dict):
        db.collection('images').add(doc, document_id=name)

    def canvas(size):
        ft.GridView(runs_count=)

    page.add(
        ft.Row(
            [
                cv.Canvas(),
                doc_name,
                field,
                ft.IconButton(ft.icons.ADD, on_click=lambda x: add_to_images(doc_name.value, {'field': field.value}))
            ]
        )
    )

ft.app(main)