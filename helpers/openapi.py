# helpers/openapi.py
def preprocessing_filter_spec(endpoints):
    allowed_endpoints = ["/v1/assets/", "/v1/netflow/"]

    filtered = []
    for path, path_regex, method, callback in endpoints:
        if any(endpoint in path for endpoint in allowed_endpoints):
            filtered.append((path, path_regex, method, callback))
    return filtered
