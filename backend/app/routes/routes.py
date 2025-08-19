from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.models import Product, Order, OrderItem
from typing import List
from pydantic import BaseModel, constr, confloat, conint
from datetime import datetime

router = APIRouter()

# Pydantic models
class ProductBase(BaseModel):
    name: constr(min_length=3, max_length=60)
    description: str | None = None
    price: confloat(ge=0.01)
    stock: conint(ge=0)
    category: str
    sku: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItemBase]
    coupon: str | None = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas
@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Produto removido com sucesso"}

@router.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Calcular total
    total = 0
    order_items = []
    
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {item.product_id} não encontrado")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {product.name}")
        
        total += product.price * item.quantity
        order_items.append({"product_id": product.id, "quantity": item.quantity, "price": product.price})
        
        # Atualizar estoque
        product.stock -= item.quantity
    
    # Aplicar cupom
    discount = 0
    if order.coupon == "ALUNO10":
        discount = total * 0.1
    
    total_final = total - discount
    
    # Criar pedido
    db_order = Order(
        total=total,
        discount=discount,
        total_final=total_final,
        coupon=order.coupon
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Criar itens do pedido
    for item in order_items:
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(db_order_item)
    
    db.commit()
    
    return {
        "message": "Pedido criado com sucesso",
        "order_id": db_order.id,
        "total": total,
        "discount": discount,
        "total_final": total_final
    }
