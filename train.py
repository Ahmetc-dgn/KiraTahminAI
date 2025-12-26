import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from app.dataset import UserDataset
from app.model import MLPModel
from sklearn.metrics import accuracy_score

def train_model(epochs=50, batch_size=16, learning_rate=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dataset = UserDataset()
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

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


    torch.save(model.state_dict(), "app/trained_model_v2.pth")
    print("Model başarıyla kaydedildi: app/trained_model_v2.pth")

if __name__ == "__main__":
    train_model()
