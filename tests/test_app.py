import pytest
from asgiapi.app import App


def test_handler_parameter_mismatch():

    app = App()


    with pytest.raises(Exception):
        @app.get("/users/{id}")
        async def handler():
            return "bad"        
        handler_func, params = app.router.match("/users/42", "GET")
        app._validate_handler_params(handler_func, params)


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
    }

    response = await app._handle_requests(scope)

    assert response.status_code == 307