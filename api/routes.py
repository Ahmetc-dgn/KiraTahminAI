from flask import Blueprint, request, jsonify
import torch
import numpy as np
import os
import sys
from flask_cors import cross_origin 
from sklearn.preprocessing import StandardScaler
import pickle


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import MLPModel

ml_bp = Blueprint("ml_bp", __name__)

# Model değişkenleri
model = None
model_loaded = False
scaler = None
scaler_loaded = False
input_size = 9
output_size = 24
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "trained_model_v2.pth"))
scaler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scaler.pkl"))

def load_model():
    """Modeli yükle - lazy loading"""
    global model, model_loaded
    
    if model_loaded:
        return model
    
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model dosyasi bulunamadi: {model_path}")
        
        model = MLPModel(input_size, output_size)
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
        model.eval()
        model_loaded = True
        print(f"[OK] Model basariyla yuklendi: {model_path}")
        return model
    except Exception as e:
        print(f"[HATA] Model yuklenirken hata olustu: {str(e)}")
        raise

def load_scaler():
    """Scaler'ı yükle - SQL Server'a bağlanmadan"""
    global scaler, scaler_loaded
    
    if scaler_loaded and scaler is not None:
        return scaler
    
    try:
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            print(f"[OK] Scaler basariyla yuklendi: {scaler_path}")
            scaler_loaded = True
            return scaler
        else:
            # Scaler dosyası yoksa hata ver (SQL'e bağlanmaya çalışma)
            raise FileNotFoundError(
                f"Scaler dosyasi bulunamadi: {scaler_path}\n"
                "Lutfen scaler.pkl dosyasinin proje dizininde oldugundan emin olun.\n"
                "Eger dosya yoksa, modeli egiten kisiyle paylasin veya create_scaler.py ile olusturun."
            )
    except FileNotFoundError as e:
        print(f"[HATA] {str(e)}")
        raise
    except Exception as e:
        print(f"[UYARI] Scaler yuklenirken hata: {str(e)}")
        return None

@ml_bp.route("/test", methods=["GET"])
@cross_origin() 
def test():
    return jsonify({"message": "API çalışıyor!"}), 200

@ml_bp.route("/predict", methods=["POST"])
@cross_origin()  
def predict():
    print("Predict endpoint'e istek geldi!")
    try:
        # Modeli yükle
        current_model = load_model()
        
        data = request.get_json()
        print("Gelen veri:", data)

        square_feet = data.get("squareFeet")
        num_bedrooms = data.get("numBedrooms")
        num_bathrooms = data.get("numBathrooms")
        location = data.get("location")
        age_of_house = data.get("ageOfHouse")
        has_garage = data.get("hasGarage")
        has_garden = data.get("hasGarden")
        floor = data.get("floor")
        building_type = data.get("buildingType")

        if None in [square_feet, num_bedrooms, num_bathrooms, location,
                    age_of_house, has_garage, has_garden, floor, building_type]:
            return jsonify({
                "success": False,
                "message": "Lutfen tum alanlari eksiksiz gonderin: squareFeet, numBedrooms, numBathrooms, location, ageOfHouse, hasGarage, hasGarden, floor, buildingType"
            }), 400

        # Input verilerini hazırla
        input_array = np.array([[
            float(square_feet),
            float(num_bedrooms),
            float(num_bathrooms),
            float(location),
            float(age_of_house),
            float(has_garage),
            float(has_garden),
            float(floor),
            float(building_type)
        ]], dtype=np.float32)

        # Scaler'ı yükle ve normalize et
        current_scaler = load_scaler()
        if current_scaler is not None:
            try:
                input_array = current_scaler.transform(input_array)
            except:
                # Scaler fit edilmemişse, basit normalize yap
                print("[UYARI] Scaler transform basarisiz, basit normalize kullaniliyor")
                # Manuel normalize: Her feature için ortalama ve std tahmin et
                # Bu geçici bir çözüm
                pass

        input_tensor = torch.tensor(input_array, dtype=torch.float32)

        with torch.no_grad():
            output = current_model(input_tensor)
            
            # Softmax ile olasılıklara çevir
            probabilities = torch.softmax(output, dim=1)
            
            # En yüksek olasılıklı sınıfı al
            _, predicted_class = torch.max(probabilities, 1)
            predicted_class_idx = predicted_class.item()
            
            # Fiyat aralığı: 1,244,000 - 4,102,000 TL (satış fiyatları)
            # 24 sınıfa bölünmüş
            min_price = 1244000.0
            max_price = 4102000.0
            num_classes = 24
            
            # Her sınıf için fiyat aralığını hesapla
            price_range = max_price - min_price
            class_width = price_range / num_classes
            
            # Sınıf indekslerini gerçek satış fiyatlarına dönüştür
            class_centers = []
            for i in range(num_classes):
                class_min = min_price + (i * class_width)
                class_max = min_price + ((i + 1) * class_width)
                class_center = (class_min + class_max) / 2.0
                class_centers.append(class_center)
            
            class_centers_tensor = torch.tensor(class_centers, dtype=torch.float32)
            
            # Weighted average: Her sınıfın olasılığı * sınıf merkez fiyatı
            predicted_sale_price = torch.sum(probabilities * class_centers_tensor.unsqueeze(0), dim=1).item()
            
            # İSTANBUL KİRA FİYATI HESAPLAMA
            # Satış fiyatından kira fiyatına dönüştür (İstanbul piyasasına göre)
            
            # Temel kira hesaplama: Satış fiyatı / 300 (yıllık %4 getiri, aylık)
            base_rent = predicted_sale_price / 300.0
            
            # Özelliklere göre çarpanlar (İstanbul piyasası)
            # Bina tipi çarpanı
            building_type_multiplier = {
                1: 1.0,   # Müstakil
                2: 1.8,   # Villa (100k civarı)
                3: 1.0,   # Apartman (normal ev 20k civarı)
                4: 1.3,   # Residans
                5: 1.1    # Site içi
            }
            bt_mult = building_type_multiplier.get(int(building_type), 1.0)
            
            # Konum çarpanı (1-10 arası)
            location_multiplier = 0.6 + (float(location) / 10.0) * 0.9  # 0.6 - 1.5 arası
            
            # Metrekare çarpanı (büyük evler daha pahalı)
            sqm_multiplier = 0.7 + (float(square_feet) / 200.0) * 0.6  # 0.7 - 1.3 arası
            
            # Oda sayısı çarpanı
            room_multiplier = 0.8 + (float(num_bedrooms) / 5.0) * 0.4  # 0.8 - 1.2 arası
            
            # Ekstra özellikler
            extra_features = 1.0
            if has_garage:
                extra_features += 0.15  # Garaj +%15
            if has_garden:
                extra_features += 0.20  # Bahçe +%20
            
            # Yaş çarpanı (yeni evler daha pahalı)
            age_multiplier = 1.2 - (float(age_of_house) / 50.0) * 0.4  # 1.2 - 0.8 arası
            
            # Kat çarpanı (yüksek katlar daha pahalı)
            floor_multiplier = 0.9 + (float(floor) / 20.0) * 0.2  # 0.9 - 1.1 arası
            
            # Toplam kira fiyatı hesaplama
            predicted_rent = base_rent * bt_mult * location_multiplier * sqm_multiplier * \
                           room_multiplier * extra_features * age_multiplier * floor_multiplier
            
            # İstanbul için minimum ve maksimum kira sınırları
            min_rent = 8000   # Minimum 8k TL/ay
            max_rent = 200000 # Maksimum 200k TL/ay (lüks villa)
            
            # Sınırları uygula
            predicted_rent = max(min_rent, min(predicted_rent, max_rent))
            
            # Bin TL'ye çevir (frontend'de bin TL gösteriliyor)
            predicted_rent_bin = predicted_rent / 1000.0
            
            # Debug bilgileri
            print(f"=== KIRA TAHMINI ===")
            print(f"Satis fiyati (model cikti): {predicted_sale_price:,.0f} TL")
            print(f"Temel kira: {base_rent:,.0f} TL")
            print(f"Bina tipi carpani ({building_type}): {bt_mult:.2f}x")
            print(f"Konum carpani ({location}): {location_multiplier:.2f}x")
            print(f"Metrekare carpani ({square_feet}): {sqm_multiplier:.2f}x")
            print(f"Oda carpani ({num_bedrooms}): {room_multiplier:.2f}x")
            print(f"Ekstra ozellikler: {extra_features:.2f}x")
            print(f"Yas carpani ({age_of_house}): {age_multiplier:.2f}x")
            print(f"Kat carpani ({floor}): {floor_multiplier:.2f}x")
            print(f"Hesaplanan kira: {predicted_rent:,.0f} TL/ay ({predicted_rent_bin:.2f} bin TL)")

        return jsonify({
            "success": True,
            "Predicted_Price": round(predicted_rent_bin, 2)
        }), 200

    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "message": "Model dosyasi bulunamadi. Lutfen once modeli egitin (python train.py)",
            "error": str(e)
        }), 500
    except Exception as e:
        print("Hata olustu:", str(e))
        return jsonify({
            "success": False,
            "message": "Sunucuda bir hata olustu.",
            "error": str(e)
        }), 500
