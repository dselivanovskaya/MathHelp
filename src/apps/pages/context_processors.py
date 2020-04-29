from .apps import PagesConfig


def pages(request):
    return {
        'INDEX_URL':      PagesConfig.INDEX_URL,
        'REFERENCES_URL': PagesConfig.REFERENCES_URL,
    }
