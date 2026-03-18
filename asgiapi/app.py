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

        if scope['type']=="http":
            response = await self._handle_http(scope,receive)
            await response.send(send)
        elif scope['type']=="lifespan":
            await self._handle_lifespan(receive,send)
        else:
            raise NotImplementedError(f"Unsuppoorted scope type {scope['type']}")
        
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
    

    async def _handle_http(self,scope,receive):
        path = scope["path"]
        method = scope["method"]
        
        match = self._resolve_route(path,method)

        if isinstance(match,RedirectResponse):
            return match
        handler, params = match

        # self._validate_handler_params(handler,params)

        result = await handler(**params)

        return JSONResponse(result)
    
    async def _handle_lifespan(self,receive,send):
        while True:
            message = await receive()

            if message['type'] == 'lifespan.startup':
                await send({'type':'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type':'lifespan.shutdown.complete'})
                return

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
