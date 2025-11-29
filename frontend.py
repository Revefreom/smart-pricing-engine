import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta

# --- AYARLAR ---
# Backend API adresimiz (Localhost)
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Otel Yönetim Paneli", page_icon="🏨", layout="wide")

st.title("🏨 Akıllı Otel ve Fiyatlandırma Sistemi")
st.markdown("---")

# --- SOL MENÜ (SIDEBAR): Rezervasyon Yapma ---
with st.sidebar:
    st.header("📝 Yeni Rezervasyon")
    
    # 1. Otel ve Oda Seçimi (Şimdilik manuel ID giriyoruz, ilerde listeden seçtirilebilir)
    room_id = st.number_input("Oda ID", min_value=1, value=1)
    email = st.text_input("Müşteri E-Posta", "musteri@ornek.com")
    
    # 2. Tarih Seçimi
    today = date.today()
    tomorrow = today + timedelta(days=1)
    check_in = st.date_input("Giriş Tarihi", today)
    check_out = st.date_input("Çıkış Tarihi", tomorrow)
    
    if st.button("Rezervasyonu Kaydet"):
        # API'ye gidecek veri paketi
        payload = {
            "room_id": room_id,
            "customer_email": email,
            "check_in": str(check_in),
            "check_out": str(check_out)
        }
        
        try:
            # Backend'e POST isteği atıyoruz
            response = requests.post(f"{API_URL}/bookings", json=payload)
            
            if response.status_code == 200:
                st.success("✅ Rezervasyon Başarıyla Oluşturuldu!")
                st.balloons() # Kutlama efekti :)
            elif response.status_code == 409:
                st.error("⚠️ HATA: O tarihlerde oda dolu! (Çakışma Var)")
            else:
                st.error(f"Bir hata oluştu: {response.text}")
                
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")

# --- ANA EKRAN: Analiz ve Raporlar ---

st.header("📊 Finansal Durum ve Doluluk Analizi")

# API'den Analiz Verisini Çek
try:
    response = requests.get(f"{API_URL}/analytics")
    
    if response.status_code == 200:
        data = response.json()
        
        # 1. Metrik Kartları (KPI)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Toplam Ciro", f"{data['total_revenue']:,.0f} ₺", delta="Bu Ay")
        col2.metric("Toplam Rezervasyon", data['total_bookings'])
        col3.metric("Ortalama İşlem", f"{data['average_price']:,.0f} ₺")
        col4.metric("En Popüler Oda", data['most_popular_room_type'])
        
        st.markdown("---")
        
        # 2. Grafikler
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Oda Tiplerine Göre Dağılım")
            # JSON verisini Pandas DataFrame'e çeviriyoruz
            df = pd.DataFrame(data['breakdown'])
            st.bar_chart(df.set_index("type"))
            
        with col_chart2:
            st.subheader("Veri Tablosu")
            st.dataframe(df, use_container_width=True)
            
    else:
        st.error("Veriler çekilemedi. Backend çalışıyor mu?")
        
except Exception as e:
    st.error(f"⚠️ API'ye bağlanılamadı. Lütfen 'uvicorn' sunucusunun çalıştığından emin olun.\nHata: {e}")