from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import models, database
from .database import engine

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root(request: Request, db: Session = Depends(database.get_db)):
    products = db.query(models.Product).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.post("/sell/{product_id}")
def sell_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product and product.quantity > 0:
        product.quantity -= 1
        
        category = product.category
        new_sale = models.Sale(
            product_id=product.id,
            product_name=product.name,
            category_brand=category.brand if category else "Unknown",
            price=category.price if category else 0,
            profit=category.profit if category else 0
        )
        db.add(new_sale)
        db.commit()
    return RedirectResponse(url="/", status_code=303)
