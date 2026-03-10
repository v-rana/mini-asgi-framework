from asgiapi.utils import compile_path


path = "/users/{id}"
regex, params_names = compile_path(path)

print(f"Compiled regex: {regex}")
print(f"Parameter names: {params_names}")