from flask import Blueprint, request, jsonify
import torch
import numpy as np
import os
from flask_cors import cross_origin 
from app.model import MLPModel

ml_bp = Blueprint("ml_bp", __name__)

# 🔍 Model yükleme
input_size = 9
output_size = 24
model = MLPModel(input_size, output_size)
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "trained_model_v2.pth"))
model.load_state_dict(torch.load(model_path))
model.eval()

@ml_bp.route("/test", methods=["GET"])
@cross_origin() 
def test():
    return jsonify({"message": "API çalışıyor!"}), 200

@ml_bp.route("/predict", methods=["POST"])
@cross_origin()  
def predict():
    print("Predict endpoint'e istek geldi!")
    try:
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
                "message": "Lütfen tüm alanları eksiksiz gönderin: squareFeet, numBedrooms, numBathrooms, location, ageOfHouse, hasGarage, hasGarden, floor, buildingType"
            }), 400

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

        input_tensor = torch.tensor(input_array)

        with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output.data, 1)

        return jsonify({
            "success": True,
            "Predicted_Price": float(predicted.item())
        }), 200

    except Exception as e:
        print("Hata oluştu:", str(e))
        return jsonify({
            "success": False,
            "message": "Sunucuda bir hata oluştu.",
            "error": str(e)
        }), 500
