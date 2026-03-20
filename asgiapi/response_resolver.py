from asgiapi.response import Response, JSONResponse, PlainTextResponse

class ResponseResolver:

    def resolve(self, result):

        # 1. Already a Response : return as is
        if isinstance(result, Response):
            return result

        # 2. dict / list : JSON
        if isinstance(result, (dict, list)):
            return JSONResponse(result)

        # 3. str : text
        if isinstance(result, str):
            return PlainTextResponse(result)

        # 4. None : error
        if result is None:
            raise ValueError("Handler returned None")

        # 5. fallback 
        return PlainTextResponse(str(result))