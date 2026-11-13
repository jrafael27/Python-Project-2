from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field


# app = FastAPI(title="Belajar FastAPI")
app = FastAPI(title="API produk")

@app.get("/")

def root():
    return {"pesan": "Halo dari FastAPI 2!"}

@app.get("/halo/{nama}")
def halo(nama:str):
    return {"pesan": f"Halo {nama}!"}

@app.get("/hitung/{a}/{b}")
def hitung(a:int, b:int):
    hasil = a + b
    return {"pesan": f"Hasil : {hasil}"}

class ProdukIn(BaseModel):
    nama: str = Field(min_length=1)
    harga: float = Field(gt=0)
    stok: int = Field(default = 0, ge=0)
    
class ProdukOut(ProdukIn):
    id: int
    
@app.get("/cari")
def cari(q: str="", limit: int=10):
    return {"kata_kunci": q, "limit" : limit}

@app.post("/produk-uji", response_model=ProdukOut, status_code=201)
def produk_uji(produk: ProdukIn):
    return {"id": 1, **produk.model_dump()}
    
db: list[dict] = []
next_id = 1

@app.post("/produk", response_model=ProdukOut, status_code = 201)
def buat(produk: ProdukIn):
    global next_id
    item = {"id": next_id, **produk.model_dump()}
    db.append(item)
    next_id += 1
    return item

@app.get("/produk", response_model=list[ProdukOut])
def daftar():
    return [item for item in db if item["harga"] >= 10000]

@app.get("/produk/{produk_id}", response_model=ProdukOut)
def detail(produk_id: int):
    for item in db:
        if item["id"] == produk_id:
            return item
    raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

@app.put("/produk/{produk_id}", response_model=ProdukOut)
def ubah(produk_id: int, produk: ProdukIn):
    for item in db:
        if item["id"] == produk_id:
            item.update(produk.model_dump())
            return item
    raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
   
@app.delete("/produk/{produk_id}", response_model=ProdukOut)
def hapus(produk_id: int):
    for i, item in enumerate(db):
        if item["id"] == produk_id:
            db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Produk tidak ditemukan")