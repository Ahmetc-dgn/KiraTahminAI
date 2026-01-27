"""
API Test Scripti - SQL Server olmadan test etmek için
"""
import requests
import json

API_URL = "http://localhost:5000"

def test_api_connection():
    """API bağlantısını test et"""
    try:
        response = requests.get(f"{API_URL}/api/test")
        if response.status_code == 200:
            print("✅ API bağlantısı başarılı!")
            print(f"   Yanıt: {response.json()}")
            return True
        else:
            print(f"❌ API yanıt hatası: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API'ye bağlanılamıyor. Flask API'nin çalıştığından emin olun.")
        print("   Çalıştırmak için: python app.py")
        return False
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        return False

def test_prediction():
    """Kira tahmini test et"""
    test_data = {
        "squareFeet": 120,
        "numBedrooms": 3,
        "numBathrooms": 2,
        "location": 7,
        "ageOfHouse": 5,
        "hasGarage": 1,
        "hasGarden": 0,
        "floor": 3,
        "buildingType": 3  # Apartman
    }
    
    try:
        print("\n📊 Test tahmini gönderiliyor...")
        print(f"   Test verisi: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            f"{API_URL}/api/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                price = result.get("Predicted_Price", 0)
                print(f"\n✅ Tahmin başarılı!")
                print(f"   Tahmini Kira: {price:.2f} Bin TL/ay")
                print(f"   ({price * 1000:,.0f} TL/ay)")
                return True
            else:
                print(f"❌ Tahmin başarısız: {result.get('message', 'Bilinmeyen hata')}")
                return False
        else:
            print(f"❌ HTTP Hatası: {response.status_code}")
            print(f"   Yanıt: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("🧪 KiraTahminAI API Test Scripti")
    print("=" * 50)
    
    # API bağlantı testi
    if not test_api_connection():
        return
    
    # Tahmin testi
    if test_prediction():
        print("\n" + "=" * 50)
        print("✅ Tüm testler başarılı! API çalışıyor.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Tahmin testi başarısız.")
        print("=" * 50)

if __name__ == "__main__":
    main()

