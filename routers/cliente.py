from fastapi import APIRouter, Depends, HTTPException, status
from carrito import cliente as ClienteModel, getCursor, psycopg
import service

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("/", summary="Listar clientes")
def listar_clientes(cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.listar_clientes(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Agregar cliente")
def agregar_cliente(nuevo: ClienteModel, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.agregar_cliente(nuevo, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id_cliente}", summary="Modificar cliente")
def modificar_cliente(id_cliente: int, cliente1: ClienteModel, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.modificar_cliente(id_cliente, cliente1, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id_cliente}", summary="Eliminar cliente")
def eliminar_cliente(id_cliente: int, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.eliminar_cliente(id_cliente, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))