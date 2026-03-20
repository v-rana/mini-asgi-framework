import pytest
from asgiapi.app import App
from asgiapi.request import Request

def test_handler_parameter_mismatch():
    app = App()

    @app.get("/users/{id}")
    async def handler(id:int, name:str):
        return "ok"

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/users/42",
        "query_string": b"",
        "headers": [],
    }

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    request = Request(scope, receive)
    handler_func, params = app.router.match("/users/42", "GET")

    with pytest.raises(TypeError):
        app.parameter_resolver.build_arguments(handler_func, request, params)


@pytest.mark.asyncio
async def test_app_redirects_trailing_slash():
    app = App()

    @app.get("/users")
    async def handler():
        return {"ok": True}

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/users/",
        "query_string": b"",
        "headers": [],
    }

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    response = await app._handle_http(scope, receive)

    assert response.status_code == 307