from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

# Initialize Firebase (Prevent duplicate initialization)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # Path to Firebase JSON key
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Firestore client

# Initialize FastAPI app
app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    """Default route to check if FastAPI is running"""
    return {"message": "FastAPI is running!"}

@app.get("/user/{user_id}")
def get_user(user_id: str):
    """Fetch user data from Firestore subcollection 'users'"""
    try:
        # Assuming there's only one parent document, retrieve the first document's ID
        parent_docs = db.collections()  # Get all top-level collections
        parent_doc_id = None

        for collection in parent_docs:
            parent_doc_id = collection.id
            break  # Get the first parent document

        if not parent_doc_id:
            raise HTTPException(status_code=404, detail="No parent document found")

        # Fetch user data from the subcollection
        doc_ref = db.collection(parent_doc_id).document("users").collection(user_id).document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            return {"user_id": user_id, **doc.to_dict()}
        else:
            raise HTTPException(status_code=404, detail="User not found in subcollection")

    except FirebaseError as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

