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
async def test_dict_response(client, app):

    @app.get("/json")
    async def route():
        return {"msg": "ok"}

    response = await client.get("/json")

    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}
    assert response.headers["content-type"] == "application/json"


@pytest.mark.asyncio
async def test_list_response(client, app):

    @app.get("/list")
    async def route():
        return [1, 2, 3]

    response = await client.get("/list")

    assert response.json() == [1, 2, 3]


@pytest.mark.asyncio
async def test_string_response(client, app):

    @app.get("/text")
    async def route():
        return "hello"

    response = await client.get("/text")

    assert response.status_code == 200
    assert response.text == "hello"
    assert response.headers["content-type"] == "text/plain"

from asgiapi.response import Response

@pytest.mark.asyncio
async def test_response_passthrough(client, app):

    @app.get("/raw")
    async def route():
        return Response(b"raw", status_code=201)

    response = await client.get("/raw")

    assert response.status_code == 201
    assert response.content == b"raw"

@pytest.mark.asyncio
async def test_none_response(client, app):

    @app.get("/none")
    async def route():
        return None

    response = await client.get("/none")

    assert response.status_code == 500


@pytest.mark.asyncio
async def test_query_and_string_response(client, app):

    @app.get("/hello")
    async def hello(name="world"):
        return f"hello {name}"

    response = await client.get("/hello?name=harsh")

    assert response.text == "hello harsh"