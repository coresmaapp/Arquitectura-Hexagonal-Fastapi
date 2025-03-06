from fastapi import APIRouter, Depends, HTTPException
from src.app.productos.application.services.producto_service import ProductoService
from src.app.productos.infrastructure.repositories.producto_repository_impl import ProductoRepositoryImpl
from src.app.productos.domain.entities.producto import Producto
from src.app.productos.domain.value_objects.nombre_producto import NombreProducto
from src.app.productos.domain.value_objects.precio import Precio
from typing import List

router = APIRouter()

def get_producto_service():
    repository = ProductoRepositoryImpl()
    return ProductoService(repository)

@router.get("/", response_model=List[Producto], summary="Obtener todos los productos")
def obtener_productos(service: ProductoService = Depends(get_producto_service)):
    return service.get_all_productos()

@router.get("/{producto_id}", response_model=Producto, summary="Obtener producto por ID")
def obtener_producto(producto_id: int, service: ProductoService = Depends(get_producto_service)):
    producto = service.get_producto_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=Producto, summary="Crear un producto")
def crear_producto( producto: Producto,
                   service: ProductoService = Depends(get_producto_service)):
    return service.create_producto(producto)


@router.put("/{producto_id}", response_model=Producto)
def update_producto(producto_id: int, producto: Producto, service: ProductoService = Depends(get_producto_service)):
    return service.actualizar(producto_id, producto)


@router.delete("/{producto_id}", response_model=dict)
def delete_producto(producto_id: int, service: ProductoService = Depends(get_producto_service)):
    eliminado = service.eliminar(producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"detail": "Producto eliminado correctamente"}