from flask import Blueprint, jsonify
from utils.response import success
# 调用后端2的数据库函数
from backend2.database import get_all_records

diet_bp = Blueprint('diet', __name__, url_prefix='/api')

@diet_bp.route('/diet/list', methods=['GET'])
def diet_list():
    # 从数据库获取所有历史记录
    records = get_all_records()
    # 格式化数据，方便APP解析
    formatted_records = []
    for r in records:
        formatted_records.append({
            "id": r[0],
            "device_id": r[1],
            "weight": r[2],
            "food_name": r[3],
            "calorie": r[4],
            "protein": r[5],
            "carbs": r[6],
            "fat": r[7],
            "create_time": r[8]
        })
    return jsonify(success(data=formatted_records, msg="获取饮食列表成功"))