from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'pages'

    INDEX_URL = 'index'
    REFERENCES_URL = 'references'
