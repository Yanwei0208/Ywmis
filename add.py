import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("public.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = [


{
  "name": "廖彥維",
  "role": "資管2b",
  "birth": 2004
}

]

collection_ref = db.collection("人選之人─造浪者")
for doc in docs:
  collection_ref.add(doc)

