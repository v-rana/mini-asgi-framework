import pytest
from asgiapi.app import App


def test_handler_parameter_mismatch():

    app = App()

    @app.get("/users/{id}")
    async def handler():
        return "bad"

    with pytest.raises(Exception):
        handler_func, params = app.router.match("/users/42", "GET")
        app._validate_handler_params(handler_func, params)