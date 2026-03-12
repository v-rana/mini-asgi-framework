#a app class with asgi contract
import json
from asgiapi.router import Router
from asgiapi.response import JSONResponse
from functools import wraps 

class App:

    def __init__(self):
        self.router = Router()

    async def __call__(self,scope,receive,send):
        for i,(k,v) in enumerate(scope.items()):
            print(f"{i} item: {k} - {v}")

        if scope['type'] != 'http':
            return 
        

        path = scope["path"]
        method = scope["method"]
        
        try:
            handler, params = self.router.match(path,method)

            result = await handler(**params)

            response = JSONResponse(result)
        except Exception as e:
            response = JSONResponse(
                {"error":str(e)}, status_code=500)
        
        await response.send(send)
    
    def get(self, path: str):

        def decorator(func):

            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

            self.router.add_route(
                path_template=path,
                method="GET",
                handler=wrapper
            )

            return wrapper

        return decorator
