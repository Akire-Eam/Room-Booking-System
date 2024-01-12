from social_django.strategy import DjangoStrategy


orbsdev = 'https://orbsdev.upm.edu.ph'
orbslive = 'https://orbs.upm.edu.ph'
localhost_default = 'http://127.0.0.1:8000'
localhost_50000 = 'http://127.0.0.1:50000'

class GoogleSSOStrategy(DjangoStrategy):
    def build_absolute_uri(self, path=None):
        uri = orbsdev + (path or '/complete/google-oauth2/')
        return uri
