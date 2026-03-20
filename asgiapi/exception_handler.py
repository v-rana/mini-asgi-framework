from asgiapi.response import JSONResponse
from asgiapi.routing.exception import RouteNotFound, MethodNotAllowed


def exception_handler(exc):
    
    if isinstance(exc, RouteNotFound):
        return JSONResponse({
            "error": "Route not found",
            "detail": str(exc)}, status_code=404)
    
    if isinstance(exc, MethodNotAllowed):
        return JSONResponse({
            "error": "Method not allowed",
            "detail": str(exc)}, status_code=405)
    
    if isinstance(exc, TypeError):
        return JSONResponse({
            "error": "Bad Request",
            "detail": str(exc)
        }, status_code=400)
    
    #default fallback for unhandled exceptions
    return JSONResponse({"error": "Internal server error","detail": str(exc)}, status_code=500)

