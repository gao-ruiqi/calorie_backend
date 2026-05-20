from flask import Blueprint, request, jsonify
from utils.response import success, fail
# 调用后端2的函数
from backend2.database import save_diet_record
from backend2.nutrition import analyze_nutrition

analyze_bp = Blueprint('analyze', __name__, url_prefix='/api')

@analyze_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    # 从请求中获取参数
    record_id = data.get('record_id')
    food_name = data.get('food_name')
    weight = data.get('weight')
    device_id = data.get('device_id', 'test_device')  # 默认设备号

    # 参数校验
    if not all([food_name, weight]):
        return jsonify(fail("参数不完整：food_name、weight不能为空"))

    try:
        # 1. 调用后端2：DeepSeek计算营养
        nutrition = analyze_nutrition(food_name, weight)
        
        # 2. 调用后端2：保存到数据库
        save_diet_record(
            device_id=device_id,
            weight=weight,
            food_name=food_name,
            calorie=nutrition["calorie"],
            protein=nutrition["protein"],
            carbs=nutrition["carbs"],
            fat=nutrition["fat"]
        )

        # 返回计算结果给APP
        return jsonify(success(
            data={
                "food_name": food_name,
                "weight": weight,
                **nutrition  # 把营养数据展开返回
            },
            msg="营养分析完成，已保存到数据库"
        ))
    except Exception as e:
        return jsonify(fail(f"分析失败：{str(e)}", code=500))