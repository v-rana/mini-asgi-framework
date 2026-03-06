import uvicorn
from asgiapi.app import App

uvicorn_app = App()



if __name__ == "__main__":
    uvicorn.run(uvicorn_app,host="127.0.0.1",port=8000)
    