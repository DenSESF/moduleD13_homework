from datetime import datetime

from django.urls import reverse_lazy
from django.http import  HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import (
    ListView, DetailView, DeleteView, CreateView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count
from posts.models import Advert, Image, Reply
from .forms import PostCreateForm, PostUpdateForm, ReplyForm


class PostsList(ListView):
    # model = Advert
    queryset = Advert.objects.prefetch_related('image')
    template_name = 'pages/posts.html'
    paginate_by = 10
    # ordering = '-id'
    context_object_name = 'posts'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # advert = context.get(
        #   'posts').values('reply__advert').annotate(reply_count=Count('reply__advert'))
        reply = Reply.objects.filter(
            advert__in=context.get('posts')).values('advert').annotate(reply_count=Count('advert'))
        # reply = Reply.objects.all().values('advert').annotate(reply_count=Count('advert'))
        reply_count_dict = {}
        # reply_count_dict.update([(a.get('reply__advert'), a.get('reply_count')) for a in advert])
        reply_count_dict.update([(a.get('advert'), a.get('reply_count')) for a in reply])
        context['reply_count'] = reply_count_dict
        context['title'] = 'Объявления'
        return context


class PostDetail(DetailView):
    model = Advert
    template_name = 'pages/post_detail.html'
    context_object_name = 'post'


def is_owner(obj, request):
    author_name = obj.author.username
    return request.user.username == author_name

def user_directory_path(request, filename):
    username = request.user.username
    data = datetime.now().strftime('%Y%m%d%H%M%S')
    return '/'.join([username, data, filename])


class PostDelete(LoginRequiredMixin, DeleteView):
    _FORBIDDEN = 'Доступ запрещён, вы не являетесь владельцем объявления'
    model = Advert
    template_name = 'pages/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('pages:advert_all')

    def get(self, request, *args, **kwargs):
        if not is_owner(self.get_object(), request):
            return HttpResponseForbidden(self._FORBIDDEN)
        return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not is_owner(self.get_object(), request):
            return HttpResponseForbidden(self._FORBIDDEN)
        return super().post(request, *args, **kwargs)
    

class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'pages/post_create.html'
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить объявление'
        return context

    def form_valid(self, form):
        ALLOW_IMAGE_CONTENT = { 'image/png', 'image/jpeg', }
        ALLOW_VIDEO_CONTENT = { 'video/mp4', }
        fields = form.save(commit=False)
        fields.author = self.request.user
        file_video = form.cleaned_data['video']
        if (file_video
            and file_video.size < 5_000_000
            and file_video.content_type in ALLOW_VIDEO_CONTENT
        ):
            file_path = user_directory_path(self.request, file_video.name)
            fields.video.save(file_path, file_video, save=False)            
        elif file_video:
            fields.video.delete(save=False)
        fields.save()
        files_image = form.cleaned_data['images']
        imges_list = []
        if files_image:
            for file in files_image:
                if file.size < 5_000_000 and file.content_type in ALLOW_IMAGE_CONTENT:
                    file_path = user_directory_path(self.request, file.name)
                    img = Image()
                    img.image.save(file_path, file, save=True)
                    imges_list.append(img)
        fields.image.add(*imges_list)
        form.save_m2m()
        return HttpResponseRedirect(fields.get_absolute_url())


class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'pages/post_create.html'
    form_class = PostUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать объявление'
        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get(self.pk_url_kwarg)
        return Advert.objects.get(pk=id)
    
    def get(self, request, *args, **kwargs):
        advert = self.get_object()
        if not is_owner(advert, request):
            return HttpResponseRedirect(advert.get_absolute_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ALLOW_IMAGE_CONTENT = { 'image/png', 'image/jpeg', }
        ALLOW_VIDEO_CONTENT = { 'video/mp4', }
        fields = form.save(commit=False)
        file_video = form.cleaned_data['video']
        if (file_video
            and type(file_video).__name__ != 'FieldFile'
            and file_video.size < 5_000_000
            and file_video.content_type in ALLOW_VIDEO_CONTENT
        ):
            file_path = user_directory_path(self.request, file_video.name)
            fields.video.save(file_path, file_video, save=False)            
        elif file_video == False and type(file_video).__name__ != 'FieldFile':
            self.get_object().delete_file()
        fields.save()
        if form.cleaned_data['clear_images']:
            for id in form.cleaned_data['clear_images']:
                img = self.get_object().image.get(pk=str(id))
                img.delete_file()
                img.delete()
        files_image = form.cleaned_data['images']
        imges_list = []
        if files_image:
            for file in files_image:
                if file.size < 5_000_000 and file.content_type in ALLOW_IMAGE_CONTENT:
                    file_path = user_directory_path(self.request, file.name)
                    img = Image()
                    img.image.save(file_path, file, save=True)
                    imges_list.append(img)
        fields.image.add(*imges_list)
        form.save_m2m()
        return HttpResponseRedirect(fields.get_absolute_url())


class ReplyCreate(LoginRequiredMixin, CreateView):
    _FORBIDDEN = 'Невозможно оставить отклик на собственное объявление.'
    template_name = 'pages/post_create.html'
    form_class = ReplyForm
    # pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        advert = Advert.objects.get(id=self.kwargs.get(self.pk_url_kwarg))
        if is_owner(advert, self.request):
            return HttpResponseForbidden(self._FORBIDDEN)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оставить отклик'
        return context
    
    def form_valid(self, form):
        fields = form.save(commit=False)
        advert = Advert.objects.get(id=self.kwargs.get(self.pk_url_kwarg))
        if is_owner(advert, self.request):
            return HttpResponseForbidden(self._FORBIDDEN)
        fields.advert = advert
        fields.author = self.request.user
        fields.save()
        form.save_m2m()
        return HttpResponseRedirect(fields.get_absolute_url())
    