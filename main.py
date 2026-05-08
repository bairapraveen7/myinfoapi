from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route.profile_v1 import router

# load dotenv variables
load_dotenv()

app = FastAPI()


# app.include_router(router, prefix="/v1/todos", tags=["todo"])
app.include_router(router, prefix="/v1/profile", tags=["profile"])

origins = [
    "http://localhost:3000",
    "https://www.praveenbaira.com"
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

