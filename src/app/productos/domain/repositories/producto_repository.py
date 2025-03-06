from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.productos.domain.entities.producto import Producto

class ProductoRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Producto]:
        pass

    @abstractmethod
    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        pass

    @abstractmethod
    def create(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def update(self, producto_id: int, producto: Producto) -> Optional[Producto]:
        pass

    @abstractmethod
    def delete(self, producto_id: int) -> bool:
        pass