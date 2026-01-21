from fastapi import FastAPI
from te_fast.api.v1 import api_router
from te_fast.core.lifespan import lifespan


app = FastAPI(
    title="My API",
    description="Test FastAPI",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", summary="Главная")
def main():
    return {"Hello": "World"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         app,
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )
