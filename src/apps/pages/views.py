from django.views.generic.base import TemplateView

from .apps import PagesConfig as app_conf


class IndexView(TemplateView):
    template_name = f'{app_conf.name}/index.html'


class ReferenceView(TemplateView):
    template_name = f'{app_conf.name}/reference.html'
