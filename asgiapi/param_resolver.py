import inspect


class ParameterResolver:
    def __init__(self):
        self.type_converters = {
            int: int,
            float: float,
            str: str,
            bool: self._to_bool
        }
    
    def _to_bool(self,value):
        return str(value).lower() in ("true","1","yes")

    def build_arguments(self,handler,request,path_params):
        bound_values = {}
        if not isinstance(path_params, dict):
            path_params = {}
        for name,param in inspect.signature(handler).parameters.items():
            value = self._resolve_param(
                name,
                param,
                request,
                path_params
            )
            bound_values[name] =value
        
        return bound_values
        
    
    def _resolve_param(self,name,param,request,path_params):

        #1. Inject Request 
        if param.annotation.__name__ == "Request":
            return request
        #2. path params
        if name in path_params:
            raw_value = path_params[name]
        #3. query params
        elif name in request.query_params:
            raw_value = request.query_params[name]
        elif param.default is not  inspect.Parameter.empty:
            return param.default
        else:
            raise TypeError(f"Missing required parameter: {name}")

        return self._convert_type(raw_value, param.annotation, name)        
    
    def _convert_type(self,value,annotation,name):

        if annotation is inspect.Parameter.empty:
            return value
        
        converter = self.type_converters.get(annotation)

        if converter is None:
            return value
        
        try:
            return converter(value)
        except Exception as e:
            raise TypeError(f"Invalid value for '{name}', expected {annotation.__name__}") from e
