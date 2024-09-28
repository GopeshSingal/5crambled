import firebase_admin
from firebase_admin import firestore, credentials

credentials_path = 'secrets.json'
cred = credentials.Certificate(credentials_path)

app = firebase_admin.initialize_app(cred)
cloud_firestore = firestore.client()
