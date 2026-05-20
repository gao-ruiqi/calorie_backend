from flask import jsonify
from utils.response import fail

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def server_error(e):
        return jsonify(fail(msg=f"服务器错误：{str(e)}", code=500)), 500