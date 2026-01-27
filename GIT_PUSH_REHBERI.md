# 📤 Git Push Rehberi - Arkadaşınız İçin Hazırlık

## ✅ Git'e Push Etmeden Önce Kontrol Listesi

### 1. Gerekli Dosyaların Varlığını Kontrol Edin

Şu dosyaların proje dizininde olduğundan emin olun:

```bash
✅ trained_model_v2.pth    # Eğitilmiş model (MUTLAKA GEREKLİ)
✅ scaler.pkl              # Veri normalizasyon dosyası (MUTLAKA GEREKLİ)
✅ app.py
✅ api/routes.py
✅ model.py
✅ requirements.txt
✅ README.md
✅ KURULUM.md
```

### 2. Git'e Eklenecek Dosyalar

**ÖNEMLİ**: `trained_model_v2.pth` ve `scaler.pkl` dosyalarını **MUTLAKA** Git'e ekleyin!

```bash
# Git'e ekle
git add trained_model_v2.pth
git add scaler.pkl
git add app.py
git add api/
git add model.py
git add requirements.txt
git add README.md
git add KURULUM.md
git add test_api.py

# Commit
git commit -m "KiraTahminAI API - SQL Server gerektirmeden çalışır hale getirildi"

# Push
git push
```

### 3. .gitignore Kontrolü

Eğer `.gitignore` dosyanız varsa, şu satırların **OLMAMASI** gerekiyor:

```
# BUNLAR .gitignore'da OLMAMALI:
# trained_model_v2.pth
# scaler.pkl
```

Bu dosyalar Git'e eklenmeli çünkü arkadaşınızın bunlara ihtiyacı var!

## 👥 Arkadaşınızın Yapması Gerekenler

### 1. Projeyi Git'ten Çekin

```bash
git clone <repository-url>
cd KiraTahminAI-main
```

### 2. Dosyaları Kontrol Edin

```bash
# Bu dosyaların mevcut olduğundan emin olun:
ls trained_model_v2.pth
ls scaler.pkl
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. API'yi Başlatın

```bash
python app.py
```

### 5. Test Edin

Başka bir terminal'de:

```bash
python test_api.py
```

VEYA tarayıcıda: `http://localhost:5000/api/test`

## ✅ Sonuç

Arkadaşınız:
- ✅ SQL Server'a **BAĞLANMAZ**
- ✅ Sadece model ve scaler dosyalarını kullanır
- ✅ Direkt API'yi çalıştırabilir
- ✅ Frontend ile kullanabilir

## ⚠️ Önemli Notlar

1. **Model dosyası büyük olabilir** (birkaç MB). Git LFS kullanmayı düşünebilirsiniz ama zorunlu değil.

2. **Scaler dosyası küçüktür** (birkaç KB), sorun olmaz.

3. **SQL Server GEREKMEZ** - API çalışırken hiçbir veritabanı bağlantısı yapılmaz.

4. **Sadece tahmin için** - Model eğitimi veya scaler oluşturma için SQL Server gerekir, ama API kullanımı için GEREKMEZ.

## 🎯 Özet

**Git'e push ederken:**
- ✅ `trained_model_v2.pth` ekle
- ✅ `scaler.pkl` ekle
- ✅ Tüm kod dosyalarını ekle

**Arkadaşınız:**
- ✅ Git pull yapar
- ✅ `pip install -r requirements.txt` yapar
- ✅ `python app.py` ile başlatır
- ✅ **SQL Server OLMADAN** kullanır!

---

**Başarılar! 🚀**

