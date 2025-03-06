from fastapi import FastAPI
from src.app.productos.infrastructure.routers.producto_router import router as producto_router
from src.infrastructure.postgresql.db_connection_factory import DatabaseConnectionFactory

app = FastAPI(title="API REST CRUD con FastAPI(Arquitectura Hexagonal) con PostgreSQL sin ORM")

@app.on_event("startup")
def startup_event():
    DatabaseConnectionFactory.initialize()

@app.on_event("shutdown")
def shutdown_event():
    DatabaseConnectionFactory.close_pool()

app.include_router(producto_router, prefix="/productos", tags=["Productos"])

@app.get("/")
def root():
    return {"message": "API sin ORM usando FastAPI"}