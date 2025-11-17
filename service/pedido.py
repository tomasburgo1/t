from typing import List, Dict, Any
from carrito import carrito, pedido as PedidoModel
import psycopg

carrito_obj = carrito()

def listar_pedidos(cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
    return carrito_obj.mostrarPedido(cursor)

def insertar_pedido(pedido1: PedidoModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if pedido1.id_pedido <= 0 or pedido1.id_cliente <= 0 or pedido1.id_producto <= 0:
        raise ValueError("ids de pedido/cliente/producto deben ser > 0")
    return carrito_obj.insertarPedido(pedido1, cursor)

def eliminar_pedido(id_pedido: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if id_pedido <= 0:
        raise ValueError("id_pedido inválido")
    return carrito_obj.eliminarPedido(id_pedido, cursor)