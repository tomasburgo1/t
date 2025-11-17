from fastapi import FastAPI
from routers import cliente as cliente_router, producto as producto_router, pedido as pedido_router
from carrito import carrito, getCursor

app = FastAPI(title="carrito de compra")

app.include_router(cliente_router.router)
app.include_router(producto_router.router)
app.include_router(pedido_router.router)

@app.get("/", tags=["root"], summary="Estado del servicio")
def health():
    return {"status": "ok", "endpoints": ["/clientes", "/productos", "/pedidos"]}