
from fastapi import FastAPI
from app import models, schemas, utils
from app.database import engine 
from app.routers import post, user, auth, vote
from pydantic import BaseSettings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

#Done via alembic now so commented out line below
#models.Base.metadata.create_all(bind=engine)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)