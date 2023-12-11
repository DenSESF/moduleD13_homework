from django.forms import Select
from django_filters import FilterSet, ModelChoiceFilter

from posts.models import Advert, Reply

def adverts(request):
    if request is None:
        return Advert.objects.none()
    id = request.user.id
    advert = Advert.objects.filter(reply__advert__author__id=id).distinct()
    return advert

class ReplyFilter(FilterSet):
    advert = ModelChoiceFilter(
        lookup_expr='exact',
        label = 'Объявление:',
        queryset = adverts,
        widget=Select(attrs={ 'class': 'form-select-sm' })
    )

    class Meta:
        model = Reply
        fields = [ 'advert', ]
