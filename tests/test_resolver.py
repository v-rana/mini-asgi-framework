import pytest
from httpx import AsyncClient, ASGITransport
from asgiapi.app import App


@pytest.fixture
def app():
    return App()






@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client, app):

    @app.get("/")
    async def root():
        return {"msg": "ok"}

    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}


@pytest.mark.asyncio
async def test_path_param(client, app):

    @app.get("/users/{id}")
    async def get_user(id:int):
        return {"id": id}

    response = await client.get("/users/123")

    assert response.status_code == 200
    assert response.json() == {"id": "123"}


@pytest.mark.asyncio
async def test_query_param(client, app):

    @app.get("/search")
    async def search(q:str):
        return {"q": q}

    response = await client.get("/search?q=python")

    assert response.status_code == 200
    assert response.json() == {"q": "python"}


@pytest.mark.asyncio
async def test_path_and_query(client, app):

    @app.get("/items/{id}")
    async def get_item(id:int, filter:str):
        return {"id": id, "filter": filter}

    response = await client.get("/items/10?filter=active")

    assert response.json() == {"id": "10", "filter": "active"}



@pytest.mark.asyncio
async def test_default_param(client, app):

    @app.get("/hello")
    async def hello(name:str="world"):
        return {"msg": name}

    response = await client.get("/hello")
    assert response.json() == {"msg": "world"}

    response = await client.get("/hello?name=Harsh")
    assert response.json() == {"msg": "Harsh"}



@pytest.mark.asyncio
async def test_request_injection(client, app):

    @app.get("/debug")
    async def debug(request):
        return {
            "method": request.method,
            "path": request.path
        }

    response = await client.get("/debug")

    assert response.json() == {
        "method": "GET",
        "path": "/debug"
    }


@pytest.mark.asyncio
async def test_missing_param(client, app):

    @app.get("/fail")
    async def fail(x:int):
        return {"x": x}

    response = await client.get("/fail")

    assert response.status_code == 500


@pytest.mark.asyncio
async def test_path_priority(client, app):

    @app.get("/test/{id}")
    async def test(id:int):
        return {"id": id}

    response = await client.get("/test/1?id=999")

    assert response.json() == {"id": "1"}

@pytest.mark.asyncio
async def test_multiple_query_params(client, app):

    @app.get("/multi")
    async def multi(a, b):
        return {"a": a, "b": b}

    response = await client.get("/multi?a=1&b=2")

    assert response.json() == {"a": "1", "b": "2"}