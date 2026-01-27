from flask import Flask
from flask_cors import CORS
from api.routes import ml_bp

app = Flask(__name__)
CORS(app)  


app.register_blueprint(ml_bp, url_prefix='/api')

@app.route('/')
def home():
    return {
        "message": "KiraTahminAI API",
        "endpoints": {
            "test": "GET /api/test",
            "predict": "POST /api/predict"
        }
    }

if __name__ == '__main__':
    print("API baslatiliyor...")
    print("Test endpoint: http://localhost:5000/api/test")
    print("Predict endpoint: http://localhost:5000/api/predict")
    app.run(debug=True, host='0.0.0.0', port=5000)

