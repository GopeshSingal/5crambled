import flet as ft
from firebase_admin import firestore
from firebase_utils import cloud_firestore
from datetime import datetime


class Upload:
    def __init__(self, page, grid_size, cp, uid) -> None:
        self.page = page
        self.grid_size = grid_size
        self.cp = cp
        self.uid = uid
        self. diag_box = ft.AlertDialog(
            modal=True,
            title=ft.Text("Upload globally or privately?"),
            actions=[
                    ft.TextButton("Global", on_click=self.upload_anon),
                    ft.TextButton("Private", on_click=self.upload_private),
                    ft.TextButton("Cancel", on_click=self.upload_cancel)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def upload_anon(self, e):
        data_array = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                data_array.append(self.cp.shapes[(int)(j + i * self.grid_size)].paint.color)
        cloud_firestore.collection("users").document('anonymous').collection('images').document(datetime.now().isoformat()).set({"hex_array": data_array,
                                            "timestamp": firestore.SERVER_TIMESTAMP})
        if self.uid != 'anonymous':
            cloud_firestore.collection("users").document(self.uid).collection('images').document(datetime.now().isoformat()).set({"hex_array": data_array,
                                            "timestamp": firestore.SERVER_TIMESTAMP})
        self.diag_box.open = False
        self.page.update()

    def upload_private(self, e):
        data_array = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                data_array.append(self.cp.shapes[(int)(j + i * self.grid_size)].paint.color)
        cloud_firestore.collection("users").document(self.uid).collection('images').document(datetime.now().isoformat()).set({"hex_array": data_array,
                                            "timestamp": firestore.SERVER_TIMESTAMP})
        self.diag_box.open = False
        self.page.update()

    def upload_cancel(self, e):
        self.diag_box.open = False
        self.page.update()

    def upload_to_firebase(self, e):
        self.page.views[-1].controls.append(self.diag_box)
        self.diag_box.open=True
        self.page.update()
