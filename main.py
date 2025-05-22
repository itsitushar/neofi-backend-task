# from fastapi import FastAPI
# from pydantic import BaseModel


# class User(BaseModel):
#     username: str
#     email: str
#     password: str

# # from routers import auth, event  # we will create these later


# app = FastAPI(title="NeoFi Collaborative Event System")

# # # Register routes
# # app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
# # app.include_router(event.router, prefix="/api/events", tags=["Events"])


# @app.get("/")
# def root():
#     return {"message": "NeoFi backend is running"}


# @app.post("/api/auth/register")
# def register_user(user: User):
#     print(user.username)

#     response = {
#         "message": "Success",
#         "status_code": 200,
#         "auth_token": "438"
#     }

#     return response
from fastapi import FastAPI
from routers import auth, event
from routers import sharing
app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

app.include_router(sharing.router, prefix="/api/events", tags=["Sharing"])
app.include_router(event.router, prefix="/api/events", tags=["Events"])


@app.get("/")
def root():
    return {"message": "NeoFi backend is live!"}
