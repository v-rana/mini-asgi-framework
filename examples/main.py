import uvicorn
from asgiapi.app import App

app = App()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{id}")
async def get_user(*, id: int):
    return {"user_id": id}

# @app.get("/user/{id}")
# def get_user(id:int):
#     return f"user_{id}"

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
    