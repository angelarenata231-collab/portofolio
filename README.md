# Angela Portfolio App

A modern Flask portfolio website for a UI/UX designer and frontend developer, with a public landing page and a protected admin dashboard for managing content.

## Features
- Modern responsive landing page
- Skill, project, experience, and certification sections
- Contact form with email fallback mock
- Admin dashboard with login
- SQLite database for local development

## Run locally

```bash
cd c:\Users\ASUS\ANGELA-PORTFOLIO
.\.venv\Scripts\python.exe app.py
```

Open: http://127.0.0.1:5000

## Admin login
- Username: admin
- Password: admin123

## Environment
Copy `.env.example` to `.env` and update values as needed.

## Menggunakan TiDB Cloud

Project ini tetap menggunakan Flask-SQLAlchemy. Untuk menghubungkan database ke
TiDB Cloud Starter/Essential:

1. Buat cluster TiDB Cloud dan database (misalnya `angela_portfolio`).
2. Buka **Connect** pada cluster, pilih koneksi **Public** dan **General**, lalu
   salin connection details. Buat/generate password bila diminta.
3. Salin `.env.example` menjadi `.env` dan isi `DATABASE_URL` dengan format:

   `mysql+pymysql://USERNAME:PASSWORD@HOST:4000/DATABASE?ssl_verify_cert=true&ssl_verify_identity=true`

   Ganti semua placeholder dengan detail dari TiDB Cloud. Jika username/password
   mengandung karakter khusus, URL-encode nilainya. Jangan commit atau membagikan
   `.env`.
4. Install dependency: `pip install -r requirements.txt`.
5. Cadangkan `portfolio.db`, lalu jalankan `python migrate_sqlite_to_tidb.py` untuk
   menyalin seluruh tabel dan data SQLite ke TiDB. Script ini mengganti isi tabel
   target dengan isi SQLite, jadi jalankan pada database TiDB baru/kosong.
6. Jalankan aplikasi dan verifikasi halaman publik serta dashboard admin.

Aplikasi menggunakan `pool_pre_ping` dan `pool_recycle=300` untuk membantu
menangani koneksi TiDB Cloud Starter yang dapat terputus setelah idle.
