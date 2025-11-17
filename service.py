from typing import List, Dict, Any
from carrito import carrito, cliente as ClienteModel, producto as ProductoModel, pedido as PedidoModel, psycopg

carrito_obj = carrito()


def listar_clientes(cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
    return carrito_obj.mostrarCliente(cursor)

def agregar_cliente(nuevo: ClienteModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.agregarCliente(nuevo, cursor)

def modificar_cliente(id_cliente: int, cliente1: ClienteModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.modificarCliente(id_cliente, cliente1, cursor)

def eliminar_cliente(id_cliente: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.eliminarCliente(id_cliente, cursor)

def listar_productos(cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
    return carrito_obj.mostrarProductos(cursor)

def agregar_producto(producto1: ProductoModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.agregarProducto(producto1, cursor)

def modificar_producto(id_producto: int, producto1: ProductoModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.modificarProducto(id_producto, producto1, cursor)

def eliminar_producto(id_producto: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.eliminarProducto(id_producto, cursor)

def listar_pedidos(cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
    return carrito_obj.mostrarPedido(cursor)

def insertar_pedido(pedido1: PedidoModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.insertarPedido(pedido1, cursor)

def eliminar_pedido(id_pedido: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
    return carrito_obj.eliminarPedido(id_pedido, cursor)