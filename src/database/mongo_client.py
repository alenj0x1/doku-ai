from pymongo import AsyncMongoClient
from dataclasses import asdict
from agent.models.context import ContextData
from utils import logger
import config

client = AsyncMongoClient(config.MONGO_URI)
db = client[config.MONGO_DATABASE]

contexts = db.contexts


async def find_context(name: str):
    logger.mongo_operation("Context", "FindOne", name)

    return await contexts.find_one({"name": name})


async def save_context(data: ContextData):
    data_asdic = asdict(data)
    result = await contexts.insert_one(data_asdic)

    logger.mongo_operation("Context", "Insert", result.inserted_id)
    return result.inserted_id
