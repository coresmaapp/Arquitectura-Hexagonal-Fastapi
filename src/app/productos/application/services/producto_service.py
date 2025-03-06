
from src.app.productos.domain.repositories.producto_repository import ProductoRepository
from src.app.productos.domain.entities.producto import Producto
from typing import List, Optional

class ProductoService:
    def __init__(self, repository: ProductoRepository):
        self.repository = repository

    def get_all_productos(self) -> List[Producto]:
        return self.repository.get_all()

    def get_producto_by_id(self, producto_id: int) -> Optional[Producto]:
        return self.repository.get_by_id(producto_id)

    def create_producto(self, producto: Producto) -> Producto:
        return self.repository.create(producto)
    
    def actualizar(self, producto_id: int, producto: Producto) -> Optional[Producto]:
        return self.repository.update(producto_id, producto)
    
    def eliminar(self, producto_id: int) -> bool:
        return self.repository.delete(producto_id)