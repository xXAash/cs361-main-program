from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import routers from the correct folder
from services.routers.auth_router import router as auth_router
from services.routers.class_router import router as class_router
from services.routers.event_router import router as event_router
from services.routers.task_router import router as task_router
from services.routers.term_router import router as term_router

from microservices.tag_add_router import router as tag_add_router

app = FastAPI()

# Include API routers
app.include_router(auth_router)
app.include_router(class_router)
app.include_router(event_router)
app.include_router(task_router)
app.include_router(term_router)

app.include_router(tag_add_router)

# CORS (for frontend JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
