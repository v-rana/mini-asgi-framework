import json


class Response:
    def __init__(self,body,status_code=200,headers=None):
        
        self.body = body
        self.status_code = status_code
        self.headers = headers or []
    
    async def send(self,send):
        await send({
            'type':"http.response.start",
            'status':self.status_code,
            'headers':self.headers,
            }
        )

        await send(
            {'type':"http.response.body",
            'body':self.body,
            'more_body':False
            }
        )

class PlainTextResponse(Response):
    def __init__(self,text,status_code=200):
        body = text.encode()
        headers = [(b'content-type',b'text/plain')]
        super().__init__(body,status_code,headers)
        
class JSONResponse(Response):
    def __init__(self,data,status_code=200):
        body = json.dumps(data).encode()
        headers = [(b'content-type',b'application/json')]

        super().__init__(body,status_code,headers)

class RedirectResponse(Response):

    def __init__(self,location,status_code=307):
        headers = [(b'location',location.encode())]

        super().__init__(b'',status_code,headers)

