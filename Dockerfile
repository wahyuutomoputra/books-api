# Gunakan image dasar Python
FROM python:3.10-slim

# Setel direktori kerja
WORKDIR /app

# Salin file requirement dan instal dependensi
COPY requirements.txt .

# Instal dependensi dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh aplikasi ke dalam container
COPY . .

# Setel variabel lingkungan untuk database dan Redis
ENV DATABASE_URL=mysql://user:password@mysql:3306/mydatabase
ENV REDIS_URL=redis://redis:6379

# Expose port aplikasi
EXPOSE 8000

# Jalankan aplikasi FastAPI menggunakan Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
