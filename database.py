import logging
from datetime import datetime, timezone

log = logging.getLogger("db")


def now():
    return datetime.now(timezone.utc)


class Database:
    """MongoDB wrapper. If MONGO_URI is missing or connection fails, every
    method silently does nothing, so the bot never crashes because of the DB."""

    def __init__(self, uri, name):
        self.uri = uri
        self.name = name
        self.client = None
        self.db = None

    @property
    def enabled(self):
        return self.db is not None

    async def connect(self):
        if not self.uri:
            log.warning("MONGO_URI not set -> running WITHOUT database")
            return
        try:
            from motor.motor_asyncio import AsyncIOMotorClient

            client = AsyncIOMotorClient(self.uri, serverSelectionTimeoutMS=8000)
            await client.admin.command("ping")
            self.client = client
            self.db = client[self.name]
            await self.db.users.create_index("user_id", unique=True)
            await self.db.history.create_index([("user_id", 1), ("ts", -1)])
            await self.db.favorites.create_index([("user_id", 1), ("url", 1)], unique=True)
            log.info("MongoDB connected")
        except Exception:
            log.exception("MongoDB connection failed -> running WITHOUT database")
            self.client = None
            self.db = None

    async def close(self):
        if self.client:
            self.client.close()

    # ---------- users ----------
    async def add_user(self, user):
        if not self.enabled or not user:
            return
        try:
            await self.db.users.update_one(
                {"user_id": user.id},
                {
                    "$set": {"name": user.full_name, "username": user.username, "last_seen": now()},
                    "$setOnInsert": {"joined": now()},
                },
                upsert=True,
            )
        except Exception:
            log.exception("add_user failed")

    async def all_user_ids(self):
        if not self.enabled:
            return []
        return [d["user_id"] async for d in self.db.users.find({}, {"user_id": 1})]

    # ---------- history ----------
    async def add_history(self, user_id, title, url):
        if not self.enabled:
            return
        try:
            await self.db.history.insert_one(
                {"user_id": user_id, "title": title, "url": url, "ts": now()}
            )
        except Exception:
            log.exception("add_history failed")

    async def get_history(self, user_id, limit=10):
        if not self.enabled:
            return []
        cur = self.db.history.find({"user_id": user_id}).sort("ts", -1).limit(limit)
        return [d async for d in cur]

    # ---------- favorites ----------
    async def add_fav(self, user_id, title, url):
        if not self.enabled:
            return False
        try:
            await self.db.favorites.update_one(
                {"user_id": user_id, "url": url},
                {"$set": {"title": title, "ts": now()}},
                upsert=True,
            )
            return True
        except Exception:
            log.exception("add_fav failed")
            return False

    async def get_favs(self, user_id, limit=20):
        if not self.enabled:
            return []
        cur = self.db.favorites.find({"user_id": user_id}).sort("ts", -1).limit(limit)
        return [d async for d in cur]

    # ---------- stats ----------
    async def stats(self):
        if not self.enabled:
            return None
        return {
            "users": await self.db.users.count_documents({}),
            "songs": await self.db.history.count_documents({}),
            "favs": await self.db.favorites.count_documents({}),
        }
