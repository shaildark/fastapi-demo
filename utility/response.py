from fastapi.responses import JSONResponse
def api_response(data = {}, payload = {},extra = {},errors = {}, message = "", status_code = 200):
    content = {
        "code" : status_code,
        "message": message,
        "data": data,
        "payload": payload,
        "extra": extra,
        "errors": errors
        }
    return JSONResponse(content=content, status_code=status_code)


def jwt_error_response(message = "", status_code = 401, errors = []):
    return {
        "code" : status_code,
        "message": message,
        "errors": errors
    }
    