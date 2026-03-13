from asgiapi.utils.router_utils import compile_path

class MethodNotAllowed(Exception):
    pass

class RouteNotFound(Exception):
    pass

class Route:
    def __init__(self,path_template,regex,params_names,method,handler,score):
        self.path_template = path_template
        self.regex = regex
        self.params_names = params_names
        self.method = method
        self.handler = handler
        self.score = score
    
    def __repr__(self):
        return f"<Route path_template={self.path_template} method={self.method} handler={self.handler.__name__}>"

class Router:
    def __init__(self):
        #list of routes instances
        self.routes = []
    
    def add_route(self,path_template,method,handler):
        regex, params_names = compile_path(path_template)
        score = self.compute_score(path_template)
        route = Route(
            path_template=path_template,
            regex=regex,
            params_names=params_names,
            method=method,handler=handler,
            score=score)  
        self.routes.append(route)
        self.routes.sort(key=lambda r: r.score, reverse=True)  # Sort routes by score in descending order

    def match(self,path,method):
        path_matched = False

        for route in self.routes:
            match = route.regex.match(path)

            if not match:
                continue

            path_matched = True

            if method != route.method:
                continue
            
            params = match.groupdict(path)
            return route.handler, params

        if path_matched:
            raise MethodNotAllowed(f"Method {method} not allowed for path {path}")

        raise RouteNotFound(f"No Route found for path {path}") 

    def compute_score(self,path):
        segments = path.strip("/").split("/")
        score = 0

        for segment in segments:
            if segment.startswith("{") and segment.endswith("}"):
                score += 1
            else:
                score += 10
        
        return score


    def __getitem__(self, key):
        try:
            return self.routes[key]
        except IndexError:
            raise IndexError(f"Route index {key} out of range. Total routes: {len(self.routes)}")
    
    def __str__(self):
        for route in self.routes:
            print(f"Route: {route.path_template} - {route.method} - {route.handler.__name__}")
        
        return f"Router with {len(self.routes)} routes"