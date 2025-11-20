from fastapi import FastAPI
from .routers import characters, clans, jutsus
app = FastAPI()

app.include_router(characters.router)
app.include_router(clans.router)
app.include_router(jutsus.router)

@app.get('/')
async def hello():
    return {'Hello ninjas!'}