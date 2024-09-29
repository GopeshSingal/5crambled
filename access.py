import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
from PIL import Image

def initialize_firebase(credential_path):
    cred = credentials.Certificate(credential_path)
    firebase_admin.initialize_app(cred)
    print("Firebase Initialized")

def fetch_firestore_data(collection_name):
    db = firestore.client()
    collection_ref = db.collection(collection_name)
    doc_ref = collection_ref.document("M1cD6LX0A4tT2X6rvyQQ")
    doc = doc_ref.get()
    return doc.to_dict()["hex_array"]

def visualize_output_from_data(data):
    hex_array = data
    rgb_array = [(int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)) for hex_color in hex_array]
    image = Image.new("RGB", (32, 32))
    image.putdata(rgb_array)
    image.save('output.png')

if __name__ == "__main__":
    credential_path = 'secrets.json'
    initialize_firebase(credential_path)

    collection_name = 'images'
    data = fetch_firestore_data(collection_name)

    output = visualize_output_from_data(data)
