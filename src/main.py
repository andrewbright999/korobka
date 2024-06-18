import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from boxes.router import router as box_router
from auth.routers import router as auth_router
from pages.router import router as page_router
from auth.admin import create_admin


app = FastAPI(
    title="Коробка"
)


app.include_router(auth_router)
app.include_router(box_router)
app.include_router(page_router)


app.mount("/static", StaticFiles(directory="../static"), name="static")


# origins = [
#     # "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
#     allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
#                    "Authorization"],
# )


# @app.middleware("http")
# async def auth_middleware(request, call_next):
#     response = await call_next(request)
#     if response.status_code == 401:
#         return RedirectResponse(url="/login", status_code=302)



@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        pass
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
    await create_admin()


# @app.get("/")
# async def login_page():
#     return RedirectResponse(url="/login")
#  location / {
#                         proxy_pass http://127.0.0.1:8000; # указанный порт должен соответствовать порту сервера Uvicorn
#                         proxy_set_header Host $host; # передаем заголовок Host, содержащий целевой IP и порта сервера.
#                         proxy_set_header X-Real-IP $remote_addr; # передаем заголовок с IP-адресом пользователя
#                         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#                         proxy_set_header X-Forwarded-Proto $scheme;
#                         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # передаем всю последовательность адресов, через которые прошел запрос
#                 }
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)