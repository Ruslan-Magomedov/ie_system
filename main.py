from fastapi import FastAPI
from fastapi.responses import Response



app = FastAPI()



@app.get("/home")
def home():
    return Response(status_code=200)
