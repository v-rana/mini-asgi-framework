import pytest
from asgiapi.router import Router

# Edge Case 1 — Static Route Priority
@pytest.mark.xfail(reason="Router does not prioritize static routes yet")
def test_static_route_priority():

    router = Router()

    async def me():
        return "me"

    async def user(*, id):
        return id

    router.add_route("/users/{id}", "GET", user)
    router.add_route("/users/me", "GET", me)

    handler, params = router.match("/users/me", "GET")

    assert handler == me

# Edge Case 2 — Trailing Slash Handling
@pytest.mark.xfail(reason="Trailing slash normalization not implemented")
def test_trailing_slash_equivalence():

    router = Router()

    async def handler():
        return "ok"

    router.add_route("/users", "GET", handler)

    handler_result, _ = router.match("/users/", "GET")

    assert handler_result == handler

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

    async def a(*, id):
        pass

    async def b(*, name):
        pass

    router.add_route("/users/{id}", "GET", a)

    with pytest.raises(Exception):
        router.add_route("/users/{name}", "GET", b)

# Edge Case 5 — Non-Async Handler
@pytest.mark.xfail(reason="Async handler enforcement not implemented")
def test_sync_handler_rejected():

    router = Router()

    def handler():
        return "sync"

    with pytest.raises(Exception):
        router.add_route("/users", "GET", handler)
