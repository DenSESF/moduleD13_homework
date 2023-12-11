from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect

from .filters import ReplyFilter
from posts.models import Reply


class RepliesList(LoginRequiredMixin, ListView):
    # model = Reply
    # queryset = Reply.objects.prefetch_related('advert', 'author')
    template_name = 'profiles/replies.html'
    ordering = '-id'
    # paginate_by = 10
    # paginate_orphans = 4    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отклики'
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        id = self.request.user.id
        # queryset = super().get_queryset().filter(advert__author__id=id)
        queryset = Reply.objects.filter(
            advert__author__id=id).prefetch_related('advert', 'author')
        self.filterset = ReplyFilter(
            self.request.GET,
            request=self.request,
            queryset=queryset
        )
        return self.filterset.qs


@login_required
@csrf_protect
def action_reply(request, username=None, action=None):
    def delete(id):
        reply = Reply.objects.get(pk=id)
        reply.delete()

    def accept(id):
        reply = Reply.objects.get(pk=id)
        reply.accept = True
        reply.save()

    ACTIONS = {
        'delete_reply': delete,
        'accept_reply': accept,
    }
    url = reverse_lazy('profiles:replies', args=[request.user.username])
    if request.user.username != username:
        return redirect(url)
    if action not in ACTIONS.keys():
        return redirect(url)
    if request.POST.get('reply_id') is not None:
        reply_id = request.POST.get("reply_id")
        ACTIONS[action](reply_id)
    return redirect(url)
