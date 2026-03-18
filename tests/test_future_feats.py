import pytest
from asgiapi.router import Router




#Edge Case 3 — Type Conversion
@pytest.mark.xfail(reason="Type conversion not implemented yet")
def test_int_conversion():

    router = Router()

    async def handler(*, id: int):
        return id

    router.add_route("/users/{id:int}", "GET", handler)

    _, params = router.match("/users/42", "GET")

    assert isinstance(params["id"], int)

# Edge Case 4 — Ambiguous Routes
@pytest.mark.xfail(reason="Route conflict detection not implemented")
def test_route_conflict_detection():

    router = Router()

    async def a(*, id:int):
        pass

    async def b(*, name:int):
        pass


    with pytest.raises(Exception):
        router.add_route("/users/{id}", "GET", a)
        router.add_route("/users/{name}", "GET", b)

# Edge Case 5 — Non-Async Handler
@pytest.mark.xfail(reason="Async handler enforcement not implemented")
def test_sync_handler_rejected():

    router = Router()

    def handler():
        return "sync"

    with pytest.raises(Exception):
        router.add_route("/users", "GET", handler)
