import streamlit as st
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.models import APIKey
from starlette.middleware.wsgi import WSGIMiddleware
from pydantic import BaseModel
import random
import string

# Datos de prueba generados automáticamente
USERS = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35},
]

PRODUCTS = [
    {"id": 101, "name": "Laptop", "price": 999.99},
    {"id": 102, "name": "Phone", "price": 499.99},
    {"id": 103, "name": "Headphones", "price": 199.99},
]

ORDERS = [
    {"id": 1001, "user_id": 1, "product_id": 101, "quantity": 1},
    {"id": 1002, "user_id": 2, "product_id": 103, "quantity": 2},
    {"id": 1003, "user_id": 3, "product_id": 102, "quantity": 1},
]

# API Key para autenticación
def get_api_keys():
    # Leer las claves de los secretos en Streamlit Cloud
    secrets = st.secrets["api_keys"]
    return secrets

API_KEYS = get_api_keys()

# FastAPI para manejar las APIs
app = FastAPI()

def get_api_key(api_key: str):
    if api_key not in API_KEYS.values():
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

class User(BaseModel):
    id: int
    name: str
    age: int

class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

@app.get("/users", response_model=list[User])
def get_users(api_key: APIKey = Depends(get_api_key)):
    return USERS

@app.get("/products", response_model=list[Product])
def get_products(api_key: APIKey = Depends(get_api_key)):
    return PRODUCTS

@app.get("/orders", response_model=list[Order])
def get_orders(api_key: APIKey = Depends(get_api_key)):
    return ORDERS

@app.get("/status")
def get_status(api_key: APIKey = Depends(get_api_key)):
    return {"status": "API is running"}

# Integración con Streamlit
st.set_page_config(page_title="API Endpoint App", page_icon="🔧")
st.title("API Endpoint App with API Key Authentication")

# Middleware para usar FastAPI en Streamlit
st.write("Esta aplicación expone varias APIs con autenticación de API Keys.")
st.write("Configura tus claves en los secretos de Streamlit Cloud en el formato:")
st.code("""
[api_keys]
demo_key = "12345"
""")

def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

if st.button("Generar nueva API Key"):
    new_key = generate_random_key()
    st.write("Agrega esta clave en los secretos de Streamlit Cloud para usarla:")
    st.code(new_key)

st.text("Puedes consultar los endpoints:")
st.code("/users", language="http")
st.code("/products", language="http")
st.code("/orders", language="http")
st.code("/status", language="http")

# Agregar FastAPI como middleware
st.write("El servidor FastAPI está integrado y ejecutándose.")
st.write("Usa herramientas como Postman para probar las APIs con tu API Key.")

# Montar la aplicación FastAPI
st_server = WSGIMiddleware(app)
