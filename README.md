# 🏨 Akıllı Otel Fiyatlandırma ve Rezervasyon Sistemi (Smart Hotel Pricing Engine)

Bu proje, otel rezervasyon süreçlerini yönetmek, dinamik fiyatlandırma yapmak ve doluluk oranlarını analiz etmek için geliştirilmiş **Full-Stack** bir uygulamadır.

**Backend:** FastAPI, PostgreSQL, SQLAlchemy (Dockerize edilmiş)
**Frontend:** Streamlit
**Analitik:** Pandas, SQL Aggregations

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)

## 🚀 Özellikler

### 1. Dinamik Fiyatlandırma Algoritması (Backend)
- Hafta sonları ve özel günlerde fiyatları otomatik günceller (`Business Logic`).
- `Race Condition` önlemek için **Database Locking (with_for_update)** ve **Transaction** yönetimi kullanır. Çifte rezervasyonu (Double Booking) %100 engeller.

### 2. Yönetim Paneli (Frontend)
- Anlık Ciro ve Rezervasyon takibi.
- Oda tiplerine göre doluluk grafikleri (Data Visualization).
- Kolay rezervasyon oluşturma arayüzü.

### 3. Teknik Altyapı
- **RESTful API:** Swagger UI ile dokümante edilmiş endpointler.
- **PostgreSQL:** İlişkisel veri tabanı tasarımı (Foreign Keys, Cascade Deletes).
- **Docker Compose:** Tek komutla tüm sistemi ayağa kaldırma.
- **Unit Tests:** `pytest` ile yazılmış, matematiksel doğruluğu kanıtlanmış test senaryoları.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Gereksinimler
- Docker & Docker Compose
- Python 3.12+

### 2. Projeyi İndirin
```bash
git clone [https://github.com/Revefreom/smart-pricing-engine.git](https://github.com/Revefreom/smart-pricing-engine.git)
cd otel-fiyatlandirma-projesi