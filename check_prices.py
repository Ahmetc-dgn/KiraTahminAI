"""Fiyat aralığını kontrol et"""
from dataset import home_price
import numpy as np

df = home_price()
prices = df['Price'].values

print(f"Fiyat istatistikleri:")
print(f"  Min: {np.min(prices)}")
print(f"  Max: {np.max(prices)}")
print(f"  Mean: {np.mean(prices):.2f}")
print(f"  Median: {np.median(prices):.2f}")
print(f"  Std: {np.std(prices):.2f}")
print(f"\nFiyat dağılımı:")
print(f"  Unique değerler: {len(np.unique(prices))}")
print(f"  İlk 10 fiyat: {sorted(np.unique(prices))[:10]}")
print(f"  Son 10 fiyat: {sorted(np.unique(prices))[-10:]}")

# Fiyatları 24 sınıfa böl
if len(np.unique(prices)) > 24:
    # Fiyatları 24 eşit aralığa böl
    price_bins = np.linspace(np.min(prices), np.max(prices), 25)  # 24 sınıf için 25 sınır
    print(f"\n24 sınıfa bölünmüş fiyat aralıkları:")
    for i in range(24):
        print(f"  Sınıf {i}: {price_bins[i]:.2f} - {price_bins[i+1]:.2f}")
else:
    print(f"\nFiyatlar zaten {len(np.unique(prices))} sınıfta")


