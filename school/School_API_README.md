
# **School API**

API ini dirancang untuk mempermudah pengelolaan data guru dan siswa dalam sistem manajemen sekolah. Dengan API ini, Anda dapat mengambil daftar guru beserta siswa yang diajar, serta membuat entri siswa baru dengan otentikasi menggunakan **API Key**.

---

## **Daftar Isi**
1. [Otentikasi](#otentikasi)
2. [Endpoint API](#endpoint-api)
   - [GET /school/api/teachers](#get-schoolapiteachers)
   - [POST /school/api/students](#post-schoolapistudents)
3. [Format Respon](#format-respon)
4. [Penanganan Error](#penanganan-error)

---

## **Otentikasi**
Untuk menggunakan API ini, Anda harus melakukan otentikasi dengan **API Key** yang dapat diperoleh dari admin. API key harus disertakan dalam header permintaan.

### **Cara Menggunakan API Key:**

- **Authorization Header (Bearer Token)**:
  ```plaintext
  Authorization: Bearer YOUR_API_KEY
  ```

- **Alternatif: X-Api-Key Header**:
  ```plaintext
  X-Api-Key: YOUR_API_KEY
  ```

Jika API key tidak ditemukan atau tidak valid, API akan mengembalikan respons **401 Unauthorized**.

---

## **Endpoint API**

### **GET /school/api/teachers**
Endpoint ini digunakan untuk mengambil daftar semua guru yang terdaftar, lengkap dengan informasi siswa yang mereka ajar.

#### **Metode:** `GET`

#### **Autentikasi:** Diperlukan (API Key)

#### **Contoh URL:** `/school/api/teachers`

**Respon:**
- **count**: Jumlah total guru yang tersedia
- **teachers**: Daftar guru yang diajarkan beserta informasi siswa yang mereka ajar:
  - **id**: ID guru
  - **name**: Nama guru
  - **phone**: Nomor telepon guru
  - **address**: Alamat guru
  - **email**: Email guru
  - **student_count**: Jumlah siswa yang diajar oleh guru tersebut
  - **students**: Data siswa yang diajar oleh guru tersebut:
    - **id**: ID siswa
    - **name**: Nama siswa
    - **class**: Nama kelas yang diikuti siswa
    - **active**: Status aktif siswa

**Contoh Respon:**
```json
{
  "count": 2,
  "teachers": [
    {
      "id": 1,
      "name": "John Doe",
      "phone": "123456789",
      "address": "123 Main St",
      "email": "johndoe@example.com",
      "student_count": 5,
      "students": [
        {
          "id": 1,
          "name": "Jane Smith",
          "class": "Math 101",
          "active": true
        },
        {
          "id": 2,
          "name": "Tom Brown",
          "class": "Math 101",
          "active": false
        }
      ]
    }
  ]
}
```

---

### **POST /school/api/students**
Endpoint ini digunakan untuk membuat data siswa baru di dalam sistem. Anda dapat menambahkan siswa baru dengan memberikan informasi terkait kelas dan guru yang mengajar.

#### **Metode:** `POST`

#### **Autentikasi:** Diperlukan (API Key)

#### **Contoh URL:** `/school/api/students`

**Field yang Diperlukan:**
- **name**: Nama siswa
- **class_id** atau **teacher_id**: Salah satu dari kelas atau guru harus disediakan.

**Field Opsional:**
- **enrollment_date**: Tanggal pendaftaran
- **email**: Email siswa
- **phone**: Nomor telepon siswa
- **tuition_fee**: Biaya sekolah siswa
- **currency_id**: Mata uang biaya sekolah

**Respon:**
- **id**: ID unik siswa yang baru dibuat
- **name**: Nama siswa
- **class_id**: ID kelas siswa (jika diberikan)
- **teacher_id**: ID guru siswa (jika diberikan)

**Contoh Permintaan:**
```json
{
  "name": "Alice Johnson",
  "class_id": 1,
  "teacher_id": 2,
  "email": "alice.johnson@example.com",
  "phone": "987654321",
  "tuition_fee": 500,
  "currency_id": 1
}
```

**Contoh Respon:**
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "class_id": 1,
  "teacher_id": 2
}
```

---

## **Format Respon**
API ini mengembalikan data dalam format **JSON**. Setiap respon berisi informasi sesuai dengan permintaan, atau pesan sukses/error sesuai dengan aksi yang diambil (untuk permintaan `GET` dan `POST`).

---

## **Penanganan Error**
API ini dirancang untuk menangani berbagai jenis kesalahan dengan memberikan pesan yang jelas dan mudah dipahami.

- **400 Bad Request**: Jika terdapat kesalahan dalam permintaan, seperti field yang hilang atau tidak valid.
- **404 Not Found**: Jika entitas yang diminta (kelas atau guru) tidak ditemukan.
- **401 Unauthorized**: Jika API key tidak valid atau tidak disertakan dalam permintaan.

**Contoh Respon Error:**
- **400 Bad Request** (Field Hilang):
  ```json
  {
    "error": "Field 'name' is required."
  }
  ```

- **404 Not Found** (Kelas Tidak Ditemukan):
  ```json
  {
    "error": "Class not found."
  }
  ```

- **401 Unauthorized** (API Key Tidak Valid):
  ```json
  {
    "error": "Unauthorized"
  }
  ```

---

Dengan API ini, Anda dapat dengan mudah mengelola dan mengakses data guru dan siswa secara efisien dan terstruktur. Pastikan untuk selalu menjaga keamanan API key Anda dan gunakan autentikasi yang tepat saat mengakses data.
