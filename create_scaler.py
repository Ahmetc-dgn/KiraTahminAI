"""Scaler oluştur ve kaydet"""
from dataset import home_price
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle

# Veriyi yükle
df = home_price()

# Kategorik sütunları encode et
categorical_cols = ['Location', 'BuildingType']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))

# Feature'ları seç
X = df[['SquareFeet', 'NumBedrooms', 'NumBathrooms', 'Location',
        'AgeOfHouse', 'HasGarage', 'HasGarden', 'Floor', 'BuildingType']].values

# Scaler oluştur ve fit et
scaler = StandardScaler()
scaler.fit(X)

# Scaler'ı kaydet
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("Scaler basariyla olusturuldu ve kaydedildi: scaler.pkl")
print(f"   Mean: {scaler.mean_}")
print(f"   Scale: {scaler.scale_}")

