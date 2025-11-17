from typing import List, Dict, Any
from carrito import carrito, cliente as ClienteModel
import psycopg

carrito_obj = carrito()

def listar_clientes(cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
    return carrito_obj.mostrarCliente(cursor)

def agregar_cliente(nuevo: ClienteModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if not nuevo.nombre or not nuevo.apellido:
        raise ValueError("nombre y apellido son obligatorios")
    if nuevo.edad is None or nuevo.edad < 0:
        raise ValueError("edad debe ser >= 0")
    return carrito_obj.agregarCliente(nuevo, cursor)

def modificar_cliente(id_cliente: int, cliente1: ClienteModel, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if id_cliente <= 0:
        raise ValueError("id_cliente inválido")
    if not cliente1.nombre or not cliente1.apellido or cliente1.edad < 0:
        raise ValueError("datos de cliente inválidos")
    return carrito_obj.modificarCliente(id_cliente, cliente1, cursor)

def eliminar_cliente(id_cliente: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
    if id_cliente <= 0:
        raise ValueError("id_cliente inválido")
    return carrito_obj.eliminarCliente(id_cliente, cursor)