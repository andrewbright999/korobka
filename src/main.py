# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from boxes.router import router as box_router
from auth.routers import router as auth_router
from auth.admin import create_admin



app = FastAPI(
    title="Коробка"
)

# origins = [
#     # "http://localhost:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.middleware("http")
async def auth_middleware(request, call_next):
    response = await call_next(request)
    if response.status_code == 401:
        return RedirectResponse(url="/", status_code=302)
    return response



app.include_router(auth_router)
app.include_router(box_router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        pass
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await create_admin()


@app.get("/")
async def login_page():
    return HTMLResponse("<h1>Велкам нахуй</h1>")
    