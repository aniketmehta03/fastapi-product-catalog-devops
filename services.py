from models import MobileApp
from schemas import MobileAppCreate

async def create_app(data: MobileAppCreate):
    app_instance = MobileApp(**data.model_dump())
    await app_instance.insert()
    return app_instance

async def get_apps():
    return await MobileApp.find_all().to_list()

async def get_app(app_id: str):
    return await MobileApp.get(app_id)

async def update_app(data: MobileAppCreate, app_id: str):
    app = await MobileApp.get(app_id)
    if app:
        for key, value in data.model_dump().items():
            setattr(app, key, value)
        await app.save()
        return app

async def delete_app(app_id: str):
    app = await MobileApp.get(app_id)
    if app:
        await app.delete()
        return app
