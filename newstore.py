from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import hashlib


DATABASE_URL = "postgresql://postgres:Bbbbbesokbbbbbesok3@192.168.1.57:5432/trial"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Aktifkan CORS agar bisa diakses dari Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan asal domain Angular kamu untuk keamanan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model yang dikirim dari Angular
# Model response
class dataResponse(BaseModel):
    status: str
    message: str
    data: list

class totalResponse(BaseModel):
    status: str
    message: str
    data: str

class dataId(BaseModel):
    id: int

class dataTotal(BaseModel):
    total: int

class FilePath(BaseModel):
    url: str
    path: str
    dbregion: str

@app.post("/items/", response_model=dataResponse)
def get_items():
    session = SessionLocal()
    try:
        # Query: Ambil 24 data dari tabel 'items'
        query = text("SELECT * FROM items LIMIT 24")
        result = session.execute(query).mappings().all()
        print(result)
        return {
            "status": "success",
            "message": "Items data received",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }
    finally:
        session.close()

@app.post("/colls/", response_model=dataResponse)
def get_items():
    session = SessionLocal()
    try:
        # Query: Ambil 24 data dari tabel 'items'
        query = text("SELECT * FROM collections LIMIT 24")
        result = session.execute(query).mappings().all()
        print(result)
        return {
            "status": "success",
            "message": "Items data received",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }
    finally:
        session.close()

@app.post("/detail/", response_model=dataResponse)
def get_items(data: dataId):
    id = data.id
    session = SessionLocal()
    try:
        # Query: Ambil 24 data dari tabel 'items'
        query = text("SELECT * FROM items Where id=" + str(id))
        result = session.execute(query).mappings().all()
        print(query)
        return {
            "status": "success",
            "message": "Items data received",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }
    finally:
        session.close()

@app.post("/total/", response_model=totalResponse)
def get_items(data: dataTotal):
    total = data.total
    session = SessionLocal()
    try:
        # Query: Ambil 24 data dari tabel 'items'
        timestamp_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # 2. Buat hash md5 dari timestamp tersebut
        hash_object = hashlib.md5(timestamp_str.encode())
        unique_hash = hash_object.hexdigest()

        # 3. INSERT ke database
        query = text("INSERT INTO public.transaction (total, uniquehash) VALUES (:total, :unique) RETURNING id")
        result = session.execute(query, {"total": total, "unique": unique_hash})
        session.commit()

        # 4. Ambil ID dari hasil insert
        inserted_id = result.fetchone()[0]

        return {
            "status": "success",
            "message": "Items data received",
            "data": inserted_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }
    finally:
        session.close()

@app.post("/detailtotal/", response_model=dataResponse)
def get_items(data: dataId):
    id = data.id
    session = SessionLocal()
    try:
        # Query: Ambil 24 data dari tabel 'items'
        query = text("SELECT * FROM transaction Where id=" + str(id))
        result = session.execute(query).mappings().all()
        print(query)
        return {
            "status": "success",
            "message": "Items data received",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }
    finally:
        session.close()
