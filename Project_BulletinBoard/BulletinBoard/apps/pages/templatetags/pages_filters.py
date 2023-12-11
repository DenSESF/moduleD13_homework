from django import template


register = template.Library()


@register.filter(name='cut_path')
def cut_path(value):
    if not isinstance(value, str):
        try:
            return str(value).split('/')[-1]
        except TypeError:
            return f'Ошибка преобразования {type(value)} в {type(str)}'
    return value.split('/')[-1]


@register.filter(name='get_reply_count')
def get_reply_count(value, id):
    return value.get(id)
