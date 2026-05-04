from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route.todo_v1 import router


app = FastAPI()

app.include_router(router, prefix="/v1/todos", tags=["todo"])

origins = [
    "http://localhost:3000",
    "https://kind-ground-0d0ce4a0f.7.azurestaticapps.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

