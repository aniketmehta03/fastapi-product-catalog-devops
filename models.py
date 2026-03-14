from beanie import Document

class MobileApp(Document):
    name: str
    description: str
    developer: str
    version: int
