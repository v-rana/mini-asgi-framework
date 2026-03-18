from asgiapi.router import Router


router = Router()

def test_static_route_priority():

    router = Router()

    async def dynamic(id: int):
        return "dynamic"

    async def static():
        return "static"

    router.add_route("/users/{id}", "GET", dynamic)
    router.add_route("/users/me", "GET", static)

    handler, _ = router.match("/users/me", "GET")

    assert handler == static
    
def get_user(*, id:int):
    return {"id": id, "name": "John Doe"}

def post_user(*,id:int,post:str):
    return "done"

router.add_route("/users/{id}", "GET", get_user)
router.add_route("/users/{id}/post/{post}","POST",post_user)
print(router)    
print(router.routes[0])

# print(router.routes[1].regex)
# print(router.routes[1].params_names)
# match_obj_0 = router.routes[1].regex.match("/users/123")
# print(type(match_obj_0))
# print(match_obj_0.groupdict())

# print(router.routes[1])

# print(router.routes[1].regex)
# print(router.routes[1].params_names)
# match_obj_1 = router.routes[1].regex.match("/users/123/post/hello")
# print(match_obj_1.groupdict())

