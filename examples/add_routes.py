from asgiapi.app import App



app = App()



@app.get("/user/{id}")
def get_user(int:id):
    return f"user_{id}"

print(app.router)
print(app.router[0])
