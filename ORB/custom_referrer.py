from django.utils.deprecation import MiddlewareMixin


class CustomReferrerPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the request is for Google SSO URL containing /complete/
        if request.path.startswith('/complete/'):
            response['X-Referrer-Policy'] = 'no-referrer'

        return response