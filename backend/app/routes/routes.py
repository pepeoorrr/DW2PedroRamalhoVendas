from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import SessionLocal
from ..models.models import Product, Pedido
from typing import List, Optional
from pydantic import BaseModel, constr, confloat, conint

router = APIRouter()

# Pydantic models
class ProdutoBase(BaseModel):
    nome: constr(min_length=3, max_length=60)
    descricao: Optional[str] = None
    preco: confloat(ge=0.01)
    estoque: conint(ge=0)
    categoria: str
    sku: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True

class ItemCarrinho(BaseModel):
    produto_id: int
    quantidade: int

class ConfirmarCarrinho(BaseModel):
    itens: List[ItemCarrinho]
    cupom: Optional[str] = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas
@router.get("/produtos", response_model=List[ProdutoResponse])
def get_produtos(
    search: Optional[str] = None,
    categoria: Optional[str] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    # Filtrar por busca
    if search:
        query = query.filter(or_(
            Product.nome.ilike(f"%{search}%"),
            Product.descricao.ilike(f"%{search}%")
        ))
    
    # Filtrar por categoria
    if categoria:
        query = query.filter(Product.categoria == categoria)
    
    # Ordenar
    if sort:
        if sort == "nome":
            query = query.order_by(Product.nome)
        elif sort == "nome_desc":
            query = query.order_by(Product.nome.desc())
        elif sort == "preco":
            query = query.order_by(Product.preco)
        elif sort == "preco_desc":
            query = query.order_by(Product.preco.desc())
    
    return query.all()

@router.post("/produtos", response_model=ProdutoResponse)
def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = Product(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def update_produto(produto_id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = db.query(Product).filter(Product.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for key, value in produto.dict().items():
        setattr(db_produto, key, value)
    
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.delete("/produtos/{produto_id}")
def delete_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(Product).filter(Product.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return {"message": "Produto removido com sucesso"}

@router.post("/carrinho/confirmar")
def confirmar_carrinho(carrinho: ConfirmarCarrinho, db: Session = Depends(get_db)):
    total = 0
    
    # Validar e processar itens
    for item in carrinho.itens:
        produto = db.query(Product).filter(Product.id == item.produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.produto_id} não encontrado"
            )
        
        if produto.estoque < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para o produto: {produto.nome}"
            )
        
        total += produto.preco * item.quantidade
    
    # Aplicar cupom
    if carrinho.cupom == "ALUNO10":
        total = total * 0.9  # 10% de desconto
    elif carrinho.cupom:
        raise HTTPException(
            status_code=400,
            detail="Cupom inválido"
        )
    
    # Criar pedido
    pedido = Pedido(total_final=total)
    db.add(pedido)
    
    # Atualizar estoque
    for item in carrinho.itens:
        produto = db.query(Product).filter(Product.id == item.produto_id).first()
        produto.estoque -= item.quantidade
    
    db.commit()
    
    return {
        "message": "Pedido confirmado com sucesso",
        "pedido_id": pedido.id,
        "total_final": total
    }
