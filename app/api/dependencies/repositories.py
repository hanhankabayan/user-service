from typing import Annotated

from app.core.database import database
from app.repositories.mongo.project import MongoProjectRepository
from app.repositories.mongo.user import MongoUserRepository
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

# --- medmon db ---
MedmonDBDependency = Annotated[AsyncIOMotorDatabase, Depends(database.get_medmon_db)]


# --- user ---
def get_user_repo(db: MedmonDBDependency):
    return MongoUserRepository(db)


UserRepoDependency = Annotated[MongoUserRepository, Depends(get_user_repo)]


# --- project ---
def get_project_repo(db: MedmonDBDependency):
    return MongoProjectRepository(db)


ProjectRepoDependency = Annotated[MongoProjectRepository, Depends(get_project_repo)]
