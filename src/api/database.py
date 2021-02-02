from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from .config import settings


class Database:
    def __init__(self, engine: AIOEngine):
        self.engine = engine


motor_client = AsyncIOMotorClient(settings.database)
engine = AIOEngine(motor_client=motor_client, database=settings.database_name)
db = Database(engine)
