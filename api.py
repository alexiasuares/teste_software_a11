from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Base de dados fake
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00},
    {"id": 2, "nome": "Mouse", "preco": 80.00},
    {"id": 3, "nome": "Teclado", "preco": 150.00},
]


class Pedido(BaseModel):
    produto_id: int
    quantidade: int


class Checkout(BaseModel):
    produto_id: int
    quantidade: int


@app.get("/api/produtos")
def listar_produtos():
    return produtos


@app.get("/api/produtos/{id}")
def pegar_produto(id: int):
    for p in produtos:
        if p["id"] == id:
            return p
    return {"erro": "Produto não encontrado"}


@app.post("/api/pedido")
def criar_pedido(pedido: Pedido):
    return {
        "mensagem": "Pedido realizado com sucesso!",
        "pedido": pedido
    }


@app.post("/api/checkout")
def finalizar_compra(checkout: Checkout):
    # Verificar se o produto existe
    produto_encontrado = None
    for p in produtos:
        if p["id"] == checkout.produto_id:
            produto_encontrado = p
            break
    
    if not produto_encontrado:
        return {"erro": "Produto não encontrado"}
    
    # Calcular total
    total = produto_encontrado["preco"] * checkout.quantidade
    
    return {
        "mensagem": "Compra finalizada com sucesso!",
        "produto": produto_encontrado["nome"],
        "quantidade": checkout.quantidade,
        "valor_unitario": produto_encontrado["preco"],
        "total": total
    }