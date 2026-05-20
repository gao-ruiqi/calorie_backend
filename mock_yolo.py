# mock_yolo.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({"food_name": "苹果", "confidence": 0.99})

if __name__ == '__main__':
    print("Mock YOLO 服务启动在 http://127.0.0.1:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)