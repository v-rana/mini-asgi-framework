import json
from urllib.parse import parse_qs


class Request:
    
    def __init__(self,scope,receive):
        self.scope = scope
        self._receive = receive
    
    @property
    def method(self):
        return self.scope['method']

    @property
    def path(self):
        return self.scope['path']
    
    @property
    def headers(self):
        return {
            k.decode():v.decode()
            for k,v in self.scope.get('headers',[])
        }
    
    @property
    def query_params(self):
        raw = self.scope.get("query_string",b"").decode()
        return parse_qs(raw)
    

    async def body(self):
        body=b""
        while True:
            message = await self._receive()

            if message["type"] == "http.request":
                #if no body coming that silently insert empty b string
                body += message.get("body", b"")

                if not message.get("more_body", False):
                    break
        return body
    

    async def json(self):
        body = await self.body()

        return json.loads(body)

    async def _drain(self):
        while True:
            message = await self._receive()

            if message["type"] == "http.request":
                if not message.get("more_body", False):
                    break


