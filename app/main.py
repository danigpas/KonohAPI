from fastapi import FastAPI
from .routers import characters, clans, jutsus
app = FastAPI()

app.include_router(characters.router)

@app.get('/')
async def hello():
    return {'Hello ninjas!'}