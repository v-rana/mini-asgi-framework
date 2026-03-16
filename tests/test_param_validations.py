import pytest
from asgiapi.app import App
    
def test_missing_annotation():
    app = App()

    with pytest.raises(ValueError):
        
        @app.get("/users/{id}")
        async def handler(id):
            return {"id": id}