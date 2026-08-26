from dh_deepdive.api.routers.produktion import produktion_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(produktion_router)


@app.get("/")
async def root():
    return {"message": "welcome to the deep dive from dh partners"}
