from pydantic import BaseModel, Field
from src.app.productos.domain.value_objects.nombre_producto import NombreProducto
from src.app.productos.domain.value_objects.precio import Precio

class Producto(BaseModel):
    id: int = Field(..., description="ID del producto")
    nombre: NombreProducto
    descripcion: str
    precio: Precio
    activo: bool
    imagen: str
    stock: int

