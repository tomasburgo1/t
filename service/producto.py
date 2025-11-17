from typing import List, Dict, Any
from carrito import carrito, producto as ProductoModel
import psycopg

carrito_obj = carrito()

def listar_productos(cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
    return carrito_obj.mostrarProductos(cursor)

def agregar_producto(producto1: ProductoModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if not getattr(producto1, "nombre", None):
        raise ValueError("nombre de producto obligatorio")
    if producto1.precio is None or producto1.precio < 0:
        raise ValueError("precio inválido")
    return carrito_obj.agregarProducto(producto1, cursor)

def modificar_producto(id_producto: int, producto1: ProductoModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if id_producto <= 0:
        raise ValueError("id_producto inválido")
    if not getattr(producto1, "nombre", None) or producto1.precio < 0:
        raise ValueError("datos de producto inválidos")
    return carrito_obj.modificarProducto(id_producto, producto1, cursor)

def eliminar_producto(id_producto: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if id_producto <= 0:
        raise ValueError("id_producto inválido")
    return carrito_obj.eliminarProducto(id_producto, cursor)