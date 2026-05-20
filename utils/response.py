def success(data=None, msg="操作成功"):
    return {
        "code": 200,
        "msg": msg,
        "data": data
    }

def fail(msg="操作失败", code=400):
    return {
        "code": code,
        "msg": msg,
        "data": None
    }