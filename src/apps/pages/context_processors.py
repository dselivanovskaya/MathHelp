from .apps import PagesConfig as app_conf


def url_names(request):
    return {
        'INDEX_URL':     app_conf.INDEX_URL,
        'REFERENCE_URL': app_conf.REFERENCE_URL,
    }
