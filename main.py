from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import services, models, schemas
from db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/apps/", response_model=list[schemas.MobileApp])
async def get_all_apps():
    return await services.get_apps()

@app.get("/apps/{id}", response_model=schemas.MobileApp)
async def get_app_by_id(id: str):
    app = await services.get_app(id)
    if app:
        return app
    raise HTTPException(status_code=404, detail="Invalid app id Provided")

@app.post("/apps/", response_model=schemas.MobileApp)
async def create_new_app(app: schemas.MobileAppCreate):
    return await services.create_app(app)

@app.put("/apps/{id}", response_model=schemas.MobileApp)
async def update_app(app: schemas.MobileAppCreate, id: str):
    db_update = await services.update_app(app, id)
    if not db_update:
        raise HTTPException(status_code=404, detail="App not found")
    return db_update

@app.delete("/apps/{id}", response_model=schemas.MobileApp)
async def delete_app(id: str):
    delete_entry = await services.delete_app(id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404, detail="App Not Found")

@app.get("/")
def root():
    return {"message": "Mobile App API running"}

# Kubernetes health checks
@app.get("/health/liveness")
def liveness():
    """Liveness probe simply returns ok to indicate the app is running."""
    return {"status": "ok"}

@app.get("/health/readiness")
def readiness(db: Session = Depends(get_db)):
    """Readiness probe checks that the application can connect to the database.
    If the database query fails we raise a 503 so Kubernetes will treat the
    pod as not ready and avoid sending traffic.
    """
    try:
        # simple lightweight query
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ready"}