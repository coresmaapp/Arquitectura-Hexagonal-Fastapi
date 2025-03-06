from src.app.productos.domain.repositories.producto_repository import ProductoRepository
from src.app.productos.domain.entities.producto import Producto
from src.infrastructure.postgresql.db_connection_factory import DatabaseConnectionFactory

from src.app.productos.domain.value_objects.nombre_producto import NombreProducto
from src.app.productos.domain.value_objects.precio import Precio

from typing import List, Optional


class ProductoRepositoryImpl(ProductoRepository):
    def get_all(self) -> List[Producto]:
        connection = DatabaseConnectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nombre, descripcion, precio, activo, imagen, stock   FROM producto_producto;")
                rows = cursor.fetchall()

                # Crear instancias de Producto utilizando el Value Object
                return [
                    Producto(
                        id=row[0],
                        nombre=NombreProducto(valor=row[1]),  # Value Object
                        descripcion=row[2],
                        precio=Precio(valor=row[3]),
                        activo=row[4],
                        imagen=row[5],
                        stock=row[6],
                    )
                    for row in rows
                ]
        finally:
            DatabaseConnectionFactory.release_connection(connection)

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        connection = DatabaseConnectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nombre, descripcion, precio, activo, imagen, stock  FROM producto_producto WHERE id = %s;", (producto_id,))
                row = cursor.fetchone()
                if row:
                    # Crear la instancia utilizando el Value Object
                    return Producto(
                        id=row[0],
                        nombre=NombreProducto(valor=row[1]),  # Value Object
                        descripcion=row[2],
                        precio=Precio(valor=row[3]),
                        activo=row[4],
                        imagen=row[5],
                        stock=row[6],
                    )
                return None
        finally:
            DatabaseConnectionFactory.release_connection(connection)

    def create(self,  producto: Producto) -> Producto:
        connection = DatabaseConnectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                # Validar el nombre usando el Value Object antes de la inserción
                nombre_producto_vo = NombreProducto(valor=producto.nombre)
                precio_producto_vo = Precio(valor=producto.precio)

                cursor.execute(
                    """
                    INSERT INTO producto_producto (nombre, descripcion, precio, activo, imagen, stock)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (
                        nombre_producto_vo.valor,
                        producto.descripcion,
                        precio_producto_vo.valor,
                        producto.activo,
                        producto.imagen,
                        producto.stock
                    )  # Pasamos el valor encapsulado
                )
                row = cursor.fetchone()  # Guarda el resultado en una variable

                producto_id = row[0]
                connection.commit()

                # Crear la entidad Producto utilizando el Value Object
                return Producto(
                    id=producto_id,
                    nombre=NombreProducto(valor=nombre_producto_vo.valor),  # Value Object
                    descripcion=producto.descripcion,
                    precio=Precio(valor=precio_producto_vo.valor),
                    activo=producto.activo,
                    imagen=producto.imagen,
                    stock=producto.stock,
                )
        finally:
            DatabaseConnectionFactory.release_connection(connection)

    def update(self, producto_id: int, producto: Producto) -> Optional[Producto]:
        connection = DatabaseConnectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE producto_producto
                    SET nombre = %s, descripcion = %s, precio = %s, activo = %s, imagen = %s, stock = %s
                    WHERE id = %s RETURNING id, nombre, descripcion, precio, activo, imagen, stock;
                """, (
                    producto.nombre.valor,  # Value Object
                    producto.descripcion,
                    producto.precio.valor,  # Value Object
                    producto.activo,
                    producto.imagen,
                    producto.stock,
                    producto_id # ID del producto a actualizar
                ))
                # Confirmar la transacción
                connection.commit()
                
                row = cursor.fetchone()
                if row:
                    return Producto(
                        id=row[0],
                        nombre=NombreProducto(valor=row[1]),  # Value Object
                        descripcion=row[2],
                        precio=Precio(valor=row[3]),
                        activo=row[4],
                        imagen=row[5],
                        stock=row[6],
                    )
                return None
        finally:
            DatabaseConnectionFactory.release_connection(connection)

    # Método para eliminar un producto por ID

    def delete(self, producto_id: int) -> bool:
        connection = DatabaseConnectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                # Ejecutar la consulta SQL de eliminación
                cursor.execute(
                    """
                    DELETE FROM producto_producto 
                    WHERE id = %s RETURNING id;
                    """,
                    (producto_id,)
                )

                # Confirmar la transacción
                connection.commit()

                # Verificar si se eliminó el registro
                row = cursor.fetchone()
                if row:
                    connection.commit()
                    return True  # Se eliminó correctamente
                return False  # No se encontró el producto con ese ID
        finally:
            DatabaseConnectionFactory.release_connection(connection)
