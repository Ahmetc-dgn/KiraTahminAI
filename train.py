import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from dataset import UserDataset
from model import MLPModel
from sklearn.metrics import accuracy_score
import pickle
import os

def train_model(epochs=50, batch_size=16, learning_rate=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dataset = UserDataset()
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Scaler'ı kaydet (eğer dataset'te scaler varsa)
    # Dataset'te scaler kullanılıyor ama kaydedilmiyor, bu yüzden manuel oluşturuyoruz
    from sklearn.preprocessing import StandardScaler
    import pandas as pd
    from dataset import home_price
    
    # Orijinal verileri al ve scaler oluştur
    df = home_price()
    from sklearn.preprocessing import LabelEncoder
    
    categorical_cols = ['Location', 'BuildingType']
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    
    X = df[['SquareFeet', 'NumBedrooms', 'NumBathrooms', 'Location',
            'AgeOfHouse', 'HasGarage', 'HasGarden', 'Floor', 'BuildingType']].values
    
    scaler = StandardScaler()
    scaler.fit(X)
    
    # Scaler'ı kaydet
    scaler_path = "scaler.pkl"
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler basariyla kaydedildi: {scaler_path}")

    input_size = dataset.X.shape[1]
    output_size = 24
    model = MLPModel(input_size, output_size).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        total_loss = 0.0
        for X_batch, y_batch in dataloader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device).long().squeeze()

            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}")


    all_preds = []
    all_labels = []

    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device).long().squeeze()

            outputs = model(X_batch)
            _, predicted = torch.max(outputs.data, 1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(y_batch.cpu().numpy())

    acc = accuracy_score(all_labels, all_preds)
    print(f"\nTraining Accuracy: {acc * 100:.2f}%")


    torch.save(model.state_dict(), "trained_model_v2.pth")
    print("Model başarıyla kaydedildi: trained_model_v2.pth")

if __name__ == "__main__":
    train_model()
