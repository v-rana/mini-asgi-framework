#a app class with asgi contract
import json
import inspect
from functools import wraps 

from asgiapi.utils.routing_utils import toggle_trailing_slash
from asgiapi.routing.exception import RouteNotFound
from asgiapi.router import Router
from asgiapi.response import JSONResponse, RedirectResponse


class App:

    def __init__(self):
        self.router = Router()

    async def __call__(self,scope,receive,send):
        for i,(k,v) in enumerate(scope.items()):
            print(f"{i} item: {k} - {v}")

        if scope['type'] != 'http':
            return 
              
        try:
            response = await self._handle_requests(scope)
        except Exception as e:
            response = JSONResponse(
                {"error":str(e)}, status_code=500)
        
        await response.send(send)
        
    def _resolve_route(self,path,method):
        try:

            handler,params = self.router.match(path,method)
            return handler,params 
        except RouteNotFound:
            alt_path = toggle_trailing_slash(path)
            try:
                self.router.match(alt_path,method)
                
            except RouteNotFound:
                raise 

            return RedirectResponse(alt_path) 
    
    async def _handle_requests(self,scope):
        path = scope["path"]
        method = scope["method"]
        
        match = self._resolve_route(path,method)

        if isinstance(match,RedirectResponse):
            return match
        handler, params = match

        # self._validate_handler_params(handler,params)

        result = await handler(**params)

        return JSONResponse(result)
    
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
