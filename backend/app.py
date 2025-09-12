from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Allow FE port 5173
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/requirements")
def get_requirements():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "requirements.json")
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            requirements = json.load(f)
        return {"requirements": requirements, "count": len(requirements)}
    except FileNotFoundError:
        return {"requirements": [], "count": 0, "error": "Requirements file not found"}
