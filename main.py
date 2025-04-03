from routes import all_routers

from fastapi import FastAPI
from db_connection import create_db_and_tables
from utils import jwt_util

app = FastAPI()

for router in all_routers:
    print(f"Connecting {router=}")
    app.include_router(router)

@app.on_event("startup")
def on_startup():
    jwt_util.generate_keys()
    create_db_and_tables()


@app.get("/")
def run_check():
    return {"status": "Server is running"}
