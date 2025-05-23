from fastapi import FastAPI
from routers import auth, event
from routers import sharing
app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

app.include_router(sharing.router, prefix="/api/events", tags=["Sharing"])
app.include_router(event.router, prefix="/api/events", tags=["Events"])
app.include_router(event.router, prefix="/api/events", tags=["Diff"])


@app.get("/")
def root():
    return {"message": "NeoFi backend is live!"}
