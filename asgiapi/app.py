#a app class with asgi contract
import json
from asgiapi.router import Router
from functools import wraps 

class App:

    def __init__(self):
        self.router = Router()

    async def __call__(self,scope,receive,send):
        for i,(k,v) in enumerate(scope.items()):
            print(f"{i} item: {k} - {v}")

        if scope['type'] != 'http':
            return 
        
        response_body = json.dumps({"message": "Begin custom framework"}).encode()

        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'application/json'],
            ],
        })


        await send({
            'type':'http.response.body',
            'body': response_body,
        })
    
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
