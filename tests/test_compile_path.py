from asgiapi.utils.routing_utils import compile_path


def test_compile_path():

    regex, params = compile_path("/users/{id}")

    match = regex.match("/users/42")

    assert match is not None
    assert match.groupdict() == {"id": "42"}