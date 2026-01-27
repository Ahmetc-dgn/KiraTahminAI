# 🚀 Proje Kurulum Rehberi (SQL Server Olmadan)

## ✅ Gereksinimler

Projenin çalışması için **SQL Server'a erişim GEREKMEZ**. Sadece şu dosyaların olması yeterli:

1. ✅ `trained_model_v2.pth` - Eğitilmiş model dosyası
2. ✅ `scaler.pkl` - Veri normalizasyon dosyası
3. ✅ Python bağımlılıkları (`requirements.txt`)

## 📦 Kurulum Adımları

### 1. Projeyi Git'ten Çekin

```bash
git clone <repository-url>
cd KiraTahminAI-main
```

### 2. Gerekli Dosyaları Kontrol Edin

Proje dizininde şu dosyaların olduğundan emin olun:

```
KiraTahminAI-main/
├── trained_model_v2.pth    ✅ Gerekli
├── scaler.pkl              ✅ Gerekli
├── requirements.txt        ✅ Gerekli
├── app.py
├── api/
│   └── routes.py
└── model.py
```

**ÖNEMLİ**: Eğer `scaler.pkl` dosyası yoksa:
- Modeli eğiten kişiden bu dosyayı isteyin
- VEYA `create_scaler.py` scriptini çalıştırın (ama bu SQL Server gerektirir)

### 3. Python Bağımlılıklarını Yükleyin

```bash
pip install -r requirements.txt
```

### 4. API'yi Başlatın

```bash
python app.py
```

API `http://localhost:5000` adresinde çalışacak.

## ⚠️ Önemli Notlar

### SQL Server Gereksiz!

- ✅ API çalışırken SQL Server'a **BAĞLANMAZ**
- ✅ Sadece model ve scaler dosyalarını kullanır
- ✅ Tahmin yapmak için veritabanına ihtiyaç yok

### Hangi Durumlarda SQL Server Gerekir?

SQL Server sadece şu durumlarda gerekir:

1. **Model eğitimi** (`train.py` çalıştırırken)
2. **Scaler oluşturma** (`create_scaler.py` çalıştırırken)
3. **Fiyat analizi** (`check_prices.py` çalıştırırken)

**API kullanımı için SQL Server GEREKMEZ!**

## 🐛 Sorun Giderme

### Hata: "Scaler dosyasi bulunamadi"

**Çözüm:**
1. `scaler.pkl` dosyasının proje dizininde olduğunu kontrol edin
2. Dosya yoksa, modeli eğiten kişiden isteyin
3. Git repository'de dosya varsa, `git pull` yapın

### Hata: "Model dosyasi bulunamadi"

**Çözüm:**
1. `trained_model_v2.pth` dosyasının proje dizininde olduğunu kontrol edin
2. Dosya yoksa, modeli eğiten kişiden isteyin

### Hata: "Module not found"

**Çözüm:**
```bash
pip install -r requirements.txt
```

## 📝 Özet

✅ **API kullanımı için**: SQL Server GEREKMEZ  
✅ **Sadece gerekli**: `trained_model_v2.pth` ve `scaler.pkl`  
✅ **Kurulum**: `pip install -r requirements.txt` ve `python app.py`

## 🎯 Test

API'nin çalıştığını test etmek için:

```bash
curl http://localhost:5000/api/test
```

Başarılı yanıt:
```json
{
  "message": "API çalışıyor!"
}
```

---

**Not**: Bu rehber, SQL Server erişimi olmayan geliştiriciler için hazırlanmıştır.

