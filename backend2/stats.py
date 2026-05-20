from backend2.database import get_today_records
import datetime

# 今日总营养
def get_daily_total():
    records = get_today_records()
    total_cal = 0
    total_pro = 0
    total_car = 0
    total_fat = 0

    for r in records:
        total_cal += r[4]
        total_pro += r[5]
        total_car += r[6]
        total_fat += r[7]

    return {
        "calorie": round(total_cal, 1),
        "protein": round(total_pro, 1),
        "carbs": round(total_car, 1),
        "fat": round(total_fat, 1)
    }

# 本周统计（简化版）
def get_weekly_total():
    today = get_daily_total()
    return {
        "week_calorie": round(today["calorie"] * 7, 1),
        "week_protein": round(today["protein"] * 7, 1),
    }