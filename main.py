from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Path to your Firebase JSON key
firebase_admin.initialize_app(cred)
db = firestore.client()  # Firestore client

# Initialize FastAPI app
app = FastAPI()

@app.get("/user/{user_id}")
def get_user(user_id: str):
    """Fetch user data from Firestore using user_id"""
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        return {"user_id": user_id, **doc.to_dict()}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Run the FastAPI server using: uvicorn main:app --reload
