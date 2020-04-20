from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views import View

from forum.forms import CommentForm
from forum.models import Comment

from .models import Ticket


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class TicketListView(View):

    template_name = 'tickets/ticket-list.html'

    def get(self, request):
        context = {'tickets': Ticket.objects.all()}
        return render(request, self.template_name, context)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class TicketDetailView(View):

    template_name = 'tickets/ticket-detail.html'
    form_class = CommentForm

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        form = self.form_class(ticket, request.user)
        comments =  Comment.objects.filter(ticket__id=id)
        return render(request, self.template_name, {'ticket': ticket, 'form': form, 'comments': comments})


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class TicketReadPDFView(View):

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        if ticket.name not in request.session['watched_tickets']:
            request.session['watched_tickets'].append(ticket.name)
        try:
            return FileResponse(open(ticket.get_absolute_path(), 'rb'))
        except FileNotFoundError:
            raise Http404
