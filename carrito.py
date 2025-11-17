from typing import Generator, List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import psycopg
from pydantic import BaseModel

load_dotenv()
password = os.getenv("passwords")

url = f"postgresql://postgres.hulynjghadotkoueopbr:{password}@aws-1-us-east-2.pooler.supabase.com:6543/postgres"

def getCursor() -> Generator[psycopg.Cursor, None, None]:
    """
    Dependencia para FastAPI: cede un cursor y garantiza commit/close.
    Uso: Depends(getCursor) en routers.
    """
    conn = psycopg.connect(url, sslmode="require")
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def _rows_to_dicts(cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
    """
    Convierte resultado de cursor a lista de diccionarios.
    Si no hay filas devuelve lista vacía.
    """
    rows = cursor.fetchall()
    if not rows:
        return []
    cols: List[str] = []
    for col in cursor.description:
        # psycopg devuelve objetos con .name, pero soportamos también tuplas
        if hasattr(col, "name"):
            cols.append(col.name)
        else:
            cols.append(col[0])
    return [dict(zip(cols, row)) for row in rows]

def _row_to_dict(cursor: psycopg.Cursor) -> Optional[Dict[str, Any]]:
    """
    Convierte una sola fila (cursor.fetchone()) a diccionario, o None.
    IMPORTANTE: Debe llamarse justo después de ejecutar una query que retorne una fila.
    """
    row = cursor.fetchone()
    if not row:
        return None
    cols: List[str] = []
    for col in cursor.description:
        if hasattr(col, "name"):
            cols.append(col.name)
        else:
            cols.append(col[0])
    return dict(zip(cols, row))

# modelos (se exportan en minúscula para mantener compatibilidad con el rest del proyecto)
class cliente(BaseModel):
    nombre: str
    apellido: str
    edad: int

class producto(BaseModel):
    # usar 'nombre' para que coincida con la columna SQL "nombre"
    nombre: str
    precio: float

class pedido(BaseModel):
    id_pedido: int
    id_producto: int
    id_cliente: int

class carrito:
    def eliminarCliente(self, id_cliente: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s RETURNING id_cliente", (id_cliente,))
        row = _row_to_dict(cursor)
        if row:
            return {"mensaje": "Cliente eliminado", "id_cliente": row.get("id_cliente")}
        return {"mensaje": f"No existe cliente con id {id_cliente}"}

    def eliminarProducto(self, id_producto: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute("DELETE FROM producto WHERE id_producto = %s RETURNING id_producto", (id_producto,))
        row = _row_to_dict(cursor)
        if row:
            return {"mensaje": "Producto eliminado", "id_producto": row.get("id_producto")}
        return {"mensaje": f"No existe producto con id {id_producto}"}

    def eliminarPedido(self, id_pedido: int, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute("DELETE FROM pedido WHERE id_pedido = %s RETURNING id_pedido", (id_pedido,))
        row = _row_to_dict(cursor)
        if row:
            return {"mensaje": "Pedido eliminado", "id_pedido": row.get("id_pedido")}
        return {"mensaje": f"No existe pedido con id {id_pedido}"}

    def mostrarProductos(self, cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
        cursor.execute("SELECT * FROM producto ORDER BY id_producto")
        return _rows_to_dicts(cursor)

    def mostrarCliente(self, cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
        cursor.execute("SELECT * FROM cliente ORDER BY id_cliente")
        return _rows_to_dicts(cursor)

    def insertarPedido(self, pedido1: pedido, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute(
            "INSERT INTO pedido (id_pedido, id_cliente, id_producto) VALUES (%s, %s, %s) RETURNING id_pedido",
            (pedido1.id_pedido, pedido1.id_cliente, pedido1.id_producto)
        )
        row = _row_to_dict(cursor)
        return {"mensaje": "Pedido insertado", "id_pedido": row.get("id_pedido") if row else None}
    
    def mostrarPedido(self, cursor: psycopg.Cursor) -> List[Dict[str, Any]]:
        cursor.execute(
            "SELECT p.id_pedido, p.id_cliente, p.id_producto, c.nombre AS cliente_nombre, c.apellido AS cliente_apellido "
            "FROM pedido p LEFT JOIN cliente c ON p.id_cliente = c.id_cliente ORDER BY p.id_pedido"
        )
        return _rows_to_dicts(cursor)
    
    def modificarCliente(self, id_cliente: int, cliente1: cliente, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute(
            "UPDATE cliente SET nombre = %s, apellido = %s, edad = %s WHERE id_cliente = %s RETURNING id_cliente",
            (cliente1.nombre, cliente1.apellido, cliente1.edad, id_cliente)
        )
        row = _row_to_dict(cursor)
        if row:
            return {"mensaje": "Cliente actualizado", "id_cliente": row.get("id_cliente"), "cliente": cliente1.dict()}
        return {"mensaje": f"No existe cliente con id {id_cliente}"}

    def agregarProducto(self, producto1: producto, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute(
            "INSERT INTO producto (nombre, precio) VALUES (%s, %s) RETURNING id_producto",
            (producto1.nombre, producto1.precio)
        )
        row = _row_to_dict(cursor)
        return {"mensaje": "Producto agregado", "id_producto": row.get("id_producto") if row else None}

    def agregarCliente(self, cliente1: cliente, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute(
            "INSERT INTO cliente (nombre, apellido, edad) VALUES (%s, %s, %s) RETURNING id_cliente",
            (cliente1.nombre, cliente1.apellido, cliente1.edad)
        )
        row = _row_to_dict(cursor)
        return {"mensaje": f"Cliente agregado", "id_cliente": row.get("id_cliente") if row else None, "cliente": cliente1.dict()}

    def modificarProducto(self, id_producto: int, producto1: producto, cursor: psycopg.Cursor) -> Dict[str, Any]:
        cursor.execute(
            "UPDATE producto SET nombre = %s, precio = %s WHERE id_producto = %s RETURNING id_producto",
            (producto1.nombre, producto1.precio, id_producto)
        )
        row = _row_to_dict(cursor)
        if row:
            return {"mensaje": "Producto actualizado", "id_producto": row.get("id_producto"), "producto": producto1.dict()}
        return {"mensaje": f"No existe producto con id {id_producto}"}