from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    """Return a simple Hello message"""
    return {"message": "Hello"}
