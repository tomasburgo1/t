from fastapi import APIRouter, Depends, HTTPException, status
from carrito import pedido as PedidoModel, getCursor, psycopg
import service

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/", summary="Listar pedidos")
def listar_pedidos(cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.listar_pedidos(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Insertar pedido")
def insertar_pedido(pedido1: PedidoModel, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.insertar_pedido(pedido1, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id_pedido}", summary="Eliminar pedido")
def eliminar_pedido(id_pedido: int, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.eliminar_pedido(id_pedido, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))