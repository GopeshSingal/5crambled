import json

import firebase_admin
from firebase_admin import firestore, credentials
from firebase import firebase

credentials_path = 'secrets.json'
cred = credentials.Certificate(credentials_path)

app = firebase_admin.initialize_app(cred)
cloud_firestore = firestore.client()

secrets = {}
with open(credentials_path) as f:
    secrets = json.load(f)

firebase_auth_url_template = 'https://identitytoolkit.googleapis.com/v1/{endpoint}?key=' + secrets['web_api_key']
