from asgiapi.router import Router


router = Router()


def get_user(*, id:int):
    return {"id": id, "name": "John Doe"}

def post_user(*,id:int,post:str):
    return "done"

router.add_route("/users/{id}", "GET", get_user)
router.add_route("/users/{id}/post/{post}","POST",post_user)
print(router)    
print(router.routes[0])

print(router.routes[0].regex)
print(router.routes[0].params_names)

print(router.routes[1])

print(router.routes[1].regex)
print(router.routes[1].params_names)
