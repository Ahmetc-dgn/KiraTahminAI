# 🏠 KiraTahminAI - İstanbul Kira Fiyat Tahmin Sistemi

## 📋 Proje Özeti

KiraTahminAI, makine öğrenmesi kullanarak İstanbul'daki ev kiralarını tahmin eden bir web uygulamasıdır. Flask backend API ve Angular frontend ile geliştirilmiştir. Sistem, ev özelliklerine (metrekare, oda sayısı, konum, bina tipi vb.) göre gerçekçi kira fiyatları tahmin eder.

## 🎯 Özellikler

- ✅ **AI Destekli Tahmin**: PyTorch ile eğitilmiş derin öğrenme modeli
- ✅ **İstanbul Piyasası**: Gerçekçi İstanbul kira fiyatları (8k - 200k TL/ay)
- ✅ **Özellik Bazlı Hesaplama**: Metrekare, konum, bina tipi, garaj, bahçe gibi faktörler
- ✅ **Modern Web Arayüzü**: Angular ile responsive ve kullanıcı dostu tasarım
- ✅ **RESTful API**: Flask ile güvenli ve hızlı API servisi

## 🏗️ Proje Yapısı

```
KiraTahminAI-main/
├── api/
│   ├── __init__.py
│   └── routes.py          # API endpoint'leri
├── app.py                  # Flask uygulama ana dosyası
├── model.py                # PyTorch MLP model mimarisi
├── dataset.py               # Veri yükleme ve preprocessing
├── train.py                # Model eğitim scripti
├── create_scaler.py        # Scaler oluşturma scripti
├── check_prices.py         # Fiyat analiz scripti
├── trained_model_v2.pth    # Eğitilmiş model dosyası
├── scaler.pkl              # Veri normalizasyon scaler'ı
├── requirements.txt         # Python bağımlılıkları
└── README.md               # Bu dosya
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

- Python 3.8+
- Node.js 16+ (sadece frontend için)
- npm veya yarn (sadece frontend için)

**⚠️ ÖNEMLİ**: SQL Server **GEREKMEZ**! API çalışması için sadece model ve scaler dosyaları yeterlidir.

### Backend Kurulumu (Flask API)

**📌 SQL Server GEREKMEZ!** Sadece şu dosyaların olması yeterli:
- `trained_model_v2.pth` (eğitilmiş model)
- `scaler.pkl` (veri normalizasyon dosyası)

1. **Bağımlılıkları yükleyin:**
```bash
cd KiraTahminAI-main
pip install -r requirements.txt
```

2. **Gerekli dosyaları kontrol edin:**
```bash
# Bu dosyaların mevcut olduğundan emin olun:
ls trained_model_v2.pth
ls scaler.pkl
```

3. **API'yi başlatın:**
```bash
python app.py
```

API şu adreste çalışacak: `http://localhost:5000`

**Not**: Eğer `scaler.pkl` dosyası yoksa, modeli eğiten kişiden isteyin veya `KURULUM.md` dosyasına bakın.

### Frontend Kurulumu (Angular)

1. **Bağımlılıkları yükleyin:**
```bash
cd KiraTahminWeb_Angular-main
npm install
```

2. **Uygulamayı başlatın:**
```bash
npm start
```

Uygulama şu adreste çalışacak: `http://localhost:4200`

## 📡 API Dokümantasyonu

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Test Endpoint
API'nin çalışıp çalışmadığını kontrol eder.

**Request:**
```http
GET /api/test
```

**Response:**
```json
{
  "message": "API çalışıyor!"
}
```

#### 2. Predict Endpoint
Ev özelliklerine göre kira fiyatı tahmin eder.

**Request:**
```http
POST /api/predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "squareFeet": 120,      // Metrekare (m²)
  "numBedrooms": 3,       // Yatak odası sayısı
  "numBathrooms": 2,      // Banyo sayısı
  "location": 7,          // Konum skoru (1-10)
  "ageOfHouse": 5,        // Ev yaşı
  "hasGarage": 1,         // Garaj var mı? (0 veya 1)
  "hasGarden": 0,         // Bahçe var mı? (0 veya 1)
  "floor": 3,             // Kat numarası
  "buildingType": 3       // Bina tipi (1=Müstakil, 2=Villa, 3=Apartman, 4=Residans, 5=Site içi)
}
```

**Response (Başarılı):**
```json
{
  "success": true,
  "Predicted_Price": 25.50  // Bin TL cinsinden aylık kira
}
```

**Response (Hata):**
```json
{
  "success": false,
  "message": "Hata mesajı",
  "error": "Detaylı hata bilgisi"
}
```

## 🧠 Model Mimarisi

### Model Tipi
- **Multi-Layer Perceptron (MLP)**: Derin öğrenme sinir ağı
- **Giriş Boyutu**: 9 özellik
- **Çıkış Boyutu**: 24 sınıf (sınıflandırma)
- **Katmanlar**: 
  - Input Layer: 9 → 128
  - Hidden Layer 1: 128 → 64
  - Hidden Layer 2: 64 → 24
  - Activation: ReLU

### Eğitim Parametreleri
- **Epochs**: 50
- **Batch Size**: 16
- **Learning Rate**: 0.001
- **Optimizer**: Adam
- **Loss Function**: CrossEntropyLoss

### Veri İşleme
- **Normalizasyon**: StandardScaler (z-score normalization)
- **Kategorik Kodlama**: LabelEncoder (Location, BuildingType)
- **Veri Kaynağı**: SQL Server veritabanı

## 💰 Kira Fiyatı Hesaplama Algoritması

Model çıktısı (satış fiyatı) İstanbul piyasasına göre kira fiyatına dönüştürülür:

### Temel Formül
```
Temel Kira = Satış Fiyatı / 300
```

### Çarpanlar

1. **Bina Tipi Çarpanı:**
   - Müstakil: 1.0x
   - Villa: 1.8x (~100k TL/ay)
   - Apartman: 1.0x (~20k TL/ay)
   - Residans: 1.3x
   - Site İçi: 1.1x

2. **Konum Çarpanı:** 0.6x - 1.5x (1-10 arası)

3. **Metrekare Çarpanı:** 0.7x - 1.3x

4. **Oda Sayısı Çarpanı:** 0.8x - 1.2x

5. **Ekstra Özellikler:**
   - Garaj: +%15
   - Bahçe: +%20

6. **Ev Yaşı Çarpanı:** 1.2x - 0.8x (yeni evler daha pahalı)

7. **Kat Çarpanı:** 0.9x - 1.1x (yüksek katlar daha pahalı)

### Fiyat Sınırları
- **Minimum**: 8,000 TL/ay
- **Maksimum**: 200,000 TL/ay

## 📊 Örnek Tahminler

| Ev Tipi | Metrekare | Oda | Konum | Bina Tipi | Tahmini Kira |
|---------|-----------|-----|-------|-----------|--------------|
| Normal Apartman | 100 | 2+1 | 5 | Apartman | ~20k TL |
| Lüks Residans | 150 | 3+1 | 9 | Residans | ~50k TL |
| Villa | 250 | 4+1 | 10 | Villa | ~100k TL |

## 🔧 Model Eğitimi

Modeli yeniden eğitmek için:

```bash
python train.py
```

Bu komut:
1. Veritabanından verileri yükler
2. Verileri normalize eder
3. Modeli 50 epoch boyunca eğitir
4. `trained_model_v2.pth` dosyasına kaydeder
5. `scaler.pkl` dosyasını oluşturur

## 🛠️ Geliştirme

### Veritabanı Yapılandırması

`dataset.py` dosyasında SQL Server bağlantı bilgilerini güncelleyin:

```python
conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=AHMETPC\\SQLEXPRESS01;'
    'Database=EmreAI;'
    'Trusted_Connection=True;'
)
```

### Model Parametrelerini Değiştirme

`train.py` dosyasında eğitim parametrelerini ayarlayabilirsiniz:

```python
train_model(epochs=50, batch_size=16, learning_rate=0.001)
```

## 📝 Teknik Detaylar

### Backend Teknolojileri
- **Flask**: Web framework
- **PyTorch**: Deep learning framework
- **scikit-learn**: Machine learning utilities
- **pandas**: Veri işleme
- **numpy**: Sayısal hesaplamalar

### Frontend Teknolojileri
- **Angular 16**: Frontend framework
- **TypeScript**: Programlama dili
- **RxJS**: Reactive programming
- **Angular Forms**: Form yönetimi

## 🐛 Sorun Giderme

### Model yüklenemiyor
- `trained_model_v2.pth` dosyasının mevcut olduğunu kontrol edin
- Model dosyasının doğru konumda olduğundan emin olun

### Scaler hatası
- `scaler.pkl` dosyasının mevcut olduğunu kontrol edin
- Dosya yoksa, modeli eğiten kişiden isteyin
- **SQL Server GEREKMEZ** - sadece dosya yeterli

### API bağlantı hatası
- Flask API'nin çalıştığından emin olun (`http://localhost:5000`)
- CORS ayarlarını kontrol edin
- Test için: `python test_api.py`

### SQL Server hatası (API kullanımında)
- **API çalışırken SQL Server GEREKMEZ!**
- Sadece model ve scaler dosyaları yeterli
- SQL Server sadece model eğitimi için gerekir

## 🧪 Test

API'yi test etmek için:

```bash
python test_api.py
```

Bu script:
- API bağlantısını test eder
- Örnek bir tahmin yapar
- Sonuçları gösterir

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👥 Yazar

Proje geliştiricisi tarafından oluşturulmuştur.

## 📞 İletişim

Sorularınız için proje deposuna issue açabilirsiniz.

---

**Not**: Bu dokümantasyon proje geliştirme sürecinde güncellenmektedir.
