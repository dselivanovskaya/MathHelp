from .apps import PagesConfig as pages_config


def pages(request):
    return {
        'INDEX_URL':      pages_config.INDEX_URL,
        'REFERENCES_URL': pages_config.REFERENCES_URL,
    }
