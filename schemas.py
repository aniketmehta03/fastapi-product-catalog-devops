from pydantic import BaseModel

class MobileAppBase(BaseModel):
    name: str
    developer: str
    description: str
    version: int
    
class MobileAppCreate(MobileAppBase):
    pass

class MobileApp(MobileAppBase):
    id: str
    
    class Config:
        from_attributes = True
