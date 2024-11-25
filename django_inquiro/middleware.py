from htmlmin import minify


class HTMLMinifyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Define URLs to exclude from processing
        self.excluded_urls = [
            '/admin/',  # Django Admin
        ]

    def __call__(self, request):
        response = self.get_response(request)

        # Skip processing for certain URLs
        if any(request.path.startswith(url) for url in self.excluded_urls):
            return response

        # Only minify HTML content
        if 'text/html' in response['Content-Type']:
            response.content = minify(
                response.content.decode('utf-8'),
                remove_comments=True,
                remove_empty_space=True,
                remove_all_empty_space=True,
                reduce_boolean_attributes=True
            ).encode('utf-8')

        return response
