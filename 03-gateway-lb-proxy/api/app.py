import socket
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def raiz():
    return {"atendido_por": socket.gethostname()}