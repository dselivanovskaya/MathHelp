from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from accounts.decorators import anonymous_required

from .apps import PagesConfig


@method_decorator(anonymous_required, name='dispatch')
class IndexView(TemplateView):
    template_name = f'{PagesConfig.name}/index.html'


class ReferencesView(TemplateView):
    template_name = f'{PagesConfig.name}/references.html'
