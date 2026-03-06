from asgiapi.router import Router


router = Router()


def get_user(*, id:int):
    return {"id": id, "name": "John Doe"}


router.add_route("/users/{id}", "GET", get_user)

print(router.routes)
print(router)    