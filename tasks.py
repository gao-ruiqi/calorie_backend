from backend2.nutrition import analyze_nutrition
from backend2.database import save_diet_record
import requests

# YOLO 服务地址（联调时改为同学B的IP）
YOLO_URL = "http://10.29.148.16:5000"

def call_yolo(image_base64):
    """调用 YOLO 服务"""
    try:
        resp = requests.post(YOLO_URL, json={"image_base64": image_base64}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("food_name", "未知食物")
    except Exception as e:
        print(f"YOLO调用失败: {e}")
    return "未知食物"

def process_upload_sync(device_id, weight, image_base64):
    """同步执行的上传处理逻辑（被线程池调用）"""
    # 1. 识别食物
    food_name = call_yolo(image_base64)
    
    # 2. 获取营养
    nutrition = analyze_nutrition(food_name, weight)
    
    # 3. 保存数据库
    save_diet_record(
        device_id=device_id,
        weight=weight,
        food_name=food_name,
        calorie=nutrition["calorie"],
        protein=nutrition["protein"],
        carbs=nutrition["carbs"],
        fat=nutrition["fat"]
    )
    
    return {
        "food_name": food_name,
        "weight": weight,
        "calorie": nutrition["calorie"],
        "protein": nutrition["protein"],
        "carbs": nutrition["carbs"],
        "fat": nutrition["fat"]
    }