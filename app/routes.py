from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db, get_menu_db
from app.models import Menu, Order
from app.schemas import MenuCreate, MenuResponse, OrderCreate, OrderResponse

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


@router.post("/menus", response_model=MenuResponse, status_code=201)
def add_menu(menu: MenuCreate, db: Session = Depends(get_menu_db)):
    new_menu = Menu(
        name=menu.name,
        description=menu.description,
        price=menu.price,
        category=menu.category,
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


@router.get("/menus", response_model=list[MenuResponse])
def list_menus(db: Session = Depends(get_menu_db)):
    menus = db.execute(select(Menu).order_by(Menu.created_at.desc())).scalars().all()
    return menus


@router.delete("/menus/{menu_id}", status_code=204)
def remove_menu(menu_id: str, db: Session = Depends(get_menu_db)):
    menu = db.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(menu)
    db.commit()
