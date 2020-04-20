from django.views.generic.base import TemplateView

from .apps import PagesConfig as pages_config


class IndexView(TemplateView):
    template_name = f'{pages_config.name}/index.html'


class ReferenceView(TemplateView):
    template_name = f'{pages_config.name}/reference.html'
