import re


PARAM_REGEX = re.compile(r"{([^}]+)}")

def compile_path(path_template):
    
    param_names = PARAM_REGEX.findall(path_template)

    regex_pattern = PARAM_REGEX.sub(
        r"(?P<\1>[^/]+)", 
        path_template)
    
    regex_pattern = "^" + regex_pattern + "$"
    
    compiled = re.compile(regex_pattern)
    
    return compiled , param_names


def toggle_trailing_slash(path):

    if path=="/":
        return path
    
    if path.endswith("/"):
        return path[:-1]
    
    return path + "/"