from django.shortcuts import render

from .models import Topic

# Create your views here.
def theory(request):
	topics = Topic.objects.all()
	return render(request, "theory/tickets.html", {"topics": topics})
	
