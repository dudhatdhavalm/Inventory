from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.dependencies import get_current_user
from core.config import settings
from fastapi.staticfiles import StaticFiles
from api.api_v1 import api_v1
from middlewares.auth_middleware import AuthMiddleWare

root_router = APIRouter()
app = FastAPI()

origins = [
    "https://d2webtech.com:85",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://193.203.161.156:85",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleWare)

@root_router.get("/")
def hello_world():
    return {"message": "Hello World!"}


app.include_router((api_v1.route_v1))
app.include_router(root_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
