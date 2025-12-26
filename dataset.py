import pyodbc
import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder, StandardScaler


def home_price():
    conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=AHMETPC\\SQLEXPRESS01;'
        'Database=EmreAI;'
        'Trusted_Connection=True;'
    )
    query = "SELECT * FROM HouseData"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


class UserDataset(Dataset):
    def __init__(self):
        df = home_price()


        categorical_cols = ['Location', 'BuildingType']
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

 
        self.X = df[['SquareFeet', 'NumBedrooms', 'NumBathrooms', 'Location',
                     'AgeOfHouse', 'HasGarage', 'HasGarden', 'Floor', 'BuildingType']].values
        self.y = df['Price'].values.reshape(-1, 1)

      
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)

        self.X = torch.tensor(self.X, dtype=torch.float32)
        self.y = torch.tensor(self.y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
