from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .models import Product
from .schemas import ProductCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()