
# Medmon User Service

Project ini digunakan sebagai service yang menangani service user aplikasi Online Media Monitoring


## Tech

**Database:** MongoDB (Default)

**Server:** FastAPI

**Python Version:** 3.12.3


## Installation

Install project dengan command berikut

```python
  # Masuk ke ke service yang akan diinstall
  cd /example-service

  # Install dependencies
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

  # Running project
  uvicorn app.main:app --reload
```
## Folder Structure

**```app/api/dependencies```**: Berisi inisialisasi dependency (dependency injection), seperti:
- Pembuatan instance repository dan service
- Integrasi dengan FastAPI Depends
- Wiring antar komponen

**```app/api/routes```**: Berisi layer HTTP (endpoint API), meliputi:
- Definisi route
- Mapping request → service
- Mapping response ke client

**```app/core```**:
Berisi komponen inti aplikasi:
- **```config.py```**: Konfigurasi global yang berasal dari .env ataupun konstanta
- **```database.py```**: Koneksi ke database
- **```exception.py```**: Exception handler untuk standarisasi error response
- **```http_client.py```**: Async HTTP Client untuk melakukan request ke API external
- **```lifespan.py```**: Fungsi yang dijalankan ketika startup service
- **```logger.py```**: Format logging supaya terstandarisasi
- dll.

**```app/dto```**: Berisi Data Transfer Object (DTO) untuk:
- Validasi request dari client
- Format data masuk ke service
- Schema khusus input/output API

**```app/enums```**: Berisi definisi enum yang digunakan di service.

**```app/factories```**: Berisi inisiasi dependency service secara default.

**```app/integrations```**: Berisi client untuk integrasi ke external service / third-party API, seperti:
- Telegram
- Email service
- Layanan eksternal lainnya

**```app/middlewares```**: Berisi middleware untuk:
- Autentikasi (misalnya: ambil user dari token)
- Handling error global
- Logging request/response
- Kebutuhan cross-cutting lainnya

**```app/models```**: Berisi domain model / schema utama aplikasi, biasanya merepresentasikan:
- Struktur data di database
- Entity utama (contoh: User)

**```app/repositories```**: Berisi layer akses data (data access layer), seperti:
- Query database (find, insert, update, delete)
- Mapping data ke model
- Abstraksi terhadap database

**```app/services```**: Berisi business logic / aturan bisnis aplikasi, seperti:
- Validasi kompleks
- Proses utama aplikasi
- Orchestration antar repository dan integration

**```app/utils```**: Berisi helper / utility function yang reusable, seperti:
- Formatter
- Helper umum
- Fungsi utilitas lainnya


## Coding Guidelines

**1. Layer Responsibility (WAJIB DIPATUHI):**
Setiap layer memiliki tanggung jawab yang jelas dan tidak boleh dilanggar:
| Layer        | Responsibility               |
| ------------ | ---------------------------- |
| api/routes   | Handle HTTP request/response |
| services     | Business logic               |
| repositories | Akses database               |
| integrations | External API                 |
| models       | Domain model                 |
| dto          | Request/response schema      |

**❌ DILARANG:**
- Query database di service langsung
- Call external API di repository
- Logic bisnis di routes

**CONTOH BENAR:**
```python
# route → service → repo
@router.get("/")
async def get_users(service: UserService = Depends(...)):
    users,pagination = await service.get_users()
    return {
        "users":users,
        "pagination":pagination,
    }
```

**2. Service Layer Rules:**
- Semua business logic harus di service
- Service tidak boleh tahu FastAPI (Depends, Request, dll)
- Service hanya menerima:
    - DTO
    - Primitive types
    - Domain model

```python
def create_user(request: Request):  # ❌ SALAH
```
```python
def create_user(data: UserCreate):  # ✅ BENAR
```

**3. Repository Rules:**
- Hanya bertanggung jawab untuk:
    - Query database
    - Mapping data ke model
- Tidak boleh ada:
    - Business logic
    - Validasi kompleks

```python
if user.role != "admin":  # ❌ SALAH
```
```python
return await collection.find_one(...) # ✅ BENAR
```

**4. Integration Rules:** 
- Digunakan untuk komunikasi dengan external service:
    - Telegram
    - Email
    - API lain
- Rules
    - Jangan raise exception ke atas (log saja)
    - Jangan berisi business logic    

```python
# CONTOH
async def send_message(...):
    try:
        ...
    except Exception:
        logger.error(...)
```

**5. Dependency Injection Rules:**
- Gunakan Depends() hanya di:
    - Routes
    - Dependency function

```python
class Service:
    def __init__(self, repo = Depends(...)):  # ❌ SALAH
```
```python
def get_service():
    return Service(repo) # ✅ BENAR
```

**6. DTO vs Model:**
| Type  | Fungsi                       |
| ----- | ---------------------------- |
| DTO   | validasi request/response    |
| Model | representasi domain/database |

**7. Clean Code Principles:**
- Gunakan nama variabel yang jelas
- Hindari penamaan variabel 1 huruf (Contoh i, j, dll)
- Hindari function terlalu panjang
- Gunakan nama function dengan prefix underscore (_) di fungsi dalam class, jika hanya digunakan internal class saja.
    ```python
    class UserRepository:
        def _to_model(...):
            pass
        
        def find_all():
            pass
    ```
- 1 function = 1 responsibility

**8. Error Handling:**
- Gunakan custom exception untuk business error
- Gunakan global handler untuk unhandled error
- Jangan kirimkan error message internal ke response HTTP

```python
# CONTOH
if not user:
    raise DataNotFoundException()
```

**9. Logging Rules:**
- Gunakan logging, bukan print
- Gunakan:
    - logger.info → informasi umum
    - logger.error → error biasa
    - logger.exception → error dengan stack trace

**10. Async Rules:**
- Gunakan async/await untuk:
    - Database
    - External API

```python
requests.post(...)  # ❌ SALAH -> blocking
```
```python
await http_client.post(...) # ✅ BENAR
```

**11. Object Lifecycle:**
- Gunakan singleton untuk:
    - HTTP client
    - Service
- Hindari create object berulang

**12. Security Rules:**
- Jangan pernah log:
    - Password
    - Token
- Selalu hash password

**13. Testing Friendly Code:**
- Hindari hard dependency
- Gunakan constructor injection

**14. Naming Convention:**
- File: snake_case
- Class: PascalCase
- Function: snake_case
- Constant: UPPER_CASE

**15. General Principles:**
- Kode harus mudah dibaca
- Hindari overengineering
- Pisahkan concern dengan jelas
- Tambahkan ke requirements.txt jika ada dependency baru yang diinstall
- Tambahkan komentar yang menjelaskan proses jika businness logic cukup panjang

