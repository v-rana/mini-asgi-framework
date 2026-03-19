import inspect


class ParameterResolver:
    #can init class get the request and path params here?
    def build_arguments(self,handler,request,path_params):
        bound_values = {}
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
        if not isinstance(path_params, dict):
            path_params = {}
        #1. Inject Request , maybe make it more dynamic 
        if name=="request":
            return request
        #2. path params
        if name in path_params:
            return path_params[name]
        #3. query params
        if name in request.query_params:
            return request.query_params[name]
        if param.default is not  inspect.Parameter.empty:
            return param.default
        
        raise TypeError(f"Missing required parameter: {name}")
