from fastapi import FastAPI
from api.endpoints import registration, tasklist, file_data
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.include_router(registration.router)
app.include_router(tasklist.router)
app.include_router(file_data.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

