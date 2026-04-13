from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order
from app.schemas import OrderCreate, OrderResponse

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(
        item_name=order.item_name,
        quantity=order.quantity,
        price=order.price,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/orders", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    orders = db.execute(select(Order).order_by(Order.created_at.desc())).scalars().all()
    return orders


@router.delete("/orders/{order_id}", status_code=204)
def remove_order(order_id: str, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
