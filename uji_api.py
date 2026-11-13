import requests

BASE_URL = "http://127.0.0.1:8000"


def cek(judul: str, res: requests.Response, status_harapan: int) -> None:
    """Cetak hasil request dan tandai OK/GAGAL sesuai status yang diharapkan."""
    tanda = "OK" if res.status_code == status_harapan else "GAGAL"
    print(f"\n[{tanda}] {judul}")
    print(f"  Status: {res.status_code} (harapan: {status_harapan})")

    if not res.content:
        isi = "(kosong)"
    else:
        try:
            isi = res.json()
        except ValueError:
            isi = res.text  # bukan JSON, tampilkan apa adanya
    print("  Isi   :", isi)


def main() -> None:
    # 1. CREATE: buat dua produk (harapan 201)
    res = requests.post(
        f"{BASE_URL}/produk",
        json={"nama": "Roti", "harga": 15000, "stok": 20},
        timeout=10,
    )
    cek("Buat produk Roti", res, 201)
    id_roti = res.json()["id"]

    res = requests.post(
        f"{BASE_URL}/produk",
        json={"nama": "Kue", "harga": 25000, "stok": 10},
        timeout=10,
    )
    cek("Buat produk Kue", res, 201)

    # 2. READ: ambil daftar (harapan 200)
    res = requests.get(f"{BASE_URL}/produk", timeout=10)
    cek("Ambil daftar produk", res, 200)

    # 3. READ: ambil satu produk (harapan 200)
    res = requests.get(f"{BASE_URL}/produk/{id_roti}", timeout=10)
    cek("Ambil detail Roti", res, 200)

    # 4. UPDATE: ubah harga (harapan 200)
    res = requests.put(
        f"{BASE_URL}/produk/{id_roti}",
        json={"nama": "Roti", "harga": 17000, "stok": 18},
        timeout=10,
    )
    cek("Ubah harga Roti", res, 200)

    # 5. DELETE: hapus (harapan 204, tanpa isi)
    res = requests.delete(f"{BASE_URL}/produk/{id_roti}", timeout=10)
    cek("Hapus Roti", res, 204)

    # 6. Ambil produk yang sudah dihapus (harapan 404)
    res = requests.get(f"{BASE_URL}/produk/{id_roti}", timeout=10)
    cek("Ambil Roti yang sudah dihapus", res, 404)

    # 7. Kirim data tidak valid (harapan 422)
    res = requests.post(
        f"{BASE_URL}/produk",
        json={"nama": "", "harga": -500},
        timeout=10,
    )
    cek("Buat produk dengan data tidak valid", res, 422)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Tidak bisa terhubung. Pastikan server FastAPI sudah berjalan.")