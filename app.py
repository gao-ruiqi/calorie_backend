from flask import Flask
from flask_cors import CORS
# 修复导入路径，确保能正确找到蓝图
from routes.upload import upload_bp
from routes.analyze import analyze_bp
from routes.diet import diet_bp
from routes.user import user_bp
from utils.error_handler import register_error_handlers

app = Flask(__name__)
CORS(app)

# 注册所有接口蓝图
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)
app.register_blueprint(diet_bp)
app.register_blueprint(user_bp)

# 注册全局异常处理
register_error_handlers(app)

if __name__ == '__main__':
    # 增加启动日志，确保能看到运行状态
    print("后端服务启动中...")
    print("服务地址：http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)