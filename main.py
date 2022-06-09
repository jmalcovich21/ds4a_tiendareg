from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from dash_app_new import dash_app_ds4a
import uvicorn

app = FastAPI()
app.mount("/tiendareg", WSGIMiddleware(dash_app_ds4a.server))

@app.get('/')
def index():
    return "Welcome to Tienda Registrada\'s Analytics Dashboard"

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)