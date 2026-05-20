import requests
import json

API_KEY = "sk-caa0149ea3c0465489173b882b8bd7ec"
URL = "https://api.deepseek.com/v1/chat/completions"

def analyze_nutrition(food_name, weight):
    try:
        prompt = f"""
你是专业的食物营养计算工具，必须严格按照要求返回数据，禁止任何多余文字。
请根据以下食物信息，计算准确的营养成分：
食物名称：{food_name}
重量：{weight}克

请仅返回标准JSON格式，字段如下：
{{
    "calorie": 热量(单位：千卡，保留1位小数),
    "protein": 蛋白质(单位：克，保留1位小数),
    "carbs": 碳水化合物(单位：克，保留1位小数),
    "fat": 脂肪(单位：克，保留1位小数)
}}

示例（苹果100克）：
{{
    "calorie": 52.0,
    "protein": 0.3,
    "carbs": 14.0,
    "fat": 0.2
}}
"""
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0
        }
        resp = requests.post(URL, headers=headers, json=data, timeout=10)
        resp_json = resp.json()
        content = resp_json["choices"][0]["message"]["content"]
        nutrition = json.loads(content)
        return nutrition
    except Exception as e:
        print(f"DeepSeek调用出错: {str(e)}")
        # 本地兜底数据
        if "苹果" in food_name:
            return {"calorie": round(52.0 * weight / 100, 1),
                    "protein": round(0.3 * weight / 100, 1),
                    "carbs": round(14.0 * weight / 100, 1),
                    "fat": round(0.2 * weight / 100, 1)}
        elif "米饭" in food_name:
            return {"calorie": round(116.0 * weight / 100, 1),
                    "protein": round(2.6 * weight / 100, 1),
                    "carbs": round(25.6 * weight / 100, 1),
                    "fat": round(0.3 * weight / 100, 1)}
        elif "鸡蛋" in food_name:
            return {"calorie": round(143.0 * weight / 100, 1),
                    "protein": round(12.6 * weight / 100, 1),
                    "carbs": round(1.1 * weight / 100, 1),
                    "fat": round(9.5 * weight / 100, 1)}
        else:
            return {"calorie": round(1.0 * weight, 1),
                    "protein": round(0.05 * weight, 1),
                    "carbs": round(0.2 * weight, 1),
                    "fat": round(0.03 * weight, 1)}