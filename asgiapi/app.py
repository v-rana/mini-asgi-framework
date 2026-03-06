#a app class with asgi contract
import json

class App:

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