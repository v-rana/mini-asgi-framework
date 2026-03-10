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