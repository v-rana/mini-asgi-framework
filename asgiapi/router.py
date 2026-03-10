from asgiapi.utils.router_utils import compile_path

class Route:
    def __init__(self,path_template,regex,params_names,method,handler):
        self.path_template = path_template
        self.regex = regex
        self.params_names = params_names
        self.method = method
        self.handler = handler
    
    def __repr__(self):
        return f"<Route path_template={self.path_template} method={self.method} handler={self.handler.__name__}>"

class Router:
    def __init__(self):
        #list of routes instances
        self.routes = []
    
    def add_route(self,path_template,method,handler):
        regex, params_names = compile_path(path_template)
        route = Route(
            path_template=path_template,
            regex=regex,
            params_names=params_names,
            method=method,handler=handler)
        self.routes.append(route)
    
    def __str__(self):
        for route in self.routes:
            print(f"Route: {route.path_template} - {route.method} - {route.handler.__name__}")
        
        return f"Router with {len(self.routes)} routes"