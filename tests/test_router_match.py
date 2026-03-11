from asgiapi.router import Router
import pytest


def test_route_match():

    router = Router()

    async def handler(*, id):
        pass

    router.add_route("/users/{id}", "GET", handler)

    h, params = router.match("/users/42", "GET")

    assert h == handler
    assert params == {"id": "42"}


def test_route_not_found():

    router = Router()

    with pytest.raises(Exception):
        router.match("/missing", "GET")


def test_method_not_allowed():

    router = Router()

    async def handler():
        pass

    router.add_route("/users", "GET", handler)

    with pytest.raises(Exception):
        router.match("/users", "POST")




