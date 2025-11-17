from fastapi import APIRouter, Depends, HTTPException, status
from carrito import producto as ProductoModel, getCursor, psycopg
import service

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/", summary="Listar productos")
def listar_productos(cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.listar_productos(cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Agregar producto")
def agregar_producto(producto1: ProductoModel, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.agregar_producto(producto1, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id_producto}", summary="Modificar producto")
def modificar_producto(id_producto: int, producto1: ProductoModel, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.modificar_producto(id_producto, producto1, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id_producto}", summary="Eliminar producto")
def eliminar_producto(id_producto: int, cursor: psycopg.Cursor = Depends(getCursor)):
    try:
        return service.eliminar_producto(id_producto, cursor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))