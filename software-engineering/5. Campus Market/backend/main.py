from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Campus Market", description="A simple app/website where university students can buy, sell, or exchange second-hand items (books, clothes, gadgets, etc.).")


MARKETPLACE = [
  {
    "name": "Wireless Mouse",
    "studentId": 101,
    "category": "Electronics",
    "description": "A smooth, ergonomic mouse with long battery life.",
    "price": 25
  },
  {
    "name": "Textbook: Data Structures",
    "studentId": 102,
    "category": "Books",
    "description": "Used textbook in good condition for CS classes.",
    "price": 40
  },
  {
    "name": "Mini Fridge",
    "studentId": 103,
    "category": "Appliances",
    "description": "Compact fridge, perfect for dorm rooms.",
    "price": 70
  }
]


class Auth(BaseModel):
    id: int
    name: str

class Item(BaseModel):
    name: str
    studentId: int
    category: str
    description: str
    price: float

@app.post("/auth", description="Login by student ID")
async def auth(student: Auth):
    return student

@app.get("/items", description="Available items, Search by name or category")
async def list_of_items(name: str = None, category: str = None):
    
    items = MARKETPLACE
    
    if category:
        items = [item for item in items if item.category.lower() == category]
    
    if name:
        items = [item for item in items if item.name.lower().include(name)]
    
    return items
    
@app.post("/list_item", description="Buy item")
async def add_item(item: Item):
    
    '''
    categories: books, clothers, gatgets
    '''
    
    MARKETPLACE.append(item)
    
    return MARKETPLACE
    
@app.post("/buy_item", description="Add your item")
async def buy_item(item: Item):
    
    
    MARKETPLACE.remove(item)
    
    return MARKETPLACE


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8899)

