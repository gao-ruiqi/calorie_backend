from flask import Blueprint, request, jsonify
from utils.response import success, fail
from concurrent.futures import ThreadPoolExecutor
import uuid
from tasks import process_upload_sync

upload_bp = Blueprint('upload', __name__, url_prefix='/api')

# 线程池（最多同时处理10个任务）
executor = ThreadPoolExecutor(max_workers=10)

# 全局存储任务状态（内存）
task_status = {}   # task_id -> "processing"/"success"/"failed"
task_results = {}  # task_id -> 结果字典或错误信息

def process_upload_task(task_id, device_id, weight, image_base64):
    """后台执行的任务"""
    try:
        result = process_upload_sync(device_id, weight, image_base64)
        task_status[task_id] = "success"
        task_results[task_id] = result
    except Exception as e:
        print(f"任务 {task_id} 失败: {e}")
        task_status[task_id] = "failed"
        task_results[task_id] = {"error": str(e)}

@upload_bp.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify(fail("请求体不是有效的JSON", code=400))

    device_id = data.get('device_id')
    weight = data.get('weight')
    image_base64 = data.get('image')

    if not all([device_id, weight, image_base64]):
        return jsonify(fail("参数不完整：device_id、weight、image不能为空", code=400))

    try:
        weight = float(weight)
    except (TypeError, ValueError):
        return jsonify(fail("weight必须是数字", code=400))

    # 生成唯一任务ID
    task_id = str(uuid.uuid4())
    task_status[task_id] = "processing"
    task_results[task_id] = None

    # 提交到线程池执行
    executor.submit(process_upload_task, task_id, device_id, weight, image_base64)

    return jsonify(success(
        data={
            "task_id": task_id,
            "status": "processing"
        },
        msg="上传已接收，正在后台识别"
    ))