from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bot import bot_response, get_history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"msg": "Emperor protects!"}


@app.get("/question")
async def getConfig(q: str | None = None):
    if q is None:
        raise HTTPException(status_code=400, detail="Question is required")

    return {"answer": bot_response(q)}


@app.get("/history")
async def getHistory():
    return {"history": get_history()}
