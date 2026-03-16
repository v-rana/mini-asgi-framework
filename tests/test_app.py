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