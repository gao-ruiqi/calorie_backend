from flask import Blueprint, jsonify
from utils.response import success
from backend2.stats import get_daily_total

user_bp = Blueprint('user', __name__, url_prefix='/api')

@user_bp.route('/user/profile', methods=['GET'])
def user_profile():
    return jsonify(success(
        data={
            "username": "test_user",
            "goal": "减脂"
        },
        msg="获取用户信息成功"
    ))

@user_bp.route('/user/stats', methods=['GET'])
def user_stats():
    daily_total = get_daily_total()
    return jsonify(success(
        data=daily_total,
        msg="获取今日营养统计成功"
    ))

# 任务状态查询接口（依赖 routes.upload 中的 task_status 和 task_results）
@user_bp.route('/task/<task_id>', methods=['GET'])
def task_status(task_id):
    from routes.upload import task_status, task_results
    if task_id not in task_status:
        return jsonify(success(data={"status": "not_found"}))
    
    status = task_status[task_id]
    if status == "processing":
        return jsonify(success(data={"status": "processing"}))
    elif status == "failed":
        return jsonify(success(data={
            "status": "failed",
            "error": task_results[task_id].get("error", "未知错误")
        }))
    else:  # success
        return jsonify(success(data={
            "status": "success",
            "result": task_results[task_id]
        }))

# 运动建议接口（新增）
@user_bp.route('/advice', methods=['GET'])
def get_advice():
    from backend2.stats import get_daily_total
    total = get_daily_total()
    calorie = total["calorie"]
    # 假设每日目标为 2000 大卡
    remaining = 2000 - calorie
    if remaining <= 0:
        advice = "今日摄入已超标，建议增加运动，散步30分钟。"
    elif remaining < 200:
        advice = f"还可以摄入 {remaining} 大卡，保持当前饮食。"
    else:
        minutes = max(10, int(remaining / 10))
        advice = f"今日剩余 {remaining} 大卡，建议运动 {minutes} 分钟（快走或慢跑）。"
    return jsonify(success(data={
        "remaining_calories": remaining,
        "advice": advice
    }))