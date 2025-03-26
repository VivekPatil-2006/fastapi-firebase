from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    """Return a simple Hello message"""
    return {"message": "Hello"}
