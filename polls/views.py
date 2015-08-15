from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from polls.models import Choice, Poll
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        '''Return the last five published olls.'''
        return Poll.objects.filter(
                pub_date__lte = timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    def get_queryset(self):
        '''
            Excludes any polls that aren't published yet.
        '''
        return Poll.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

def vote(request, poll_id):
    try:
        poll = Poll.objects.get(pk = poll_id)
    except Poll.DoesNotExist:
        raise Http404
    try:
        selected_choice = poll.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        template = loader.get_template('polls/detail.html')
        context = RequestContext(request, {'error_message': "You didn't select a choice.", 'poll': poll, })
        #return HttpResponseRedirect(reverse('polls:detail', args = (3 - poll.id, )))
        return HttpResponse(template.render(context))
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args = (poll.id, )))

